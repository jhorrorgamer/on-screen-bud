# On-Screen Buddy

A tiny fantasy desktop buddy that roams around your screen like an animated pixel sprite.

## Merge-conflict fix

If you previously saw GitHub conflict markers in `README.md` and `buddy_app.py`, this branch resolves that by:

- Keeping `buddy_app.py` as a **small stable entrypoint**.
- Moving runtime logic to `buddy_sprite.py`.
- Keeping README concise and current.

## Features

- No window chrome (`overrideredirect`) so it behaves like a floating animated PNG.
- Small icon-like size (64×64 px) with pixel-art rendering.
- Transparent background where supported, with automatic dark fallback otherwise.
- Auto-roaming movement that bounces around the desktop edges.
- Fantasy/medieval classes: knight, wizard, ranger.
- Double-click to regenerate, right-click or `Esc` to quit.

## Run

```bash
python3 buddy_app.py
```
