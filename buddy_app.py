import random
import tkinter as tk
from dataclasses import dataclass


SCALE = 4
GRID = 16
SIZE = GRID * SCALE
TRANSPARENT = "#ff00ff"


@dataclass
class BuddyStyle:
    role: str
    cloak: str
    armor: str
    trim: str
    skin: str


ROLES = ["knight", "wizard", "ranger"]
SKIN_TONES = ["#f2d3b1", "#e6bc90", "#d39a72", "#b57a56"]

ROLE_PALETTES = {
    "knight": {
        "cloak": ["#4a6fa5", "#6c5b7b"],
        "armor": ["#9aa0a8", "#b8bec6"],
        "trim": ["#f4d35e", "#ffd166"],
    },
    "wizard": {
        "cloak": ["#593196", "#3b2f7f"],
        "armor": ["#7a6f9b", "#8a82b7"],
        "trim": ["#7fe7dc", "#9bf6ff"],
    },
    "ranger": {
        "cloak": ["#356859", "#4f772d"],
        "armor": ["#7c6a58", "#927e6a"],
        "trim": ["#dda15e", "#e9c46a"],
    },
}


class DesktopBuddyApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.config(bg=TRANSPARENT)
        self.root.wm_attributes("-topmost", True)

        try:
            self.root.wm_attributes("-transparentcolor", TRANSPARENT)
        except tk.TclError:
            # Transparent color is not supported on every platform.
            pass

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        start_x = random.randint(0, max(0, self.screen_w - SIZE))
        start_y = random.randint(0, max(0, self.screen_h - SIZE))
        self.root.geometry(f"{SIZE}x{SIZE}+{start_x}+{start_y}")

        self.canvas = tk.Canvas(
            self.root,
            width=SIZE,
            height=SIZE,
            bg=TRANSPARENT,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.style = self.random_style()
        self.frame = 0
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.step_timer = 0

        self.root.bind("<Double-Button-1>", self.new_buddy)
        self.root.bind("<Button-3>", lambda _e: self.root.destroy())
        self.root.bind("<Escape>", lambda _e: self.root.destroy())

        self.draw_buddy(foot_offset=0)
        self.tick()

    @staticmethod
    def random_style() -> BuddyStyle:
        role = random.choice(ROLES)
        role_colors = ROLE_PALETTES[role]
        return BuddyStyle(
            role=role,
            cloak=random.choice(role_colors["cloak"]),
            armor=random.choice(role_colors["armor"]),
            trim=random.choice(role_colors["trim"]),
            skin=random.choice(SKIN_TONES),
        )

    def px(self, x: int, y: int, color: str) -> None:
        self.canvas.create_rectangle(
            x * SCALE,
            y * SCALE,
            (x + 1) * SCALE,
            (y + 1) * SCALE,
            fill=color,
            outline=color,
        )

    def draw_buddy(self, foot_offset: int) -> None:
        self.canvas.delete("all")

        for x in range(5, 11):
            self.px(x, 15, "#000000")

        for x in range(6, 10):
            self.px(x, 14, self.style.cloak)

        helmet_y = 4 if self.style.role != "wizard" else 3
        for x in range(5, 11):
            self.px(x, helmet_y, self.style.armor)
        for x in range(4, 12):
            self.px(x, helmet_y + 1, self.style.armor)

        if self.style.role == "wizard":
            for i, span in enumerate([1, 3, 5]):
                row = 2 - i
                for x in range(8 - span // 2, 8 + span // 2 + 1):
                    self.px(x, row, self.style.cloak)
            self.px(8, 3, self.style.trim)

        for y in range(6, 9):
            for x in range(5, 11):
                self.px(x, y, self.style.skin)

        self.px(6, 7, "#1b1b1b")
        self.px(9, 7, "#1b1b1b")

        for y in range(9, 13):
            for x in range(5, 11):
                self.px(x, y, self.style.cloak)

        for y in range(10, 12):
            self.px(4, y, self.style.armor)
            self.px(11, y, self.style.armor)

        self.px(7, 11, self.style.trim)
        self.px(8, 11, self.style.trim)

        if self.style.role == "knight":
            for y in range(9, 13):
                self.px(12, y, "#c0c7cf")
            self.px(12, 8, "#ffd166")
        elif self.style.role == "wizard":
            for y in range(9, 12):
                self.px(12, y, "#8b5e34")
            self.px(12, 8, "#7fe7dc")
            self.px(12, 7, "#9bf6ff")
        else:
            self.px(12, 9, "#8b5e34")
            self.px(12, 10, "#8b5e34")
            self.px(13, 10, "#8b5e34")
            self.px(13, 11, "#8b5e34")

        left_foot = 13 + foot_offset
        right_foot = 13 - foot_offset
        self.px(6, left_foot, "#2b2d42")
        self.px(7, left_foot, "#2b2d42")
        self.px(8, right_foot, "#2b2d42")
        self.px(9, right_foot, "#2b2d42")

    def move_window(self) -> None:
        x = self.root.winfo_x() + self.vx
        y = self.root.winfo_y() + self.vy

        if x <= 0 or x >= self.screen_w - SIZE:
            self.vx *= -1
            x = max(0, min(x, self.screen_w - SIZE))
            self.style = self.random_style()

        if y <= 0 or y >= self.screen_h - SIZE:
            self.vy *= -1
            y = max(0, min(y, self.screen_h - SIZE))

        if random.random() < 0.02:
            self.vx += random.choice([-1, 1])
            self.vy += random.choice([-1, 1])
            self.vx = max(-3, min(3, self.vx))
            self.vy = max(-3, min(3, self.vy))
            if self.vx == 0:
                self.vx = 1
            if self.vy == 0:
                self.vy = -1

        self.root.geometry(f"+{x}+{y}")

    def new_buddy(self, _event=None) -> None:
        self.style = self.random_style()
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def tick(self) -> None:
        self.move_window()
        self.step_timer = (self.step_timer + 1) % 12
        foot_offset = 1 if self.step_timer < 6 else 0
        self.draw_buddy(foot_offset=foot_offset)
        self.root.after(80, self.tick)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    DesktopBuddyApp().run()
