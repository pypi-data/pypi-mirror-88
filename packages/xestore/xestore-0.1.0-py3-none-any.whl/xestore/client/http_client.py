import json
import time
import tempfile
import eve
import httpx
from tqdm import tqdm
import param
import os
from io import BufferedIOBase

from xestore.settings import config as settings
from .auth import Oauth2DeviceFlow


APPS = {}

class HttpxClient(param.Parameterized):
    _app_settings = param.Dict(default=None, allow_None=True)
    _self_serve = param.Boolean(False)
    server_url = param.String(
        default="http://localhost:5000/v1",
        regex=
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    )
    server_urls = param.List(default=[], class_=str)
    auth = param.ClassSelector(Oauth2DeviceFlow, default=Oauth2DeviceFlow())
    _log = param.String()
    _messages = param.List(default=[])
    _busy = param.Boolean(False)
    _client_ttl = param.Integer(600)
    _client_created = param.Number(0)
    _client = None

    @property
    def app(self):
        if not self._self_serve:
            return None
        if self.name not in APPS and self._app_settings:
            APPS[self.name] = eve.Eve(settings=self._app_settings)
        return APPS.get(self.name, None)

    @property
    def client(self):
        if self._client is None or (time.time() - self._client_created) > self._client_ttl:
            if self._client:
                self._client.close()
            self._client = httpx.Client(app=self.app, base_url=self.server_url)
            self._client_created = time.time()
        return self._client
    
    def get_client_kwargs(self):
        kwargs = {
            "headers": self.headers(),
            "base_url": self.server_url,
            "app": None,
        }
        if self._self_serve:
            kwargs["app"] = self._app_settings
        
        return kwargs

    def headers(self):
        headers = self.auth.get_headers()
        headers["Accept"] = "application/json"
        return headers

    def upload_file(self, url, _file, name=None, **kwargs):
        if isinstance(_file, BufferedIOBase):
            if name is None and hasattr(_file, "name"):
                name = _file.name.rpartition(".")[0]
            f = _file
        elif isinstance(_file, str):
            if not os.path.isfile(str):
                raise ValueError("File does not exist.")
            f = open(_file, "rb")
        else:
            raise TypeError("_file parameter must be a string or File object.")

        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            try:
                httpx.post(url, data={"name": name}, files={"data": f} **kwargs)
            finally:
                f.close()

    def download_file(self, url, f):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            with client.stream("GET", url, headers=self.auth.get_headers()) as response:
                total = int(response.headers["Content-Length"])
                with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        f.write(chunk)
                        progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded
                    
    def get(self, url, timeout=10, **params):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            try:
                resp = client.get(url,
                                params=params,
                                headers=self.headers(),
                                timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                else:
                    self.clear_messages()
                    return resp.json()
            except Exception as e:
                self.log_error(e)
            self._busy = False
            return {}
     
    def post(self, url, data=None, json=None, files=None, timeout=10, **kwargs):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            headers = self.headers()
            if files is None:
                headers["Content-Type"] = "application/json"
            headers.update(kwargs.get("headers", {}))

            try:
                resp = client.post(url,
                                   data=data,
                                   json=json,
                                   headers=headers,
                                   files=files,
                                   timeout=timeout,
                                   **kwargs)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def put(self, url, data=None, json=None, files=None, etag=None, timeout=10, **kwargs):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            headers = self.headers()
            if files is None:
                headers["Content-Type"] = "application/json"
            if etag:
                headers["If-Match"] = etag
            try:
                resp = client.put(url,
                                  data=data,
                                  json=json,
                                  files=files,
                                  headers=headers,
                                  timeout=timeout,
                                  **kwargs)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
        self._busy = False

    def patch(self, url, data, json=None, files=None, etag=None, timeout=10, **kwargs):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            headers = self.headers()
            if files is None:
                headers["Content-Type"] = "application/json"
            if etag:
                headers["If-Match"] = etag
            try:
                resp = client.patch(url,
                                    data=data,
                                    json=json,
                                    files=files,
                                    headers=headers,
                                    timeout=timeout,
                                    **kwargs)
                self._busy = False
                if resp.is_error or settings.DEBUG:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def delete(self, url, etag="", timeout=10):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            headers = self.headers()
            if etag:
                headers["If-Match"] = etag
            try:
                resp = client.delete(url, headers=headers, timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def log_error(self, e):
        try:
            e = str(e)
            log = [e] + self._log.split("\n")
            self._log = "\n".join(log[:settings.MAX_LOG_SIZE])
            self._messages = (e.split("\n")+self._messages)[:settings.MAX_MESSAGES]
        except:
            pass

    def clear_messages(self):
        self._messages = []

    def set_token(self, token):
        self.auth.set_token(token)

    def login(self, webbrowser=True):
        self.auth.login(webbrowser)

    def __getstate__(self):
        state = super().__getstate__() 
        state.pop("_client", None)
        return state

