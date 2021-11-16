import requests
from typing import Optional


class Tracker:
    def __init__(self, team_code, ds_id, relay_url, cerem_url, *args, **kwargs) -> None:
        self.team_code = team_code
        self.ds_id = ds_id
        self.relay_url = relay_url
        self.cerem_url = cerem_url

    def click_event(self, version: str, url: str, title: str, target: str,
                    language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                    sd: str = '', sr: str = '', did: str = '', view_port_size: str = '', *args, **kwargs
                    ):
        self._record_event(
            version=version, action='click', url=url, title=title, target=target,
            language=language, cid=cid, decode_format=decode_format, sd=sd,
            sr=sr, did=did, view_port_size=view_port_size
        )

    def view_event(self, version: str, url: str, title: str, target: str,
                   language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                   sd: str = '', sr: str = '', did: str = '', view_port_size: str = '', *args, **kwargs
                   ):
        self._record_event(
            version=version, action='view', url=url, title=title, target=target,
            language=language, cid=cid, decode_format=decode_format, sd=sd,
            sr=sr, did=did, view_port_size=view_port_size
        )

    def _record_event(self, version: str, action: str, url: str, title: str, target: str,
                      language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                      sd: str = '', sr: str = '', did: str = '', view_port_size: str = ''):

        if cid is None:
            try:
                response = requests.get(self.cerem_url + '/tracking/generate-cid/', params={'team_code': self.team_code})
                cid = response.json()['cid']
            except Exception:
                return

        payload = {
            'tc': self.team_code,
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
        requests.get(self.relay_url + '/api/'+ self.ds_id +'/tracking/', params=payload)
        return cid
