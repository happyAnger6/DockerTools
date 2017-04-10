from . import BaseObject

class Project(BaseObject):
    PROJECT_INFO_NECESSARY=['name', 'master']

    def get_neccessary_cfg_key(self):
        return self.PROJECT_INFO_NECESSARY
