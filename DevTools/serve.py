#!/usr/bin/env python3
"""Open or close a local preview of the book. Run it once to start, run it again to stop.

  python DevTools/serve.py          toggle the preview on port 8000
  python DevTools/serve.py 9000     use another port

The server listens on 127.0.0.1 only, so nothing outside this computer can reach it.
"""
import os, signal, socket, subprocess, sys, tempfile, time, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIDFILE = Path(tempfile.gettempdir()) / "liber-noctis-serve.pid"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


def running():
    """Returns (pid, port) of our server if it is still alive, else None."""
    try:
        pid, port = map(int, PIDFILE.read_text().split())
        os.kill(pid, 0)
    except (OSError, ValueError):
        return None
    # shortcut: the cmdline check needs Linux's /proc; elsewhere a reused pid is trusted
    cmd = Path(f"/proc/{pid}/cmdline")
    if cmd.exists() and b"http.server" not in cmd.read_bytes():
        return None
    return pid, port


def port_free(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def stop(pid, port):
    os.kill(pid, signal.SIGTERM)
    PIDFILE.unlink(missing_ok=True)
    print(f"Stopped the preview on port {port}.")


def start():
    if not port_free(PORT):
        sys.exit(f"Port {PORT} is already in use by something else. Try: python DevTools/serve.py {PORT + 1}")
    sys.path.insert(0, str(ROOT / ".github" / "scripts"))
    import check
    errors = check.check()[0]
    for m in errors: print("✗", m)
    if errors: print(f"{len(errors)} problem(s) in the data: the book may not open until they're fixed.\n")
    # a leftover bundle would hide your edits; without it the page reads data/ directly
    (ROOT / "data" / "bundle.json").unlink(missing_ok=True)
    proc = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", str(ROOT)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(0.5)
    if proc.poll() is not None:
        sys.exit("The server didn't start.")
    PIDFILE.write_text(f"{proc.pid} {PORT}")
    url = f"http://localhost:{PORT}/"
    print(f"Preview open at {url}\nRun this script again to stop it.")
    webbrowser.open(url)


if __name__ == "__main__":
    alive = running()
    stop(*alive) if alive else start()
