"""Stable entrypoint for On-Screen Buddy.

This file is intentionally tiny so merge operations stay conflict-free.
All implementation details live in ``buddy_sprite.py``.
"""

from buddy_sprite import DesktopBuddyApp


def main() -> None:
    DesktopBuddyApp().run()


if __name__ == "__main__":
    main()
