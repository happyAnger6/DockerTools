from .exception import CfgError

class BaseObject:
    def __init__(self, settings):
        self._settings = settings
        self._check_settings()

    def _check_settings(self):
        for k in self.get_neccessary_cfg_key():
            if k not in self._settings.keys():
                raise CfgError()

    def get_neccessary_cfg_key(self):
        return []

    def show(self):
        print(self.__class__,self._settings)
