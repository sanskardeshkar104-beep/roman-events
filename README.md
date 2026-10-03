# Roman Events Tracker

A tiny command-line tracker for NASA Roman Space Telescope virtual events.
Add events you hear about, see what's coming, mark them done. No accounts, no setup.

## Usage

```bash
python roman_events.py list
python roman_events.py add "Watch party" 2026-10-20 19:00 https://example.com
python roman_events.py done 1
```

Dates accept `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`. Events are saved in `events.json` next to the script.

## Why

Built as a first GitHub project by a fan of NASA's Roman Space Telescope.
