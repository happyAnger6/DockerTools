from common.utils import execute

import unittest

class CommonUtilsTest(unittest.TestCase):
    def test_normal_execute(self):
        out = execute(["ls"])
        self.assertIsNone(out)
        self.fail("Finish the tests!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')