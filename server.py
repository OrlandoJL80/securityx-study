#!/usr/bin/env python3
"""Study server: serves the deck and keeps one progress file per account.

Run from this folder:
    python server.py
Then open http://127.0.0.1:8080 on every machine that should share accounts.
A reboot does not clear data/accounts.json.
"""
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "accounts.json"
PIN = "CAS005"
ACCOUNTS = [
    "Orlando", "Scott", "Daniel", "Donald", "Leslie",
    "Jaye", "Kelly", "Albert", "Johnny", "Mark", "Kevin",
]
LOCK = threading.Lock()
PORT = 8080


def load_all():
    if not DATA.exists():
        return {}
    try:
        return json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_all(blob):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(blob, indent=2), encoding="utf-8")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/progress":
            name = (parse_qs(parsed.query).get("name") or [""])[0]
            if name not in ACCOUNTS:
                self._json(404, {"error": "unknown account"})
                return
            with LOCK:
                blob = load_all()
            rec = blob.get(name) or {"history": {}}
            self._json(200, {"name": name, "history": rec.get("history") or {}})
            return
        if parsed.path == "/api/accounts":
            self._json(200, {"accounts": ACCOUNTS})
            return
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/progress":
            self._json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "bad json"})
            return
        name = body.get("name") or ""
        if name not in ACCOUNTS or body.get("pin") != PIN:
            self._json(403, {"error": "denied"})
            return
        history = body.get("history") if isinstance(body.get("history"), dict) else {}
        with LOCK:
            blob = load_all()
            blob[name] = {"history": history}
            save_all(blob)
        self._json(200, {"ok": True, "name": name})

    def _json(self, code, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith("GET /api"):
            return
        super().log_message(fmt, *args)


if __name__ == "__main__":
    DATA.parent.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        save_all({})
    print(f"SecurityX study server on http://127.0.0.1:{PORT}")
    print("Accounts:", ", ".join(ACCOUNTS))
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
