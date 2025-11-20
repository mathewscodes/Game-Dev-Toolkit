import os
import threading
from PIL import Image, ImageSequence
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuração inicial
nova_largura, nova_altura = 250, 210


# Função para redimensionar os GIFs (em thread separada)
def redimensionar_gifs(input_folder):
    if not input_folder:
        messagebox.showwarning("Aviso", "Selecione uma pasta primeiro.")
        return

    output_folder = os.path.join(input_folder, "redimensionados")
    os.makedirs(output_folder, exist_ok=True)

    gifs = [f for f in os.listdir(input_folder) if f.lower().endswith('.gif')]
    total = len(gifs)

    if total == 0:
        messagebox.showwarning("Aviso", "Nenhum GIF encontrado na pasta.")
        return

    for i, filename in enumerate(gifs, start=1):
        image_path = os.path.join(input_folder, filename)

        with Image.open(image_path) as img:
            frames = []
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA")

                # Criar nova tela (canvas)
                new_frame = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))

                # Centralizar GIF
                x_offset = (nova_largura - img.width) // 2
                y_offset = (nova_altura - img.height) // 2
                new_frame.paste(frame, (x_offset, y_offset), frame)

                frames.append(new_frame)

            # Salvar novo GIF
            output_path = os.path.join(output_folder, filename)
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=img.info.get('duration', 100),
                loop=img.info.get('loop', 0),
                disposal=2
            )

        # Atualizar barra de progresso e label
        progresso = i / total
        progress_bar.set(progresso)
        progress_label.configure(
            text=f"Processando {i}/{total}  ({int(progresso*100)}%)"
        )
        root.update_idletasks()

    messagebox.showinfo("Concluído", f"Processo finalizado!\nArquivos salvos em:\n{output_folder}")
    progress_bar.set(0)
    progress_label.configure(text="Aguardando...")  # Reseta texto


# Funções da interface
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_var.set(pasta)


def iniciar_processamento():
    # Rodar em thread separada para não travar a interface
    thread = threading.Thread(target=redimensionar_gifs, args=(pasta_var.get(),))
    thread.start()


# Configuração da Janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Redimensionador de GIFs")

# Centralizar janela
largura = 500
altura = 280
pos_x = (root.winfo_screenwidth() // 2) - (largura // 2)
pos_y = (root.winfo_screenheight() // 2) - (altura // 2)
root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

# Variável da pasta
pasta_var = ctk.StringVar()

# Widgets
frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Selecione a pasta com os arquivos GIF:")
label.pack(pady=10)

entry = ctk.CTkEntry(frame, textvariable=pasta_var, width=350)
entry.pack(pady=5)

btn_pasta = ctk.CTkButton(frame, text="Escolher Pasta", command=selecionar_pasta)
btn_pasta.pack(pady=5)

btn_iniciar = ctk.CTkButton(frame, text="Iniciar Redimensionamento", command=iniciar_processamento)
btn_iniciar.pack(pady=15)

# Barra de Progresso
progress_bar = ctk.CTkProgressBar(frame, width=350)
progress_bar.set(0)
progress_bar.pack(pady=5)

# Label de Progresso
progress_label = ctk.CTkLabel(frame, text="Aguardando...")
progress_label.pack(pady=5)

# Rodar janela
root.mainloop()
