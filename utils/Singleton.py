class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class ZOmato_API_Factory(Borg):
    def __init__(self):
        Borg.__init__(self)
