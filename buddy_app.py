"""Entry point for the desktop buddy app.

Keeping this file intentionally tiny reduces merge conflicts in PR workflows.
"""

from buddy_sprite import DesktopBuddyApp


if __name__ == "__main__":
    DesktopBuddyApp().run()
