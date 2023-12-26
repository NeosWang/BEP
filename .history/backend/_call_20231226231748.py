import requests
import json
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Call:
    setup_request = requests.session()
    # setup_request.keep_alive = False


    def __init__(
            self,
            payload,
            domain,
            endpoint='',
            api_key=None,
            app_json=True,
            key_str=None) -> None:

        self.time = datetime.now()
        self.url = domain + endpoint
        self.api_key = api_key

        self.payload = payload
        self.app_json = app_json
        self.key_str = key_str

        self.res=None
        self.log_name=None

        self.run()

    def __headers(self):
        type = 'application/json' if self.app_json else "application/x-www-form-urlencoded"
        return {
            'api_key': self.api_key,
            "Content-Type": type
        }


    def run(self):
        headers = self.__headers()
        data = json.dumps(
            self.payload) if "json" in headers['Content-Type'] else self.payload

        self.res = self.setup_request.post(
            url=self.url,
            headers=headers,
            data=data,
            verify=False,
        )

