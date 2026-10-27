#!/usr/bin/env python3
"""Witch's Handbook: opens the page in your browser and saves recipes to recipes.json.

  ./handbook.py          start on port 8765 and open the browser
  ./handbook.py 9000     use another port
Stop it with Ctrl+C. recipes.json can be edited by hand at any time; the previous
version is kept as recipes.json.bak on every save.
"""
import http.server, json, os, shutil, sys, webbrowser
from pathlib import Path

DIR = Path(__file__).resolve().parent
DATA = DIR / "recipes.json"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
URL = f"http://localhost:{PORT}/"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(DIR), **k)

    def host_ok(self):
        # blocks DNS-rebinding sites from reaching the server through another hostname
        return self.headers.get("Host", "").split(":")[0] in ("localhost", "127.0.0.1")

    def do_GET(self):
        if not self.host_ok() or self.path.split("?")[0] not in ("/", "/index.html", "/recipes.json"):
            return self.send_error(404)
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_PUT(self):
        if not self.host_ok() or self.path != "/recipes.json":
            return self.send_error(404)
        n = int(self.headers.get("Content-Length", 0))
        if n > 5_000_000:
            return self.send_error(413, "Too large")
        try:
            data = json.loads(self.rfile.read(n))
        except ValueError:
            return self.send_error(400, "Not valid JSON")
        if not (isinstance(data, list) and all(isinstance(r, dict) and isinstance(r.get("name"), str) for r in data)):
            return self.send_error(400, "Expected a list of recipes, each with a name")
        if DATA.exists():
            shutil.copy2(DATA, DATA.with_suffix(".json.bak"))
        tmp = DATA.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(tmp, DATA)  # atomic, so a crash mid-save never leaves a half-written file
        self.send_response(204)
        self.end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not DATA.exists():
        DATA.write_text("[]\n", encoding="utf-8")
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"Already running? Opening {URL}")
        webbrowser.open(URL)
        sys.exit()
    print(f"Witch's Handbook open at {URL}  (Ctrl+C to stop)")
    webbrowser.open(URL)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
