import unittest
from src.app import load_announcements, STATIC
class AppTests(unittest.TestCase):
    def test_data(self):
        self.assertIsInstance(load_announcements(),list)
    def test_dashboard(self):
        self.assertTrue(STATIC.is_file())
if __name__ == '__main__':
    unittest.main()
