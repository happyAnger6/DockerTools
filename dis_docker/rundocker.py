import sys
import os
import re

import argparse
from configparser import ConfigParser

from comware.board import Board

BOARD_NAME_RE=re.compile(r'mpu|lpu', flags=re.I)
BOARD_INFO_NECSSARY=['chassis', 'slot', 'cpu']

parser = argparse.ArgumentParser(description='run a docker')

parser.add_argument('-f','--ini', dest='cfgfile', metavar='cfg filename',
                    action='store', help='speicfy cfg file name',
                    required=True)
args = parser.parse_args()

cfgfile = args.cfgfile
if not os.path.exists(cfgfile):
    print("file:%s not exist!"%cfgfile)

cfg = ConfigParser()
cfg.read(cfgfile)
all_boards=[]
for sec in cfg.sections():
    all_values = {}
    if re.match(BOARD_NAME_RE, sec):
        print("find a board:%s" % sec)
        try:
            for key in BOARD_INFO_NECSSARY:
                all_values[key] = cfg.get(sec, key)
            board = Board(all_values)
            all_boards.append(board)
        except Exception as e:
            print("ERROR parse %s for %s error:%s"%(key,sec,e))
            sys.exit(-1)

for board in all_boards:
    board.show()

