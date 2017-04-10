import sys
import os
import re

import argparse
from configparser import ConfigParser

from comware.board import Board
from comware.project import Project

BOARD_NAME_RE=re.compile(r'mpu|lpu', flags=re.I)

PROJECT_INFO_RE=re.compile(r'project', flags=re.I)

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
        try:
            for k in cfg.options(sec):
                all_values[k] = cfg.get(sec, k)
            board = Board(all_values)
            all_boards.append(board)
        except Exception as e:
            print("ERROR parse %s for %s error:%s" % (key, sec, e))
            sys.exit(-1)
    elif re.match(PROJECT_INFO_RE, sec):
        for k in cfg.options(sec):
            all_values[k] = cfg.get(sec, k)
        proj = Project(all_values)
    else:
        print("find a unkown sectoin:%s"%sec)

for board in all_boards:
    board.show()

proj.show()

