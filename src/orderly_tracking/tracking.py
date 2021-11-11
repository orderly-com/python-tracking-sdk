import requests
import uuid
from typing import Optional
from . import settings

ACTION_VIEW = 'view'
ACTION_CLICK = 'click'

AVALIBLE_ACTIONS = [ACTION_VIEW, ACTION_CLICK]

class ActionTypeNotAllowed(Exception):
    pass

def record_event(version: str, action: str, url: str, title: str,
    language: str='zh-tw', cid: Optional[str]=None, decode_format: str='UTF-8',
    sd: str='24-bit', sr: str='1920x1080', did: str='tl', view_port_size: str='1905x887'):

    if action not in AVALIBLE_ACTIONS:
        raise ActionTypeNotAllowed(f'{action} is not a valid action type, use tracking.ACTION_VIEW instead. Check tracking.AVALIBLE_ACTIONS for choices')

    if cid is None:
        cid = uuid.uuid4().hex[:16].lower()

    payload = {
        'v': version,
        'cid': cid,
        'de': decode_format,
        'at': action,
        'ul': language,
        'pt': url,
        'sd': sd,
        'sr': sr,
        'tl': title,
        'did': did,
        'vp': view_port_size
    }
    requests.get(settings.RELAY_URL+'/api/1/1', params=payload)
    return cid
