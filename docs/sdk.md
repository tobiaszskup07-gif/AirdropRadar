# Python SDK preview

Install from a local checkout with `python -m pip install .` (not yet published to PyPI).

```python
from airdropkit import query
import json
with open("data/announcements.json") as f:
    rows = query(json.load(f), chain="Solana", status="Needs review")
```

CLI: `airdropkit data/announcements.json --chain Solana`.

Validation checks schema and HTTPS URL syntax only. It does not certify authenticity or eligibility. No wallet access is needed.
