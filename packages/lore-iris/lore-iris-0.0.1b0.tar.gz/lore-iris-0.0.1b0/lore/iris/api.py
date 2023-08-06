import requests 
import yaml
import json
import pkgutil
import os
from getpass import getpass

from pathlib import Path

from http import HTTPStatus
from functools import wraps

from .objects import SearchResult


DEFAULT_VERSION = "0.1"

AUTH_URL = "https://api.iris-main.lore.ai/user"

def auth_wrapper(f):
    """wrap backend functions to allow somce nice systematic logging of when
    they're called.
    """

    @wraps(f)
    def wrap_auth(*args, **kwargs):
        funcname = f.__name__
        api = args[0]
        try:
            ret = f(*args, **kwargs)
        except ApiError as e:
            if e.code == HTTPStatus.UNAUTHORIZED:
                print( (f"Authorization failed.  Visit {api.auth_url} "
                    "to get your token and then update your iris.yaml"))
                new_token = getpass(prompt="Token: ",stream=None)
                api._save_config(new_token = new_token)
                api._load_config()
                # we only try this one more time
                ret = f(*args, **kwargs)
            else:
                raise e
        return ret

    return wrap_auth




class ApiError(Exception):

    def __init__(self, code, reason, response):
        self.code = code
        self.reason = reason
        self.response = response

    def __repr__(self):
        return f"ApiError [code: {self.code}]: {self.reason}"


def _get_conf_file():
    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources

    from . import conf  # relative-import the *package* containing the templates

    conf_data = pkg_resources.read_text(conf, 'iris.yaml')
    return conf_data


class IrisApiClient():


    def __init__(
            self,
            conf_file: str=None
        ):
        """
        """
        self._load_config()



    def _load_config(self,
            conf_file: str = None
            ):
        """
        """
        conf = None
        if conf_file:
            with open(conf_file, 'r') as fl:
                conf = yaml.load(fl, Loader=yaml.SafeLoader)
        else:
            # try the user's homedir
            home = str(Path.home())
            conf_file = os.path.join(home, ".config", "iris", "iris.yaml")
            if os.path.exists(conf_file):
                with open(conf_file, 'r') as fl:
                    conf = yaml.load(fl, Loader=yaml.SafeLoader)
            else:
                conf= yaml.load(_get_conf_file(), Loader=yaml.SafeLoader)
        self._conf = conf
        self._server = conf['irisapi']['server']
        if not self._server.endswith("/"):
            self._server += "/"
        self._token = conf['irisapi']['token']
        self._version = DEFAULT_VERSION
        if 'version' in conf['irisapi']:
            self._version = conf['irisapi']['version']
        self.headers = {
            "Content-Type": "application/json", 
            "Authorization": "Token %s" % self._token
        }
        self.auth_url = "%s/user"%(self._server)
        self._last_response = None

    def _save_config(self,
            new_token: str=None):
        if new_token:
            self._conf["irisapi"]["token"]=new_token
            self._token=new_token
            print("Updated to new token")
        # try the user's homedir
        home = str(Path.home())
        conf_dir = os.path.join(home, ".config", "iris")
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        conf_file = os.path.join(conf_dir, "iris.yaml")
        with open(conf_file, 'w') as fl:
            yaml.dump(self._conf, fl)
            print(f"Config file saved to {conf_file}")


    def _call_api_function(self,
            api_function,
            api_data,
            http_type = "get"):
        """
        Execute api call, print the response, and return the response.
        """
        #api_data["docset_ids"] = list(range(20))
        endpoint_url = "%sapi/v%s/%s/"%(self._server, self._version, api_function)
        #endpoint_url = endpoint_url.replace("//", "/")

        #print(f"Using url: {endpoint_url}")
        if http_type == "get":
            response = requests.get(
                url=endpoint_url,
                params=api_data,
                headers=self.headers,
                verify=True
            )
        elif http_type == "post":
            response = requests.post(
                url=endpoint_url,
                data=json.dumps(api_data),
                headers=self.headers,
                verify=True
            )
        self._last_response = response
        #print(response.ok)
        #print(response.status_code)
        #print(response.url)
        if not response.ok:
            raise ApiError(
                    response.status_code,
                    response.reason,
                    response
                    )
        return response


    @auth_wrapper
    def get_token(self):
        resp = self._call_api_function(
                api_function = "get_token/",
                api_data = {}
                )
        data = json.loads(resp.content)
        return data['token']

    @auth_wrapper
    def search(self,
            docset_name: str,
            query_string: str,
            max_results: int=None,
            fuzzy: bool=None,
            filters: dict=None,
            sorts: dict=None
        ):
        search = SearchResult(
            client=self,
            docset_name=docset_name,
            query_string=query_string,
            max_results=max_results,
            fuzzy=fuzzy,
            filters=filters,
            sorts=sorts)
        return search

    





