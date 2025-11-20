import os
from PIL import Image, ImageTk, ImageSequence
import customtkinter as ctk
from tkinter import filedialog, Toplevel, Label


class Tooltip:
    """Classe simples para tooltips"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(
            tw,
            text=self.text,
            justify="left",
            background="#333333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            padx=5,
            pady=3,
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class ImageAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Config da janela
        self.win_w, self.win_h = 800, 920
        self.geometry(f"{self.win_w}x{self.win_h}")
        self.center_window()
        self.minsize(800, 700)

        self.title("Analisador de Imagens")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variáveis
        self.folder_path = None
        self.tooltips = {}
        self.animations = {}

        # Frame superior (botões)
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.select_btn = ctk.CTkButton(
            button_frame, text="Selecionar Pasta", command=self.select_folder
        )
        self.select_btn.grid(row=0, column=0, padx=10)

        self.analyze_btn = ctk.CTkButton(
            button_frame, text="Iniciar Análise", command=self.analyze_images
        )
        self.analyze_btn.grid(row=0, column=1, padx=10)

        # Frame central para os 4 canvas (grid para centralizar)
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(expand=True, fill="both", pady=20)

        self.canvas_frame.grid_rowconfigure((0, 1), weight=1, uniform="row")
        self.canvas_frame.grid_columnconfigure((0, 1), weight=1, uniform="col")

        self.canvases = {}
        titles = [
            "Maior Largura (X)",
            "Maior Altura (Y)",
            "Menor Largura (X)",
            "Menor Altura (Y)",
        ]

        for i, title in enumerate(titles):
            frame = ctk.CTkFrame(self.canvas_frame)
            frame.grid(row=i // 2, column=i % 2, padx=20, pady=20, sticky="nsew")

            label = ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold"))
            label.pack(pady=5)

            canvas = ctk.CTkCanvas(frame, width=350, height=250, bg="gray20", highlightthickness=0)
            canvas.pack()

            name_label = ctk.CTkLabel(frame, text="", font=("Arial", 12))
            name_label.pack(pady=2)

            size_label = ctk.CTkLabel(frame, text="", font=("Arial", 11))
            size_label.pack(pady=2)

            tie_label = ctk.CTkLabel(
                frame, text="", font=("Arial", 11), text_color="orange", wraplength=330, justify="center"
            )
            tie_label.pack(pady=2)

            self.canvases[title] = {
                "canvas": canvas,
                "name_label": name_label,
                "size_label": size_label,
                "tie_label": tie_label,
                "img": None,
                "frames": [],
                "frame_index": 0,
                "delay": 100,
            }

    def center_window(self):
        """Centraliza a janela na tela"""
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (self.win_w // 2)
        y = (screen_h // 2) - (self.win_h // 2)
        self.geometry(f"{self.win_w}x{self.win_h}+{x}+{y}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder

    def analyze_images(self):
        if not self.folder_path:
            return

        images_info = []
        for file in os.listdir(self.folder_path):
            path = os.path.join(self.folder_path, file)
            if os.path.isfile(path):
                try:
                    with Image.open(path) as img:
                        images_info.append((file, path, img.width, img.height))
                except:
                    pass

        if not images_info:
            return

        def select_image(images, key_index, mode):
            if mode == "max":
                value = max(img[key_index] for img in images)
            else:
                value = min(img[key_index] for img in images)

            filtered = [img for img in images if img[key_index] == value]
            filtered.sort(key=lambda x: x[0].lower())
            chosen = filtered[0]
            ties = len(filtered)
            others = [img[0] for img in filtered if img != chosen]
            return chosen, ties, others

        max_width, tie_wmax, others_wmax = select_image(images_info, 2, "max")
        max_height, tie_hmax, others_hmax = select_image(images_info, 3, "max")
        min_width, tie_wmin, others_wmin = select_image(images_info, 2, "min")
        min_height, tie_hmin, others_hmin = select_image(images_info, 3, "min")

        results = {
            "Maior Largura (X)": (max_width, tie_wmax, others_wmax),
            "Maior Altura (Y)": (max_height, tie_hmax, others_hmax),
            "Menor Largura (X)": (min_width, tie_wmin, others_wmin),
            "Menor Altura (Y)": (min_height, tie_hmin, others_hmin),
        }

        for title, (data, ties, others) in results.items():
            filename, path, w, h = data
            self.show_image(title, path, filename, w, h, ties, others)

    def show_image(self, title, path, filename, w, h, ties, others):
        canvas = self.canvases[title]["canvas"]
        name_label = self.canvases[title]["name_label"]
        size_label = self.canvases[title]["size_label"]
        tie_label = self.canvases[title]["tie_label"]

        # limpar canvas
        canvas.delete("all")

        # carregar imagem
        img = Image.open(path)

        # GIF animado
        if getattr(img, "is_animated", False):
            frames = []
            delays = []
            for frame in ImageSequence.Iterator(img):
                frame_copy = frame.copy()
                frame_copy.thumbnail((350, 250))
                frames.append(ImageTk.PhotoImage(frame_copy))
                delays.append(frame.info.get('duration', 100))

            self.canvases[title]["frames"] = frames
            self.canvases[title]["frame_index"] = 0
            self.canvases[title]["delay"] = delays
            self.animate_gif(title)
        else:
            img.thumbnail((350, 250))
            img_tk = ImageTk.PhotoImage(img)
            self.canvases[title]["img"] = img_tk
            canvas.create_image(175, 125, image=img_tk)

        # atualizar labels
        name_label.configure(text=filename)
        size_label.configure(text=f"{w} x {h} px")

        if title in self.tooltips:
            self.tooltips[title].hide_tip()
            self.tooltips.pop(title)

        if ties > 1:
            tie_label.configure(
                text=f"⚠ Empate: {ties} imagens (passe o mouse para ver lista)"
            )
            if others:
                self.tooltips[title] = Tooltip(tie_label, "\n".join(others))
        else:
            tie_label.configure(text="")

    def animate_gif(self, title):
        canvas = self.canvases[title]["canvas"]
        frames = self.canvases[title]["frames"]
        delays = self.canvases[title]["delay"]
        index = self.canvases[title]["frame_index"]

        canvas.delete("all")  # limpar frame anterior
        frame = frames[index]
        canvas.create_image(175, 125, image=frame)
        self.canvases[title]["frame_index"] = (index + 1) % len(frames)

        self.after(delays[index], self.animate_gif, title)


if __name__ == "__main__":
    app = ImageAnalyzerApp()
    app.mainloop()
