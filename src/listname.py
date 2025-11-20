import os
import customtkinter as ctk
from tkinter import filedialog
from openpyxl import Workbook

# ---------------- FUNÇÕES ----------------
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if not pasta:
        return
    entry_pasta.delete(0, "end")
    entry_pasta.insert(0, pasta)

    listar_arquivos(pasta)


def listar_arquivos(pasta_base):
    textbox.delete("1.0", "end")  # limpa o campo de texto
    arquivos.clear()

    for root, dirs, files in os.walk(pasta_base):
        for file in files:
            caminho_relativo = os.path.relpath(os.path.join(root, file), start=pasta_base)
            caminho_final = f"{os.path.basename(pasta_base)}/{caminho_relativo}"
            arquivos.append(caminho_final)
            textbox.insert("end", f"{caminho_final}\n")


def exportar_xlsx():
    if not arquivos:
        return

    salvar_arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Planilha Excel", "*.xlsx")],
        title="Salvar como"
    )
    if not salvar_arquivo:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Arquivos"

    ws.append(["Lista de Arquivos"])  # título
    for caminho in arquivos:
        ws.append([caminho])

    wb.save(salvar_arquivo)


# ---------------- JANELA ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Listar Arquivos da Pasta")

# centralizar janela
largura = 700
altura = 500
x = (janela.winfo_screenwidth() // 2) - (largura // 2)
y = (janela.winfo_screenheight() // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{x}+{y}")

arquivos = []  # lista global para armazenar os caminhos

# entrada + botão
frame_top = ctk.CTkFrame(janela)
frame_top.pack(pady=10, padx=10, fill="x")

entry_pasta = ctk.CTkEntry(frame_top, placeholder_text="Selecione uma pasta...")
entry_pasta.pack(side="left", fill="x", expand=True, padx=5)

btn_selecionar = ctk.CTkButton(frame_top, text="Selecionar Pasta", command=selecionar_pasta)
btn_selecionar.pack(side="left", padx=5)

btn_exportar = ctk.CTkButton(frame_top, text="Exportar XLSX", command=exportar_xlsx)
btn_exportar.pack(side="left", padx=5)

# caixa de texto com rolagem
frame_text = ctk.CTkFrame(janela)
frame_text.pack(padx=10, pady=10, fill="both", expand=True)

textbox = ctk.CTkTextbox(frame_text, wrap="none")
textbox.pack(side="left", fill="both", expand=True)

scrollbar_y = ctk.CTkScrollbar(frame_text, command=textbox.yview)
scrollbar_y.pack(side="right", fill="y")
textbox.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = ctk.CTkScrollbar(janela, orientation="horizontal", command=textbox.xview)
scrollbar_x.pack(fill="x")
textbox.configure(xscrollcommand=scrollbar_x.set)

janela.mainloop()
