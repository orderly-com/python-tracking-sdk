import requests
from typing import Optional


class Tracker:
    def __init__(self, relay_url, cerem_url) -> None:
        self.relay_url = relay_url
        self.cerem_url = cerem_url

    def click_event(self, version: str, url: str, title: str, target: str,
            language: str='zh-tw', cid: Optional[str]=None, decode_format: str='',
            sd: str='', sr: str='', did: str='', view_port_size: str=''
    ):
        self._record_event(
            version=version, action='click', url=url, title=title, target=target,
            language=language, cid=cid, decode_format=decode_format,sd=sd,
            sr=sr, did=did, view_port_size=view_port_size
        )

    def view_event(self, version: str, url: str, title: str, target: str,
            language: str='zh-tw', cid: Optional[str]=None, decode_format: str='',
            sd: str='', sr: str='', did: str='', view_port_size: str=''
    ):
        self._record_event(
            version=version, action='view', url=url, title=title, target=target,
            language=language, cid=cid, decode_format=decode_format,sd=sd,
            sr=sr, did=did, view_port_size=view_port_size
        )

    def _record_event(self, version: str, action: str, url: str, title: str, target: str,
        language: str='zh-tw', cid: Optional[str]=None, decode_format: str='',
        sd: str='', sr: str='', did: str='', view_port_size: str=''):

        if cid is None:
            try:
                response = requests.get(self.cerem_url + '/tracking/generate-cid/')
                cid = response.json()['cid']
            except Exception:
                return

        payload = {
            'v': version,
            'cid': cid,
            'tg': target,
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
        requests.get(self.relay_url + '/api/1/1', params=payload)
        return cid
