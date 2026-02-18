import random
import tkinter as tk
from dataclasses import dataclass


@dataclass
class BuddyStyle:
    body_color: str
    eye_color: str
    blush_color: str
    accessory: str
    mood: str


PALETTES = {
    "body": ["#8ecae6", "#ffb4a2", "#bde0fe", "#caffbf", "#ffd6a5", "#f1c0e8"],
    "eyes": ["#1d3557", "#023047", "#2b2d42", "#3a5a40", "#4a4e69"],
    "blush": ["#ffafcc", "#ffc8dd", "#ffcad4", "#f4acb7"],
}

MOODS = ["sleepy", "happy", "curious", "cozy", "goofy"]
ACCESSORIES = ["none", "leaf", "star", "headphones", "beanie"]


class DesktopBuddyApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("On-Screen Buddy")
        self.root.configure(bg="black")

        self.width = 240
        self.height = 260
        self.root.geometry(f"{self.width}x{self.height}+100+100")
        self.root.attributes("-topmost", True)

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#10161f",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.status = tk.Label(
            self.root,
            text="",
            bg="#10161f",
            fg="#e6edf3",
            font=("Arial", 10, "bold"),
        )
        self.status.place(relx=0.5, rely=0.95, anchor="s")

        self.tick = 0
        self.style = self.random_style()
        self.draw_buddy()

        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        self.root.bind("<Double-Button-1>", self.regenerate_buddy)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.offset_x = 0
        self.offset_y = 0
        self.animate()

    @staticmethod
    def random_style() -> BuddyStyle:
        return BuddyStyle(
            body_color=random.choice(PALETTES["body"]),
            eye_color=random.choice(PALETTES["eyes"]),
            blush_color=random.choice(PALETTES["blush"]),
            accessory=random.choice(ACCESSORIES),
            mood=random.choice(MOODS),
        )

    def draw_buddy(self) -> None:
        self.canvas.delete("all")
        self.status.configure(
            text=(
                f"{self.style.mood} buddy • {self.style.accessory}"
                " • double-click for a new friend"
            )
        )

        # Shadow + body
        self.canvas.create_oval(60, 200, 180, 232, fill="#0b1118", outline="")
        self.body = self.canvas.create_oval(
            50, 60, 190, 210, fill=self.style.body_color, outline="#1f2937", width=3
        )

        # Face
        self.left_eye = self.canvas.create_oval(
            87, 110, 102, 126, fill=self.style.eye_color, outline=""
        )
        self.right_eye = self.canvas.create_oval(
            138, 110, 153, 126, fill=self.style.eye_color, outline=""
        )
        self.canvas.create_oval(72, 132, 95, 148, fill=self.style.blush_color, outline="")
        self.canvas.create_oval(145, 132, 168, 148, fill=self.style.blush_color, outline="")

        if self.style.mood == "sleepy":
            self.mouth = self.canvas.create_line(106, 156, 134, 156, fill="#334155", width=3)
        elif self.style.mood == "curious":
            self.mouth = self.canvas.create_oval(114, 150, 126, 164, fill="#334155", outline="")
        elif self.style.mood == "goofy":
            self.mouth = self.canvas.create_arc(
                100,
                145,
                140,
                175,
                start=200,
                extent=140,
                style="arc",
                outline="#334155",
                width=3,
            )
        else:
            self.mouth = self.canvas.create_arc(
                100,
                145,
                140,
                175,
                start=180,
                extent=180,
                style="arc",
                outline="#334155",
                width=3,
            )

        self.draw_accessory()

    def draw_accessory(self) -> None:
        if self.style.accessory == "leaf":
            self.canvas.create_oval(108, 44, 136, 66, fill="#2a9d8f", outline="")
            self.canvas.create_line(120, 52, 120, 72, fill="#1b4332", width=3)
        elif self.style.accessory == "star":
            points = [120, 35, 127, 52, 146, 52, 131, 63, 136, 80, 120, 69, 104, 80, 109, 63, 94, 52, 113, 52]
            self.canvas.create_polygon(points, fill="#ffca3a", outline="#8f6800", width=2)
        elif self.style.accessory == "headphones":
            self.canvas.create_arc(76, 50, 164, 124, start=0, extent=180, outline="#495057", width=6, style="arc")
            self.canvas.create_oval(72, 96, 88, 126, fill="#495057", outline="")
            self.canvas.create_oval(152, 96, 168, 126, fill="#495057", outline="")
        elif self.style.accessory == "beanie":
            self.canvas.create_arc(68, 45, 172, 125, start=0, extent=180, fill="#6c63ff", outline="")
            self.canvas.create_rectangle(75, 80, 165, 102, fill="#5a54d1", outline="")

    def animate(self) -> None:
        self.tick += 1
        bob = (self.tick % 40) - 20
        shift = bob / 20
        self.canvas.move(self.body, 0, 0.2 if shift > 0 else -0.2)
        self.canvas.move(self.left_eye, 0, 0.2 if shift > 0 else -0.2)
        self.canvas.move(self.right_eye, 0, 0.2 if shift > 0 else -0.2)
        self.root.after(90, self.animate)

    def regenerate_buddy(self, _event=None) -> None:
        self.style = self.random_style()
        self.draw_buddy()

    def start_drag(self, event: tk.Event) -> None:
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event: tk.Event) -> None:
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    DesktopBuddyApp().run()
