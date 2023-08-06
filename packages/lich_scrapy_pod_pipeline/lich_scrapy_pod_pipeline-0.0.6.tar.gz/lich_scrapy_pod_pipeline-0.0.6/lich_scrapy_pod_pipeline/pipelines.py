# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from typing import Optional

from scrapy import signals
from scrapy.utils.python import to_bytes
from scrapy.utils.serialize import ScrapyJSONEncoder

from .sender import HttpSender
from .utils import as_deferred

REFERER_KEY = "extractor.referer"
HEAD_KEY = "enqueue.head"
RESERVED_KEY = "reserved"
DEPTH_KEY = "depth"


class PodPipeline:
    def __init__(self, crawler):
        self.sender = HttpSender()
        self.encoder = ScrapyJSONEncoder()
        self.logger = logging.getLogger(self.__class__.__name__)
        crawler.signals.connect(self.spider_closed, signals.spider_closed)

    def _get_request(self, urls, depth, referer, reserved, rule_meta):
        d = None
        try:
            d = int(depth)
        except Exception as e:
            d = -1
            self.logger.error("depth illegal %s", e)
        res = {
            "urls": urls,
            "meta": {DEPTH_KEY: d + 1, REFERER_KEY: referer, HEAD_KEY: True,},
        }
        if reserved is not None:
            res["meta"][RESERVED_KEY] = reserved
        if rule_meta is not None:
            for key, value in rule_meta.items():
                res["meta"][key] = value
        return res

    def _get_extracted_links(self, item) -> Optional[bytes]:
        reqs_array = []
        if (
            "meta" in item
            and isinstance(item["meta"], dict)
            and "extractor.links" in item["meta"]
            and "extractor.rules" in item["meta"]
        ):
            links = item["meta"]["extractor.links"]
            depth = item["meta"]["depth"]
            reserved = None
            if RESERVED_KEY in item["meta"]:
                reserved = item["meta"]["reserved"]
            for idx, value in enumerate(links):
                if len(value) > 0:
                    rule_meta = None
                    if idx < len(item["meta"]["extractor.rules"]):
                        rule_meta = item["meta"]["extractor.rules"][idx].get(
                            "meta", None
                        )
                    reqs = to_bytes(
                        self.encoder.encode(
                            self._get_request(
                                value,
                                depth,
                                item["request"]["url"],
                                reserved,
                                rule_meta,
                            )
                        )
                    )
                    reqs_array.append(reqs)
        return reqs_array

    def _get_addr(self, item) -> Optional[str]:
        addr = None
        if "meta" in item and isinstance(item["meta"], dict):
            meta = item["meta"]
            addr = meta.get("pod.addr", None)
        return addr

    def process_item(self, item, spider):
        addr = self._get_addr(item)
        requests = self._get_extracted_links(item)
        d = as_deferred(self.sender.multi_send(addr, requests))
        d.addBoth(lambda _: item)
        return d

    def spider_closed(self, spider):
        return self.sender.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
