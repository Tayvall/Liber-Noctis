#!/usr/bin/env python3
"""Turn the public website (GitHub Pages) on or off. Run it once to toggle.

  ./DevTools/pages.py          on -> off, or off -> on (and publishes main)

Needs the GitHub CLI logged in (gh auth login).
"""
import subprocess, sys

REPO = "Tayvall/Liber-Noctis"
API = f"repos/{REPO}/pages"


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True)


def main():
    status = gh("api", API)
    if status.returncode == 0:
        r = gh("api", "-X", "DELETE", API)
        if r.returncode: sys.exit(f"Couldn't turn the site off:\n{r.stderr}")
        print("Website is OFF.")
    elif "404" in status.stderr or "Not Found" in status.stderr:
        r = gh("api", "-X", "POST", API, "-f", "build_type=workflow")
        if r.returncode: sys.exit(f"Couldn't turn the site on:\n{r.stderr}")
        # turning Pages on doesn't build anything; the Action has to run on main
        r = gh("workflow", "run", "pages.yml", "--repo", REPO, "--ref", "main")
        if r.returncode: sys.exit(f"Site is on, but the build didn't start:\n{r.stderr}")
        print(f"Website is ON. Building now (1-2 min): https://tayvall.github.io/Liber-Noctis/\n"
              f"Watch it with: gh run watch --repo {REPO}")
    else:
        sys.exit(f"Couldn't check the site (is gh logged in?):\n{status.stderr}")


if __name__ == "__main__":
    main()
