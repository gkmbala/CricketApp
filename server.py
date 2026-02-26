"""
🏏 Cricket AI Dashboard — Local Backend Server v2
Run: python server.py  →  open http://localhost:5000
"""

import json, os, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

CRICKET_API_KEY = "c********************************************************"  # get your free key from https://www.cricapi.com/ (or use demo mode) 
BASE            = "https://api.cricapi.com/v1"
PORT            = 5000

ENDPOINTS = {
    "/api/live":      lambda p: f"{BASE}/currentMatches?apikey={CRICKET_API_KEY}&offset=0",
    "/api/scores":    lambda p: f"{BASE}/cricScore?apikey={CRICKET_API_KEY}",
    "/api/scorecard": lambda p: f"{BASE}/match_scorecard?apikey={CRICKET_API_KEY}&id={p.get('id',[''])[0]}",
    "/api/match":     lambda p: f"{BASE}/match_info?apikey={CRICKET_API_KEY}&id={p.get('id',[''])[0]}",
    "/api/series":    lambda p: f"{BASE}/series?apikey={CRICKET_API_KEY}&offset=0",
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        status = a[1] if len(a) > 1 else '?'
        symbol = "✅" if str(status).startswith("2") else "❌"
        print(f"  {symbol} [{self.command}] {self.path.split('?')[0]} → {status}")

    def cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200); self.cors(); self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path in ("/", "/index.html"):
            return self.file("dashboard.html", "text/html")

        if parsed.path in ENDPOINTS:
            url = ENDPOINTS[parsed.path](params)
            return self.proxy(url)

        self.json({"error": "Not found"}, 404)

    def proxy(self, url):
        print(f"  🌐 {url[:90]}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CricAI/2.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                raw  = r.read()
                peek = raw[:150].decode(errors="replace")
                print(f"  📦 {peek}")
                self.raw_json(raw)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            print(f"  ❌ HTTP {e.code}: {body[:200]}")
            self.json({"error": f"API HTTP {e.code}", "detail": body[:200]}, e.code)
        except urllib.error.URLError as e:
            print(f"  ❌ URL Error: {e.reason}")
            self.json({"error": str(e.reason)}, 503)
        except Exception as e:
            print(f"  ❌ {e}")
            self.json({"error": str(e)}, 500)

    def json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.cors(); self.end_headers(); self.wfile.write(body)

    def raw_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.cors(); self.end_headers(); self.wfile.write(data)

    def file(self, name, ct):
        fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        if not os.path.exists(fp):
            return self.json({"error": f"{name} not found"}, 404)
        with open(fp, "rb") as f: body = f.read()
        self.send_response(200)
        self.send_header("Content-Type",   ct)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)


if __name__ == "__main__":
    print("\n🔍 Testing API key...")
    try:
        url = f"{BASE}/currentMatches?apikey={CRICKET_API_KEY}&offset=0"
        req = urllib.request.Request(url, headers={"User-Agent":"CricAI/2.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            d     = json.loads(r.read())
            count = len(d.get("data", []))
            print(f"  ✅ Connected! Matches available: {count}")
            # Print match names
            for m in d.get("data", [])[:5]:
                status = "🔴 LIVE" if m.get("matchStarted") and not m.get("matchEnded") else "📅"
                print(f"     {status} {m.get('name','?')}  ID: {m.get('id','?')}")
    except Exception as e:
        print(f"  ⚠️  {e} — demo mode will work in browser")

    server = HTTPServer(("localhost", PORT), Handler)
    print()
    print("╔═══════════════════════════════════════════════╗")
    print("║   🏏  Cricket AI Dashboard v2 — Server       ║")
    print("╠═══════════════════════════════════════════════╣")
    print(f"║   ✅  Open → http://localhost:{PORT}            ║")
    print("║   📡  Endpoints:                              ║")
    print("║       /api/live  /api/scorecard  /api/match  ║")
    print("║   🛑  Ctrl+C to stop                         ║")
    print("╚═══════════════════════════════════════════════╝")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
