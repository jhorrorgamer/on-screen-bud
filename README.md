# On-Screen Buddy

A tiny fantasy desktop buddy that roams around your screen like an animated pixel sprite.

## Why this update?

To reduce GitHub merge conflicts, the app logic now lives in `buddy_sprite.py` and `buddy_app.py` is only a tiny entrypoint.

## Features

- No window chrome (`overrideredirect`) so it behaves like a floating animated PNG.
- Small icon-like size (64×64 px) with pixel art rendering.
- Uses transparent background where supported, with an automatic dark fallback on unsupported platforms.
- Auto-roaming movement that bounces around the edges of your desktop.
- Random fantasy/medieval classes: knight, wizard, ranger.
- Double-click to spawn a new random buddy.
- Right-click or press `Esc` to close.

## Run

```bash
python3 buddy_app.py
```
