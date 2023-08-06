# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import time
from functools import partial
from typing import Optional

from os_scrapy_kafka_pipeline.pipelines import (
    KAFKA_PRODUCER_BROKERS,
    KAFKA_PRODUCER_CLOSE_TIMEOUT,
    KAFKA_PRODUCER_CONFIGS,
    KAFKA_PRODUCER_LOGLEVEL,
    KAFKA_PRODUCER_TOPIC,
    KafKaRecord,
)
from os_scrapy_kafka_pipeline.producer import AutoProducer
from os_scrapy_kafka_pipeline.utils import loglevel
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.python import to_bytes
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet import threads


class LichScrapyExtractsPipeline(object):
    def __init__(self, crawler):
        self.crawler = crawler
        settings = self.crawler.settings
        try:
            self.producer = AutoProducer(
                bootstrap_servers=settings.getlist(KAFKA_PRODUCER_BROKERS),
                configs=settings.get(KAFKA_PRODUCER_CONFIGS, None),
                topic=settings.get(KAFKA_PRODUCER_TOPIC, None),
                kafka_loglevel=loglevel(
                    settings.get(KAFKA_PRODUCER_LOGLEVEL, "WARNING")
                ),
            )
        except Exception as e:
            raise NotConfigured(f"init producer {e}")
        self.logger = logging.getLogger(self.__class__.__name__)
        crawler.signals.connect(self.spider_closed, signals.spider_closed)
        self.encoder = ScrapyJSONEncoder()

    def kafka_record(self, item) -> KafKaRecord:
        record = KafKaRecord()
        if "meta" in item and isinstance(item["meta"], dict):
            meta = item["meta"]
            record.meta = meta
            record.topic = meta.get("extractor2.kafka.topic", None)
            record.key = meta.get("extractor2.kafka.key", None)
            record.partition = meta.get("extractor2.kafka.partition", None)
            bootstrap_servers = meta.get("extractor2.kafka.brokers", None)
            if isinstance(bootstrap_servers, str):
                record.bootstrap_servers = bootstrap_servers.split(",")

        return record

    def kafka_value(self, item, record) -> Optional[bytes]:
        record.ts = time.time()
        try:
            result = item["meta"].get("extractor2.extracts", None)
            if result is None:
                raise NotConfigured("empty extractor2.extracts")
            record.value = to_bytes(self.encoder.encode(result))
            record.dmsg["size"] = len(record.value)
        except Exception as e:
            record.dmsg["err"] = e
            raise e
        finally:
            record.dmsg["encode_cost"] = time.time() - record.ts

    def _log_msg(self, item, record):
        err = record.dmsg.pop("err", None)
        msg = " ".join(
            [
                f"{k}:{v:.5f}" if k.endswith("_cost") else f"{k}:{v}"
                for k, v in record.dmsg.items()
            ]
        )
        msg = f"topic:{record.topic} partition:{record.partition} {msg}"
        if err:
            self.logger.error
            msg = f"{msg} err:{err}"
            record.dmsg["err"] = err
        return msg

    def log(self, item, record):
        logf = self.logger.debug
        if "err" in record.dmsg and record.dmsg["err"]:
            logf = self.logger.error
        logf(self._log_msg(item, record))

    def on_send_succ(self, item, record, metadata):
        record.topic = metadata.topic
        record.partition = metadata.partition
        record.dmsg["offset"] = metadata.offset
        record.dmsg["send_cost"] = time.time() - record.ts
        self.log(item, record)

    def on_send_fail(self, item, record, e):
        record.dmsg["err"] = e
        record.dmsg["send_cost"] = time.time() - record.ts
        self.log(item, record)

    def send(self, item, record):
        record.ts = time.time()
        try:
            self.producer.send(
                topic=record.topic,
                value=record.value,
                key=record.key,
                headers=record.headers,
                partition=record.partition,
                timestamp_ms=record.timestamp_ms,
                bootstrap_servers=record.bootstrap_servers,
            ).add_callback(partial(self.on_send_succ, item, record)).add_errback(
                partial(self.on_send_fail, item, record)
            )
        except Exception as e:
            record.dmsg["err"] = e
            record.dmsg["send_cost"] = time.time() - record.ts
            self.log(item, record)

        return item

    def process_item(self, item, spider):
        record = self.kafka_record(item)
        if record.bootstrap_servers is None or len(record.bootstrap_servers) == 0:
            return item
        try:
            self.kafka_value(item, record)
        except:
            self.log(item, record)
            return item
        return threads.deferToThread(self.send, item, record)

    def spider_closed(self, spider):
        if self.producer is not None:
            settings = self.crawler.settings
            self.producer.close(settings.get(KAFKA_PRODUCER_CLOSE_TIMEOUT, None))
            self.producer = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
