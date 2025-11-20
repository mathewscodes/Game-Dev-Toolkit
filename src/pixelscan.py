import os
from openpyxl import Workbook
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageSequence

resultados = []  # lista de (nome, pixel, caminho)
indice_atual = None  # índice do sprite atualmente visualizado

# ---------------- FUNÇÕES ----------------
def detectar_pe(image_path):
    """Detecta o pixel mais baixo (maior Y) em todos os frames do GIF"""
    try:
        img = Image.open(image_path)
        altura = img.size[1]
        maior_y = -1  # começa acima do limite superior

        for frame in ImageSequence.Iterator(img):
            frame_rgba = frame.convert("RGBA")
            largura, altura = frame_rgba.size
            pixels = frame_rgba.load()

            for y in range(altura - 1, -1, -1):  # de baixo pra cima
                for x in range(largura):
                    r, g, b, a = pixels[x, y]
                    if a > 0:  # pixel não transparente
                        if y > maior_y:
                            maior_y = y
                        break  # já achou nesse Y, vai pro próximo

        return maior_y if maior_y >= 0 else None
    except Exception as e:
        return f"Erro: {e}"

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_var.set(pasta)

def iniciar_scan():
    global resultados, indice_atual
    pasta = pasta_var.get()
    if not pasta:
        messagebox.showwarning("Aviso", "Selecione uma pasta antes de iniciar o scan.")
        return

    # Limpa resultados anteriores
    for widget in resultados_frame.winfo_children():
        widget.destroy()
    resultados = []
    indice_atual = None

    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(".gif")]
    arquivos.sort()

    if not arquivos:
        aviso = ctk.CTkLabel(resultados_frame, text="⚠️ Nenhum arquivo .gif encontrado!")
        aviso.pack(pady=5)
        return

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        pos_y = detectar_pe(caminho)
        resultados.append((arquivo, pos_y, caminho))

    # Cria botões para cada resultado
    for i, (nome, pixel, _) in enumerate(resultados):
        btn = ctk.CTkButton(resultados_frame, text=f"{nome}  ({pixel})",
                            command=lambda idx=i: visualizar_sprite(idx))
        btn.pack(fill="x", padx=5, pady=2)

def exportar_xlsx():
    if not resultados:
        messagebox.showwarning("Aviso", "Nenhum resultado para exportar.")
        return

    arquivo_xlsx = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Salvar como"
    )
    if not arquivo_xlsx:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Cabeçalho
    ws.append(["nome", "pixel"])

    # Dados
    for nome, pixel, _ in resultados:
        ws.append([nome, pixel])

    wb.save(arquivo_xlsx)
    messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{arquivo_xlsx}")

def visualizar_sprite(idx):
    global indice_atual
    indice_atual = idx
    atualizar_canvas()

def atualizar_canvas():
    global indice_atual
    if indice_atual is None or not resultados:
        return

    nome, pixel_y, caminho_img = resultados[indice_atual]

    # Carrega imagem e desenha linha
    img = Image.open(caminho_img).convert("RGBA")
    draw = ImageDraw.Draw(img)
    if isinstance(pixel_y, int):  # só desenha se não for erro
        draw.line([(0, pixel_y), (img.width, pixel_y)], fill="red", width=1)

    # Redimensiona para caber no canvas 250x210 mantendo proporção
    scale = min(250 / img.width, 210 / img.height, 1)
    new_size = (int(img.width * scale), int(img.height * scale))
    img_resized = img.resize(new_size, Image.NEAREST)

    img_tk = ImageTk.PhotoImage(img_resized)
    sprite_canvas.delete("all")
    sprite_canvas.create_image(125, 105, anchor="center", image=img_tk)
    sprite_canvas.image = img_tk  # evitar garbage collector

    titulo_label.configure(text=f"{nome}  |  Pixel Y = {pixel_y}")

def navegar_sprite(direcao):
    global indice_atual
    if indice_atual is None:
        return
    indice_atual = (indice_atual + direcao) % len(resultados)
    atualizar_canvas()

# ---------------- INTERFACE ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PixelScan")
app.geometry("800x800")

pasta_var = ctk.StringVar()

frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=20, fill="x")

pasta_label = ctk.CTkLabel(frame, text="Pasta selecionada:")
pasta_label.pack(anchor="w", padx=10, pady=(5, 0))

pasta_entry = ctk.CTkEntry(frame, textvariable=pasta_var, width=400)
pasta_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

pasta_button = ctk.CTkButton(frame, text="Selecionar Pasta", command=selecionar_pasta)
pasta_button.pack(side="left", padx=10)

scan_button = ctk.CTkButton(app, text="Iniciar Scan", command=iniciar_scan)
scan_button.pack(pady=5)

export_button = ctk.CTkButton(app, text="Exportar XLSX", command=exportar_xlsx)
export_button.pack(pady=5)

# Área de resultados (scrollable)
scroll_frame = ctk.CTkScrollableFrame(app, height=200)
scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

resultados_frame = ctk.CTkFrame(scroll_frame)
resultados_frame.pack(fill="both", expand=True)

# Área de visualização
titulo_label = ctk.CTkLabel(app, text="Selecione um sprite", font=("Arial", 14))
titulo_label.pack(pady=5)

sprite_canvas = ctk.CTkCanvas(app, width=250, height=210, bg="black")
sprite_canvas.pack(pady=5)

# Botões navegação
nav_frame = ctk.CTkFrame(app)
nav_frame.pack(pady=10)

btn_prev = ctk.CTkButton(nav_frame, text="⬅ Anterior", command=lambda: navegar_sprite(-1))
btn_prev.grid(row=0, column=0, padx=10)

btn_next = ctk.CTkButton(nav_frame, text="Próximo ➡", command=lambda: navegar_sprite(1))
btn_next.grid(row=0, column=1, padx=10)

# Bind das teclas de seta
app.bind("<Left>", lambda event: navegar_sprite(-1))
app.bind("<Right>", lambda event: navegar_sprite(1))

app.mainloop()
