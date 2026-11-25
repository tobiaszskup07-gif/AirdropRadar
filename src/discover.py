"""Collect candidate announcements, never automatically verify eligibility."""
import json, re, urllib.request, urllib.error, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent.parent
SOURCES=[("Ethereum Foundation","Ethereum","https://blog.ethereum.org/en/feed.xml"),("Solana","Solana","https://solana.com/news/rss.xml"),("Curve Finance","Ethereum","https://blog.curve.fi/feed"),("Synthetix","Ethereum","https://blog.synthetix.io/rss/"),("Optimism","Ethereum","https://dev.optimism.io/rss/")]
def parse(raw, project, chain, feed):
    root=ET.fromstring(raw)
    rows=[]
    for item in root.findall(".//item")+root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        def field(name):
            return item.find(name) if item.find(name) is not None else item.find("{http://www.w3.org/2005/Atom}"+name)
        t=field("title"); l=field("link")
        if t is None or l is None: continue
        title="".join(t.itertext()).strip()
        link=l.get("href") or l.text or ""
        if not re.search(r"\bairdrops?\b|\btoken claims?\b|\bclaim eligibility\b",title,re.I): continue
        u=urlparse(link)
        if u.scheme!="https" or u.hostname!=urlparse(feed).hostname: continue
        rows.append(dict(project=project,chain=chain,status="Needs review",source_url=link,summary=title,eligibility="Not verified",deadline=None))
    return rows
def main():
    path=ROOT/"data"/"candidates.json"
    old=json.loads(path.read_text()) if path.exists() else []
    rows={x["source_url"]:x for x in old}
    success=0
    health=[]
    for project,chain,feed in SOURCES:
        try:
            req=urllib.request.Request(feed,headers={"User-Agent":"AirdropRadar/0.2"})
            with urllib.request.urlopen(req,timeout=20) as response:
                if urlparse(response.geturl()).hostname!=urlparse(feed).hostname: raise ValueError("Unexpected redirect")
                raw=response.read(2_000_001)
            if len(raw)>2_000_000: raise ValueError("Feed too large")
            for x in parse(raw,project,chain,feed): rows[x["source_url"]]=x
            success+=1
            health.append({"project":project,"status":"ok"})
            print(f"{project}: feed parsed successfully")
        except urllib.error.HTTPError as e:
            health.append({"project":project,"status":"rate limited" if e.code==429 else "HTTP "+str(e.code)})
            print(f"{project}: {e}")
        except Exception as e:
            health.append({"project":project,"status":"failed"})
            print(f"{project}: {e}")
    print(f"Sources successful: {success}/{len(SOURCES)}; stored candidates: {len(rows)}")
    (ROOT/"data"/"health.json").write_text(json.dumps(health,indent=2)+"\n")
    if not success: raise SystemExit("All sources failed")
    path.write_text(json.dumps(list(rows.values())[-500:],indent=2)+"\n")
if __name__=="__main__": main()
