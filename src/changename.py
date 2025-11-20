import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox


# ---------------- VARIÁVEIS DE CONTROLE ----------------
ultima_acao = []  # guarda os arquivos renomeados para desfazer
pasta_selecionada = None


# ---------------- FUNÇÕES ----------------
def selecionar_pasta():
    global pasta_selecionada
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_selecionada = pasta
        label_pasta.configure(text=f"Pasta selecionada:\n{pasta}")


def renomear_arquivos():
    global ultima_acao, pasta_selecionada
    sufixo = entry_sufixo.get().strip()

    if not pasta_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
        return

    if not sufixo:
        messagebox.showwarning("Aviso", "Digite um sufixo para renomear!")
        return

    arquivos = os.listdir(pasta_selecionada)
    renomeados = []

    for arquivo in arquivos:
        caminho_antigo = os.path.join(pasta_selecionada, arquivo)
        if os.path.isfile(caminho_antigo):
            nome, ext = os.path.splitext(arquivo)
            novo_nome = f"{nome}{sufixo}{ext}"
            caminho_novo = os.path.join(pasta_selecionada, novo_nome)

            os.rename(caminho_antigo, caminho_novo)
            renomeados.append((caminho_novo, caminho_antigo))  # guarda para desfazer

    ultima_acao = renomeados
    messagebox.showinfo("Sucesso", f"{len(renomeados)} arquivos foram renomeados!")


def desfazer_acao():
    global ultima_acao
    if not ultima_acao:
        messagebox.showwarning("Aviso", "Não há ação para desfazer!")
        return

    for novo, antigo in ultima_acao:
        if os.path.exists(novo):
            os.rename(novo, antigo)

    messagebox.showinfo("Desfeito", f"{len(ultima_acao)} arquivos voltaram ao nome original.")
    ultima_acao = []


# ---------------- INTERFACE ----------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Renomeador de Arquivos")
janela.geometry("500x300")
janela.eval('tk::PlaceWindow . center')  # abre no meio da tela

# Widgets
label_instrucao = ctk.CTkLabel(janela, text="Digite o sufixo para adicionar ao nome dos arquivos:")
label_instrucao.pack(pady=10)

entry_sufixo = ctk.CTkEntry(janela, width=300, placeholder_text="_normal")
entry_sufixo.pack(pady=5)

btn_pasta = ctk.CTkButton(janela, text="Selecionar Pasta", command=selecionar_pasta)
btn_pasta.pack(pady=10)

label_pasta = ctk.CTkLabel(janela, text="Nenhuma pasta selecionada")
label_pasta.pack(pady=5)

btn_renomear = ctk.CTkButton(janela, text="Renomear Arquivos", command=renomear_arquivos)
btn_renomear.pack(pady=10)

btn_desfazer = ctk.CTkButton(janela, text="Desfazer Última Ação", command=desfazer_acao)
btn_desfazer.pack(pady=10)

# Iniciar
janela.mainloop()
