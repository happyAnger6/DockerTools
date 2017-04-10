from comware.board import Board
from comware.exception import CfgError

import unittest

class ComwareBoardUtilsTest(unittest.TestCase):
    def test_init_board_error(self):
        with self.assertRaises(CfgError):
            board = Board({"chassis":1, "slot":2})

if __name__ == "__main__":
    unittest.main(warnings='ignore')
