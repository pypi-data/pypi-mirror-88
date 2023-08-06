#Copyright STACKEO - INRIA 2020 .
import sys
import io


class GraphvizManger:

    def __init__(self):
        self.initial_stderr = sys.stderr
        self.redirected_error = sys.stderr = io.StringIO()

    def __enter__(self):
        return self.redirected_error.getvalue()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stderr = self.initial_stderr
