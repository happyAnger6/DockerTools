from linux.ip_link_support import IpLinkSupport

import unittest

class IpLinkSupportTest(unittest.TestCase):
    def test_normal_execute(self):
        _stdout = IpLinkSupport._get_ip_link_output()
        print(_stdout)
        self.assertIsNotNone(_stdout)

if __name__ == "__main__":
    unittest.main(warnings='ignore')