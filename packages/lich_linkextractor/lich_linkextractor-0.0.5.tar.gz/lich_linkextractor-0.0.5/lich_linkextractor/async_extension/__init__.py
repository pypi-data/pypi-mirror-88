import base64
import logging
import os

import ujson as json
from aiohttp import ClientSession
from scrapy.utils.python import to_unicode

from lich_linkextractor.utils import as_deferred

logger = logging.getLogger(__name__)

DEPTH_LIMIT_KEY = "extractor.depth_limit"
DROP_ANCHOR_KEY = "extractor.drop_anchor"
key_map = {
    "allow": "AllowedURLFilters",
    "deny": "DisallowedURLFilters",
    "allow_domains": "AllowedDomains",
    "deny_domains": "DisallowedDomains",
    "restrict_xpaths": "XPathQuerys",
    "restrict_css": "CSSSelectors",
    "same_domain_only": "OnlyHomeSite",
}


class AyncExtractor:
    def __init__(self, depth_limit=None, server_addr=None):
        self.depth_limit = depth_limit
        self.server_addr = server_addr
        self.client = ClientSession()

    @classmethod
    def from_crawler(cls, crawler):
        crawler.settings
        depth_limit = crawler.settings.get("DEPTH_LIMIT")
        depth_limit = int(depth_limit) if depth_limit else None
        server_addr = crawler.settings.get("EXTRACTOR_ADDR")
        return cls(depth_limit=depth_limit, server_addr=server_addr)

    def process_response(self, response):
        d = as_deferred(self.extract_links_and_extracts(response))

        def _on_success(extract_recode):
            links = extract_recode["links"]
            extracts = extract_recode["extracts"]
            if links is not None and len(links) > 0:
                assert "extractor.links" not in response.meta
                response.meta["extractor.links"] = links
            if extracts is not None and len(extracts) > 0:
                assert "extractor2.extracts" not in response.meta
                response.meta["extractor2.extracts"] = extracts

        d.addCallback(_on_success)
        d.addBoth(lambda _: response)
        return d

    def _get_base_ex_req(self, response):
        base_ex_req = None
        if response.request.meta.get("render_proxy.api", None) is None:
            base_ex_req = {
                "URL": response.url,
                "Content": to_unicode(base64.encodebytes(response.body)),
                "ContentType": to_unicode(response.headers.get("Content-Type")),
            }
        else:
            render_body = json.loads(response.body.decode("utf8"))
            if (
                "renderStatus" in render_body
                and render_body["renderStatus"] == "RENDER_OK"
                and render_body["httpStatus"] < 300
                and render_body["httpStatus"] >= 200
            ):
                base_ex_req = {
                    "URL": render_body["url"],
                    "Content": to_unicode(
                        base64.encodebytes(render_body["renderPage"].encode("utf-8"))
                    ),
                    "ContentType": "html;charset=utf-8",
                }
        return base_ex_req

    async def _get_links(self, rules, response):
        res = []
        base_ex_req = self._get_base_ex_req(response)
        if base_ex_req is None:
            return res
        for rule in rules:
            ex_req = base_ex_req
            for key in [
                "allow",
                "deny",
                "allow_domains",
                "deny_domains",
                "restrict_xpaths",
                "restrict_css",
                "same_domain_only",
            ]:
                v = rule.get(key, None)
                if v is not None and (
                    isinstance(v, str)
                    or (
                        isinstance(v, (list, tuple))
                        and all(isinstance(i, str) for i in v)
                    )
                    or isinstance(v, bool)
                ):
                    ex_req[key_map[key]] = v
            resp = await self._send(self.server_addr, json.dumps(ex_req), 3)
            s = set()
            for value in resp.values():
                for link in value:
                    s.add(link)
            res.append(list(s))
        return res

    async def _get_extracts(self, extract_template, response):
        base_ex_req = self._get_base_ex_req(response)
        if base_ex_req is None:
            return res
        ex_req = base_ex_req
        ex_req["template"] = extract_template
        resp = await self._send(
            os.path.join(self.server_addr, "extract"), json.dumps(ex_req), 3
        )
        return resp["extract"]

    def _get_max_depth(self, req_depth_limit):
        if self.depth_limit is None:
            return req_depth_limit
        if req_depth_limit is None:
            return self.depth_limit
        return min(self.depth_limit, req_depth_limit)

    async def extract_links_and_extracts(self, response):
        extract_recode = {}
        meta = response.request.meta
        extracts = None
        links = None
        extract_template = response.request.meta.get("extractor2.template", None)
        if extract_template is not None and isinstance(extract_template, dict):
            extracts = await self._get_extracts(extract_template, response)
        rules = response.request.meta.get("extractor.rules", None)
        if rules is not None and isinstance(rules, list):
            # check depth limit
            depth = int(meta["depth"]) if "depth" in meta else None
            req_depth_limit = (
                int(meta[DEPTH_LIMIT_KEY]) if DEPTH_LIMIT_KEY in meta else None
            )
            max_depth = self._get_max_depth(req_depth_limit)
            if not (max_depth and depth and depth >= max_depth):
                links = await self._get_links(rules, response)
        extract_recode["links"] = links
        extract_recode["extracts"] = extracts
        return extract_recode

    async def _send(self, addr, data, num_retries):
        if addr != None and data != None:
            async with self.client.post(addr, data=data) as response:
                if response.status == 200:
                    return await response.json()
                if response.status == 404:
                    if num_retries > 0:
                        return await self._send(addr, data, num_retries - 1)
                response.raise_for_status()

    async def spider_closed(self):
        return await self.client.close()
