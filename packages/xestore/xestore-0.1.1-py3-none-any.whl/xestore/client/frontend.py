
import param
import panel as pn
import os
import httpx
import tempfile
import base64
import json
from io import BytesIO, BufferedReader
import pathlib
from xestore.settings import config
from .http_client import HttpxClient
from .auth import Oauth2DeviceFlow


class Resource(param.Parameterized):
    http_client = param.ClassSelector(HttpxClient)
    path = param.String()
    _created = param.String(constant=True)
    _updated = param.String(constant=True)
    _version = param.Integer(None, constant=True)

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def view(self):
        return pn.Param(self.param)

    def _repr_mimebundle_(self, include=None, exclude=None):
        mimebundle = self.view()._repr_mimebundle_(include, exclude)
        return mimebundle

    def __repr__(self):
        return self.name

class File(Resource):
    _id = param.String(constant=True)
    name = param.String(constant=True)
    extension = param.String(constant=False)
    
    metadata = param.Dict(constant=True)
    content_type = param.String(constant=True)
    length = param.Integer(0, constant=True)
    

    @classmethod
    def from_dict(cls, data):
        params = {k: data.get(k, v.default) for k, v in cls.param.params().items()}
        fdata = data.get("data", {})
        if fdata is not None:
            params.update(fdata)
        if "file" in params:
            
            params["path"] = "media" + params.pop("file").partition("media")[-1]
        
        return cls(**params)

    @property
    def filename(self):
        return ".".join([self.name, self.extension])

    def download(self, f=None):
        if f is None:
            download_file = tempfile.NamedTemporaryFile()
        elif isinstance(f, str):
            if os.path.isdir(f):
                path = os.path.join(f, self.filename)
            else:
                path = f
            download_file = open(path, "wb")
        elif isinstance(f, BytesIO):
            download_file = f
        else:
            raise TypeError("Invalid file type given.")

        self.http_client.download_file(self.path, download_file)
        download_file.seek(0)
        return download_file

    def view(self):
        fwidget = pn.widgets.FileDownload(callback=self.download, filename=self.filename)
        params = pn.Param(self.param, parameters=[name for name in self.param.objects() if name not in ["http_client"]])
        return pn.Column(params, fwidget)


class Document(Resource):
    _id = param.String(constant=True)
    name = param.String(constant=True)
    data = param.Dict(constant=True)
    metadata = param.Dict(constant=True)
    
    @classmethod
    def from_dict(cls, data):
        params = {k: data.get(k, v.default) for k, v in cls.param.params().items()}
        return cls(**params)

class XeEndpoint(param.Parameterized):
    http_client = param.ClassSelector(HttpxClient)
    resource_class = param.ClassSelector(Resource, is_instance=False)
    path = param.String("/")

    def __getitem__(self, name):
        return self.get_by_name(name)

    def make_resource(self, data):
        data = dict(data)
        data["http_client"] = self.http_client
        resource = self.resource_class.from_dict(data)
        return resource

    def find(self, query={}, projection={}, max_results=100, page=1, timeout=10):
        params={
            "where": query,
            "projection": projection,
            "max_results": max_results,
            "page": page,
            "timeout": timeout,
        }
        r = self.http_client.get(self.path, params=params)
        return [self.make_resource(d) for d in r.get("_items", [])]

    def ids(self, max_results=100, page=1, timeout=10):
        params={
            "projection": '{"_id":1, "name":1}',
            "max_results": max_results,
            "page": page,
            "timeout": timeout,
        }
        r = self.http_client.get(self.path, params=params)
        ids = {d["name"]: d["_id"] for d in r.get("_items", [])}
        return ids

    def names(self, max_results=100, page=1, timeout=10):
        params={
                "projection": '{"name": 1}',
                "max_results": max_results,
                "page": page,
                "timeout": timeout,
            }
        r = self.http_client.get(self.path, **params)
        names = [d["name"] for d in r.get("_items", [])]
        return names

    def get_by_id(self, _id, timeout=10, return_raw=False):
        url = "/".join([self.path, _id])
        params = {"timeout": timeout}
        data = self.http_client.get(url, **params)
        if not data:
            raise KeyError(f"Failed to fetch {_id}. Either not found in database or connection refused.")
        if return_raw:
            item = data
        else:
            item = self.make_resource(data)
        return item

    def get_by_name(self, name, timeout=10, return_raw=False):
        _id = self.get_id(name)
        if _id is None:
            raise ConnectionError(f"Failed to fetch id for {name}.")
        return self.get_by_id(_id, timeout=10, return_raw=return_raw)

    def get_version(self, _id, version, timeout=10, return_raw=False, **kwargs):
        url = "/".join([self.path, _id])
        params = {"timeout": timeout, "version": version}
        params.update(kwargs)
        data = self.http_client.get(url, **params)
        if not data:
            raise KeyError(f"Failed to fetch {_id}. Either not found in database or connection refused.")
        if return_raw:
            item = data
        else:
            item = self.make_resource(data)
        return item

    def get_id(self, name):
        url = "/".join([self.path, name])
        params={
                "projection": '{"_id": 1}',
                "max_results":1,

            }
            
        r = self.http_client.get(url,)
        items = r.get("_items", [])
        if items:
            return items[0].get("_id", None)
        elif "_id" in r:
            return r["_id"]

    def keys(self):
        yield from self.names()

    def values(self):
        for name in self.names():
            yield self[name]

    def items(self):
        for name in self.names():
            yield name, self[name]

    def get(self, name, default=None):
        try:
            self[name]
        except Exception as e:
            if default is not None:
                return default
            else:
                raise e

    def delete(self, name):
        _id = self.get_id(name)
        url = "/".join([self.path, _id])
        return self.http_client.delete(url)

    def view(self):
        return pn.Panel(self.param)

