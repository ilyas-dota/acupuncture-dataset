#!/usr/bin/env python3
"""Fast search server for acupuncture dataset."""
import json, os, glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

CHUNKS = "/root/acupuncture-dataset/data/chunks"
TUNG = "/root/acupuncture-dataset/data/tung-points.json"
DAO_MA = "/root/acupuncture-dataset/data/dao-ma.json"

# Preload all chunks into memory
INDEX = []
print("Loading chunks...", end=" ")
for f in glob.glob(f"{CHUNKS}/**/*.json", recursive=True):
    try:
        with open(f) as fp:
            c = json.load(fp)
        txt = (c.get("text", "") + " " + c.get("text_ru", "")).lower()[:2000]
        INDEX.append({"source": c.get("source",""), "title": c.get("title",""),
                      "text": c.get("text_ru","") or c.get("text",""),
                      "cat": f.split("/")[-2], "key": txt})
    except:
        pass
print(f"{len(INDEX)} chunks loaded")

class H(BaseHTTPRequestHandler):
    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_GET(self):
        p = urlparse(self.path)
        q = parse_qs(p.query)

        if p.path == "/search":
            query = q.get("q", [""])[0].lower()
            cat = q.get("cat", [None])[0]
            limit = int(q.get("limit", [5])[0])
            if not query:
                self._json({"error": "missing q"})
                return
            results = []
            for c in INDEX:
                if cat and c["cat"] != cat:
                    continue
                if query in c["key"]:
                    results.append({"source": c["source"], "title": c["title"],
                                    "text": c["text"][:800], "category": c["cat"]})
                    if len(results) >= limit:
                        break
            self._json({"results": results, "total": len(results)})

        elif p.path == "/point":
            pid = q.get("id", [""])[0]
            if os.path.exists(TUNG):
                with open(TUNG) as f:
                    for pt in json.load(f):
                        if pt.get("id") == pid:
                            self._json(pt); return
            self._json({"error": "not found"})

        elif p.path == "/daoma":
            if os.path.exists(DAO_MA):
                with open(DAO_MA) as f:
                    self._json(json.load(f))
            else:
                self._json([])

        elif p.path == "/health":
            self._json({"ok": True, "chunks": len(INDEX)})
        else:
            self._json({"error": "not found"})

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 3467), H).serve_forever()
