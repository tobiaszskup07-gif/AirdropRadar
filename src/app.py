from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
from functools import partial

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'announcements.json'
STATIC = ROOT / 'index.html'

def load_announcements():
    raw = json.loads(DATA.read_text(encoding='utf-8'))
    if not isinstance(raw, list):
        raise ValueError('Expected a list')
    return [x for x in raw if isinstance(x, dict) and all(isinstance(x.get(k), str) for k in ('project','chain','status','source_url','summary')) and x['chain'] in ('Solana','Ethereum','Base') and x['source_url'].startswith('https://')]

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/announcements':
            body = json.dumps({'data':load_announcements()}).encode()
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.getenv('PORT','8000'))),partial(Handler,directory=str(ROOT))).serve_forever()