class XeFiles(XeEndpoint):
    private = param.ClassSelector(XeEndpoint)

    def open(self, name):
        return self[name].file

    def __init__(self, isroot=True, **params):
        path  = params.get("path", "/files")
        params["path"] = path
        if isroot:
            params["private"] = self.__class__(path=f"{path}/private",
                                             isroot=False, http_client=params["http_client"])
        params["resource_class"] = File
        super().__init__(**params)

    def upload(self, f, name=None, extension=None, **metadata):
        if isinstance(f, BufferedReader):
            if name is None:
                name = f.name.rpartition(".")[0]
            if extension is None:
                extension = f.name.rpartition(".")[-1]
        elif isinstance(f, str) and pathlib.Path(f).is_file():
            if name is None:
                name = f.rpartition(".")[0]
            if extension is None:
                extension = f.rpartition(".")[-1]
            f = open(f, "rb")
        else:
            raise ValueError("Must provide a file object object or a path to an existing file.")
        
        data = {"name": name, "extension": extension}
        r = self.http_client.post(self.path, data=data, files={"data": f})
        if not r:
            raise ConnectionError("Failed to upload file.")
        if isinstance(f, BufferedReader):
            f.close()
        return name


class XeDocuments(XeEndpoint):
    private = param.ClassSelector(XeEndpoint, constant=True)

    def __init__(self, isroot=True, **params):
        path  = params.get("path", "/documents")
        params["path"] = path
        if isroot:
            params["private"] = self.__class__(path=f"{path}/private", 
                                            isroot=False, http_client=params["http_client"])
        params["resource_class"] = Document
        super().__init__(**params)
    

    def upload(self, document: dict, name: str,  **metadata):
        if not isinstance(name, str):
            raise TypeError("Document name must be a string")
        if not isinstance(document, dict):
            raise TypeError("Document must be a dict")
     
        data = {"name": name, "data": document, "metadata": metadata}
        r = self.http_client.post(self.path, json=data)
        if not r:
            print(self.http_client._log)
            return r
        return name
        
    def update(self, document, name, **metadata):
        if not isinstance(name, str):
            raise TypeError("Document name must be a string")
        if not isinstance(document, dict):
            raise TypeError("Document must be a dict")
        data = {"name": name, "data": document, "metadata": metadata}
        
        _id = self.get_id(name)
        path = "/".join([self.path.strip("/"), _id])
        r = self.http_client.put(path, json=data, )
        if not r:
            raise ConnectionError("Failed to upload file.")
        return name

    def versions(self, name):
        _id = self.get_id(name)
        path = "/".join([self.path.strip("/"), _id])
        r = self.http_client.get(path, version="all", )
        if "_items" in r:
            return [d["_version"] for d in r["_items"]]
        else:
            raise ConnectionError("Failed to retreive document versions.")

    def get_version(self, name, v):
        _id = self.get_id(name)
        path = "/".join([self.path.strip("/"), _id])
        r = self.http_client.get(path, version=v,)
        if "_items" in r:
            return [self.make_resource(d) for d in r["_items"]]
        else:
            return self.make_resource(r)

class XeStore(param.Parameterized):
    http_client = param.ClassSelector(HttpxClient)
    auth = param.ClassSelector(Oauth2DeviceFlow, default=Oauth2DeviceFlow())
    files = param.ClassSelector(XeFiles)
    documents = param.ClassSelector(XeDocuments)

    def __init__(self, **params):
        server_url = params.get("server_url", config.API_SERVER)
        client = HttpxClient()
        params["http_client"] = client
        params["files"] = XeFiles(http_client=client)
        params["documents"] = XeDocuments(http_client=client)
        super().__init__(**params)

    def login(self, notify_emails="", webbrowser=True):
        if isinstance(notify_emails, list):
            notify_emails = ",".join(notify_emails)
        self.http_client.auth.notify_email = notify_emails
        self.http_client.login(webbrowser)