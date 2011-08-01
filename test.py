from tests import test_browser, test_downloader, test_loader
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromModule(test_browser))
    suite.addTest(loader.loadTestsFromModule(test_downloader))
    suite.addTest(loader.loadTestsFromModule(test_loader))
    unittest.TextTestRunner(verbosity=2).run(suite)

