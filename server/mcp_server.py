#!/usr/bin/env python3
"""MCP server for acupuncture dataset — search across 9,900 chunks."""
import json, os, sys, glob

CHUNKS = "/root/acupuncture-dataset/data/chunks"
INDEX = None  # lazy load

def load_index():
    global INDEX
    if INDEX is not None:
        return
    INDEX = []
    for f in glob.glob(f"{CHUNKS}/**/*.json", recursive=True):
        try:
            with open(f) as fp:
                c = json.load(fp)
            txt = (c.get("text", "") + " " + c.get("text_ru", "")).lower()[:2000]
            INDEX.append({
                "source": c.get("source", ""),
                "title": c.get("title", ""),
                "text": c.get("text_ru", "") or c.get("text", ""),
                "cat": f.split("/")[-2],
                "key": txt
            })
        except:
            pass

def search(query, category=None, limit=5):
    load_index()
    q = query.lower()
    results = []
    for c in INDEX:
        if category and c["cat"] != category:
            continue
        if q in c["key"]:
            results.append(c)
            if len(results) >= limit:
                break
    return results

# MCP protocol via stdin/stdout
def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def recv():
    line = sys.stdin.readline()
    return json.loads(line) if line else None

# Initialize
send({"jsonrpc": "2.0", "method": "initialized"})

while True:
    msg = recv()
    if not msg:
        break
    
    method = msg.get("method", "")
    id = msg.get("id")
    
    if method == "tools/list":
        send({
            "jsonrpc": "2.0", "id": id,
            "result": {
                "tools": [
                    {
                        "name": "search",
                        "description": "Search acupuncture knowledge base by symptom or point name. Returns relevant chunks from 162 books.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Symptom, condition or point name (e.g. headache, migraine, 11.01)"},
                                "category": {"type": "string", "enum": ["tung", "tcm", "waa", "jin", "ear", "manual", "psyche", "general"], "description": "Optional category filter"},
                                "limit": {"type": "integer", "default": 5}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_stats",
                        "description": "Get dataset statistics",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        })
    
    elif method == "tools/call":
        tool = msg.get("params", {}).get("name", "")
        args = msg.get("params", {}).get("arguments", {})
        
        if tool == "search":
            results = search(args.get("query", ""), args.get("category"), args.get("limit", 5))
            text = "Nothing found."
            if results:
                parts = []
                for r in results:
                    parts.append(f"📖 {r['source']} — {r['title']}\n{r['text'][:600]}")
                text = "\n\n---\n\n".join(parts)
            send({
                "jsonrpc": "2.0", "id": id,
                "result": {"content": [{"type": "text", "text": text}]}
            })
        
        elif tool == "get_stats":
            send({
                "jsonrpc": "2.0", "id": id,
                "result": {"content": [{"type": "text", "text": json.dumps({"chunks": len(INDEX)}, indent=2)}]}
            })
    
    elif method == "initialize":
        send({
            "jsonrpc": "2.0", "id": id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "acupuncture", "version": "1.0.0"},
                "capabilities": {"tools": {}}
            }
        })
