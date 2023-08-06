from .utils import error_suppress, false
import requests


class Action:
    def __init__(self, echoer_url, req_url, name):
        self.name = name
        self.req_url = req_url
        self.params = ''
        self.echoer_url = echoer_url

    def add_data(self, dictData):
        if not isinstance(dictData, dict):
            return False
        length = len(dictData)
        params = '('
        for k, v in dictData.items():
            if str(v) != 'str' and str(v) != 'int':
                return False
            if length == 1:
                params += f'{v} {k})'
            else:
                params += f'{v} {k},'
            length -= 1
        self.params = params
        return True

    def generate(self):
        data = \
            f"""action {self.name}
                  addr = "{self.req_url}";
                  method = http;
                  args = {self.params};
                  return = (SUCCESS | FAIL);
                action_end
            """
        return data

    def send_echoer(self):
        data = self.generate()
        action_data = {"data": data}
        with error_suppress(false):
            req = requests.post(self.echoer_url, json=action_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('action发送echoer错误', req.json())
                return False
