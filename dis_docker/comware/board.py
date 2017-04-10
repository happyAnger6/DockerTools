from . import BaseObject
from .exception import CfgError

class Board(BaseObject):
    BOARD_INFO_NECESSARY=['chassis', 'slot', 'cpu']

    def get_neccessary_cfg_key(self):
        return self.BOARD_INFO_NECESSARY



