"""Local announcement validation and querying; no wallet access."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

def validate(record):
    if not isinstance(record, dict):
        raise ValueError("Expected object")
    for key in ("project","chain","status","source_url","summary"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError("Missing or invalid "+key)
    url = urlsplit(record["source_url"])
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("Expected HTTPS source without credentials")
    return dict(record)

def query(records, chain=None, status=None):
    return [r for r in map(validate, records)
            if (chain is None or r["chain"].casefold()==chain.casefold())
            and (status is None or r["status"].casefold()==status.casefold())]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file",type=Path)
    parser.add_argument("--chain")
    parser.add_argument("--status")
    args=parser.parse_args()
    records=json.loads(args.file.read_text(encoding="utf-8"))
    if not isinstance(records,list):
        parser.error("Expected JSON array")
    print(json.dumps(query(records,args.chain,args.status),indent=2))
