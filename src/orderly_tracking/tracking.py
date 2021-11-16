import requests
from typing import Optional
from .errors import IntegrationError, InternalConnectionError

class Tracker:
    def __init__(
        self, team_code, ds_id, relay_url, cerem_url, timeout=10,
        skip_internal_errors=True, skip_connection_errors=False, *args, **kwargs
    ) -> None:
        self.team_code = team_code
        self.ds_id = ds_id
        self.relay_url = relay_url
        self.cerem_url = cerem_url
        self.timeout = timeout
        self.skip_internal_errors = skip_internal_errors
        self.skip_connection_errors = skip_connection_errors

    def click_event(self, version: str, url: str, title: str, target: str,
                    language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                    sd: str = '', sr: str = '', did: str = '', view_port_size: str = '', *args, **kwargs
                    ):
        try:
            return self._record_event(
                version=version, action='click', url=url, title=title, target=target,
                language=language, cid=cid, decode_format=decode_format, sd=sd,
                sr=sr, did=did, view_port_size=view_port_size
            )
        except InternalConnectionError as e:
            if not self.skip_connection_errors:
                raise e
        except IntegrationError as e:
            if not self.skip_internal_errors:
                raise e
        except Exception as e:
            raise e

    def view_event(self, version: str, url: str, title: str, target: str,
                   language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                   sd: str = '', sr: str = '', did: str = '', view_port_size: str = '', *args, **kwargs
                   ):
        try:
            return self._record_event(
                version=version, action='view', url=url, title=title, target=target,
                language=language, cid=cid, decode_format=decode_format, sd=sd,
                sr=sr, did=did, view_port_size=view_port_size
            )
        except InternalConnectionError as e:
            if not self.skip_connection_errors:
                raise e
        except IntegrationError as e:
            if not self.skip_internal_errors:
                raise e
        except Exception as e:
            raise e

    def _record_event(self, version: str, action: str, url: str, title: str, target: str,
                      language: str = 'zh-tw', cid: Optional[str] = None, decode_format: str = '',
                      sd: str = '', sr: str = '', did: str = '', view_port_size: str = ''):

        if cid is None:
            try:
                response = requests.get(self.cerem_url + '/tracking/generate-cid/', params={'team_code': self.team_code}, timeout=self.timeout)
            except Exception as e:
                raise InternalConnectionError('Cannot connect to Cerem, got response:', e)

            if response.status_code == 404:
                raise IntegrationError('Team code is invalid')

            elif response.status_code != 200:
                raise IntegrationError('Cannot get cid from Cerem, got response:', response.text)

        cid = response.json()['cid']

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
        try:
            requests.get(self.relay_url + '/api/'+ self.ds_id +'/tracking/', params=payload, timeout=self.timeout)
        except Exception as e:
            raise InternalConnectionError('Cannot connect to Relay:', e)

        if response.status_code != 200:
            raise InternalConnectionError('Cannot deliver tracking payload to Relay:', response.text)

        return cid
