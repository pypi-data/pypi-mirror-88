
from contextlib import ContextDecorator


class error_suppress(ContextDecorator):

    def __init__(self, error_func,):
        self.error_msg = error_func

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.error_msg()
