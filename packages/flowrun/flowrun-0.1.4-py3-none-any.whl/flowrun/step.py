class Step:

    def __init__(self, name, action):
        self._flow = None
        self._str_args = None
        self._desc = None

        self._name = name
        self._action = action

    def flow_return(self, step, args=None):
        flow = ''
        for key in step.keys():
            if flow:
                flow += ' | '
            flow += f'{key}->{step[key]}'

        str_args = ''
        if isinstance(args, dict):
            for key in args.keys():
                if str_args:
                    str_args += ','
                value = f'{args[key]}' if isinstance(args[key], int) else f'"{args[key]}"'
                str_args += f'{key}={value}'

        self._flow = flow
        self._str_args = str_args
        self._desc = list(step.values())
        return [self._name]

    def generate(self):
        _ = f'step {self._name} => ({self._flow}) {{action = "{self._action}"; args = ({self._str_args});}};'

        return _
