import unittest
from airdropkit import validate, query

class SDKTests(unittest.TestCase):
    def setUp(self):
        self.row=dict(project="Example",chain="Base",status="Needs review",source_url="https://example.org",summary="Test fixture")
    def test_filter(self):
        self.assertEqual(query([self.row],chain="base"),[self.row])
        self.assertEqual(query([self.row],status="Active"),[])
    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            validate(dict(self.row,source_url="javascript:alert(1)"))
    def test_missing(self):
        with self.assertRaises(ValueError):
            validate({})
