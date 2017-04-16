from comware.board import Board
from dockercmd import DockerBoardRunCmd, SubProcessBase

import unittest

class DockerCmdUtilsTest(unittest.TestCase):
    def test_run_one_board(self):
        board = Board("mpu-1",{"chassis":1, "slot":2, "cpu":0})
        docker_run_cmd = DockerBoardRunCmd(SubProcessBase())
        docker_run_cmd.execute(board, "ubuntu", env=["SELFNODE=1,0,1", "VETHNAME=veth-0-1-0-b"], entry="/bin/bash")

if __name__ == "__main__":
    unittest.main(warnings='ignore')
