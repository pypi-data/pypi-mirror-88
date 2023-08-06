#Copyright STACKEO - INRIA 2020 .
class Link:
    def __init__(self, source: str, sink: str, layer: str,secure=False):
        self.source = source
        self.sink = sink
        self.layer = layer
        self.secure = secure

    def set_secure(self, secure: bool) -> None:
        self.secure = secure

    def is_internal(self, tier_src: str, tier_sink: str) -> bool:
        if tier_sink == tier_src:
            return True
        return False
