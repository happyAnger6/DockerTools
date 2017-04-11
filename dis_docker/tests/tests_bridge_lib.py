from linux.bridge_lib import get_bridge_names

import unittest

class BridgeLibSupportTest(unittest.TestCase):
    def test_normal_execute(self):
        names = get_bridge_names()
        print(names)
        self.assertIsNotNone(names)

if __name__ == "__main__":
    unittest.main(warnings='ignore')