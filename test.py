import unittest

from pybrowscap.test.loader import test_downloader
from pybrowscap.test.loader.csv import test_loader, test_browser


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromModule(test_browser))
    suite.addTest(loader.loadTestsFromModule(test_downloader))
    suite.addTest(loader.loadTestsFromModule(test_loader))
    unittest.TextTestRunner(verbosity=2).run(suite)