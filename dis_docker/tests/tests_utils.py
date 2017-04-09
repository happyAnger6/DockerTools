from common.utils import execute

import unittest

class CommonUtilsTest(unittest.TestCase):
    def test_normal_execute(self):
        out, err = execute(["docker","run","--name","test3","ubuntu"], return_stderr=True)
        self.assertIsNotNone(out)
        self.assertIsNone(err)
        self.fail("Finish the tests!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')