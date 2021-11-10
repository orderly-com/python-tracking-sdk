import json

from typing import Optional
from aiokafka import AIOKafkaProducer

from . import settings

class Tracker:
    def __init__(self, **producer_params):
        self.producer = AIOKafkaProducer(bootstrap_servers='localhost:9092', **producer_params)

    def connect_target(self):
        pass

    async def record_event(self, msg: str, place: str, pt: str, title: str,
        language: str='zh-tw', cid: Optional[str]=None, decode_format: str='UTF-8',
        sd: str='24-bit', sr: str='1920x1080', did: str='tl', view_port_size: str='1905x887'):

        payload = {
            'v': msg,
            'cid': cid,
            'de': decode_format,
            'at': place,
            'ul': language,
            'pt': pt,
            'sd': sd,
            'sr': sr,
            'tl': title,
            'did': did,
            'vp': view_port_size
        }
        await self.producer.start()
        await self.producer.send(settings.KAFKA_TOPIC, json.dumps(payload), partition=0)
        await self.producer.stop()