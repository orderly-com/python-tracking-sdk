import requests
from typing import Optional
from . import settings

def record_event(msg: str, place: str, pt: str, title: str,
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
    record_raw_event(payload)


def record_raw_event(payload): # payload must match the standard format
    requests.get(settings.RELAY_URL+'/api/1/1', params=payload)