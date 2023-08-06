import requests
from utils import error_suppress, false
from step import Step


class FlowRun:

    def __init__(self, req_url, name):
        self.req_url = req_url
        self._name = name
        self._step_list = []
        self._desc = []
        self._step = []

    def add_step(self, name, step, action, args):
        new_step = Step(name=name, action=action)
        desc = new_step.flow_return(step=step, args=args)
        self._step = list(set(self._step).union(set(desc)))
        self._step.sort()
        self._step_list.append(new_step)

    def check_desc(self, desc):
        if not set(self._step).issubset(set(desc.keys())):
            return False
        return True

    def generate(self):
        data = ''
        for step in self._step_list:
            _ = step.generate()
            data += f'{_}\n'
        return f'flow_run  {self._name}\n {data} flow_run_end'

    def send_echoer(self):
        a = self.generate()
        a = a.replace('"`', '`')
        a = a.replace('`"', '`')
        flow_data = {'data': a}
        print(flow_data['data'])

        with error_suppress(false):
            req = requests.post(self.req_url, json=flow_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('发送echoer错误', req.json())
                return False
