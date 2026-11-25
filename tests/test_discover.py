import unittest
from src.discover import parse
class DiscoveryTests(unittest.TestCase):
    def test_candidate(self):
        raw=b'<rss><channel><item><title>Token airdrop</title><link>https://example.org/news</link></item><item><title>Other news</title><link>https://example.org/other</link></item><item><title>Airdrop</title><link>https://evil.example/news</link></item></channel></rss>'
        rows=parse(raw,"Example","Base","https://example.org/feed")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["status"],"Needs review")
