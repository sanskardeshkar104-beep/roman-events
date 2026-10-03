#!/usr/bin/env python3
"""Roman Events Tracker
A tiny command-line tracker for NASA Roman Space Telescope virtual events.
Keep it simple: add events you hear about, list what's coming.

Usage:
  python roman_events.py list
  python roman_events.py add "Watch party" 2026-10-20 19:00 https://example.com
  python roman_events.py done 1
"""
import json
import sys
from datetime import datetime, date
from pathlib import Path

EVENTS_FILE = Path(__file__).parent / "events.json"


def load_events():
    if EVENTS_FILE.exists():
        return json.loads(EVENTS_FILE.read_text())
    return []


def save_events(events):
    EVENTS_FILE.write_text(json.dumps(events, indent=2))


def parse_when(when_str):
    """Accepts 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'."""
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(when_str, fmt)
        except ValueError:
            continue
    raise SystemExit(f"Could not read date '{when_str}'. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")


def cmd_list():
    events = load_events()
    if not events:
        print("No events yet. Add one with:")
        print('  python roman_events.py add "Event name" 2026-10-20 19:00 https://...')
        return
    today = date.today()
    upcoming = sorted((e for e in events if not e["done"]), key=lambda e: e["when"])
    if not upcoming:
        print("All caught up, every event is marked done.")
        return
    for i, e in enumerate(upcoming, 1):
        when = datetime.fromisoformat(e["when"])
        days = (when.date() - today).days
        countdown = "today!" if days == 0 else f"in {days} day(s)"
        when_text = when.strftime("%d %b %Y, %H:%M") if when.hour else when.strftime("%d %b %Y")
        print(f"{i}. {e['title']}")
        print(f"   {when_text} ({countdown})")
        if e.get("url"):
            print(f"   {e['url']}")


def cmd_add(title, when_str, url=""):
    events = load_events()
    events.append({
        "title": title,
        "when": parse_when(when_str).isoformat(),
        "url": url,
        "done": False,
    })
    save_events(events)
    print(f"Added: {title}")


def cmd_done(num):
    events = load_events()
    upcoming = sorted((e for e in events if not e["done"]), key=lambda e: e["when"])
    try:
        upcoming[num - 1]["done"] = True
    except IndexError:
        raise SystemExit(f"No event number {num} on the upcoming list.")
    save_events(events)
    print(f"Marked done: {upcoming[num - 1]['title']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_list()
    elif sys.argv[1] == "list":
        cmd_list()
    elif sys.argv[1] == "add" and len(sys.argv) >= 4:
        cmd_add(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif sys.argv[1] == "done" and len(sys.argv) >= 3:
        cmd_done(int(sys.argv[2]))
    else:
        print(__doc__)
