from comware.project import Project
from comware.exception import CfgError

import unittest

class ComwareBoardUtilsTest(unittest.TestCase):
    def test_init_project_error(self):
        with self.assertRaises(CfgError):
            proj = Project({"chassis":1, "slot":2})

if __name__ == "__main__":
    unittest.main(warnings='ignore')
