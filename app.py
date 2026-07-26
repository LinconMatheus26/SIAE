import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import json
import os
import sys

from core.processor import processar

# ================== FIX PYINSTALLER ==================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_PATH = resource_path("config/settings.json")

def carregar_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def salvar_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# Tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Faturas")
        self.geometry("1000x600")

        # Estado
        self.pdf_var = ctk.StringVar()
        self.energia_var = ctk.StringVar()
        self.agua_var = ctk.StringVar()
        self.output_var = ctk.StringVar()
        self.historico = []
        self.processando = False

        self.config_data = carregar_config()

        self.setup_ui()

    # ================= UI =================

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_main_area()

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#0F172A")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # LOGO
        logo_container = ctk.CTkFrame(self.sidebar, width=140, height=140, corner_radius=20, fg_color="#FFFFFF")
        logo_container.pack(pady=(20, 10))
        logo_container.pack_propagate(False)

        logo_img = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/logo.png")),
            dark_image=Image.open(resource_path("assets/logo.png")),
            size=(110, 110)
        )

        ctk.CTkLabel(logo_container, image=logo_img, text="").pack(expand=True)

        ctk.CTkLabel(self.sidebar, text="Sistema de Faturas",
                     font=("Segoe UI", 16, "bold"), text_color="#E2E8F0").pack(pady=(0, 20))

        ctk.CTkButton(self.sidebar, text="Processar", command=self.mostrar_home)\
            .pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(self.sidebar, text="Histórico", command=self.mostrar_historico)\
            .pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(self.sidebar, text="Configurações", command=self.mostrar_config)\
            .pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(self.sidebar, text="Suporte", fg_color="transparent",
                      text_color="#E2E8F0", command=self.mostrar_suporte)\
            .pack(side="bottom", pady=20)

    def criar_main_area(self):
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.mostrar_home()

    def limpar_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    # ================= TELAS =================

    def mostrar_home(self):
        self.limpar_main()

        ctk.CTkLabel(self.main, text="SEPARAÇÃO DE FATURAS",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.tipo_label = ctk.CTkLabel(self.main, text="Aguardando ação...", text_color="gray")
        self.tipo_label.pack(pady=5)

        self.criar_input("Arquivo PDF", self.pdf_var, self.selecionar_pdf)
        self.criar_input("Planilha Energia", self.energia_var, self.selecionar_energia)
        self.criar_input("Planilha Água", self.agua_var, self.selecionar_agua)
        self.criar_input("Pasta de Saída", self.output_var, self.selecionar_pasta)

        ctk.CTkButton(self.main, text="Processar Arquivos",
                      height=45, command=self.executar_thread).pack(pady=20)

        self.progress = ctk.CTkProgressBar(self.main)
        self.progress.set(0)

    def mostrar_historico(self):
        self.limpar_main()

        ctk.CTkLabel(self.main, text="Histórico",
                     font=("Segoe UI", 20, "bold")).pack(pady=20)

        if not self.historico:
            ctk.CTkLabel(self.main, text="Nenhuma execução ainda.").pack()
            return

        for item in self.historico[::-1]:
            card = ctk.CTkFrame(self.main)
            card.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(card, text=f"{item['tipo']} • {item['pasta']}")\
                .pack(anchor="w", padx=10, pady=10)

    def mostrar_config(self):
        self.limpar_main()

        ctk.CTkLabel(self.main, text="Configurações",
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.config_output = ctk.StringVar(
            value=self.config_data.get("pasta_saida", "output")
        )

        self.criar_input("Pasta padrão", self.config_output, self.selecionar_pasta_config)

        self.var_abrir = ctk.BooleanVar(
            value=self.config_data.get("abrir_pasta_apos_processamento", True)
        )

        self.var_consolidado = ctk.BooleanVar(
            value=self.config_data.get("gerar_consolidado", True)
        )

        self.var_normalizar = ctk.BooleanVar(
            value=self.config_data.get("normalizar_texto", True)
        )

        ctk.CTkSwitch(self.main, text="Abrir pasta automaticamente", variable=self.var_abrir).pack(pady=5)
        ctk.CTkSwitch(self.main, text="Gerar consolidado", variable=self.var_consolidado).pack(pady=5)
        ctk.CTkSwitch(self.main, text="Normalizar nomes", variable=self.var_normalizar).pack(pady=5)

        ctk.CTkButton(self.main, text="Salvar Configurações",
                      command=self.salvar_configuracoes).pack(pady=20)

    def salvar_configuracoes(self):
        self.config_data["pasta_saida"] = self.config_output.get()
        self.config_data["abrir_pasta_apos_processamento"] = self.var_abrir.get()
        self.config_data["gerar_consolidado"] = self.var_consolidado.get()
        self.config_data["normalizar_texto"] = self.var_normalizar.get()

        salvar_config(self.config_data)
        messagebox.showinfo("Sucesso", "Configurações salvas!")

    def criar_input(self, label_text, variavel, comando):
        frame = ctk.CTkFrame(self.main, fg_color="transparent")
        frame.pack(fill="x", padx=60, pady=8)

        ctk.CTkLabel(frame, text=label_text).pack(anchor="w")

        inner = ctk.CTkFrame(frame)
        inner.pack(fill="x")

        ctk.CTkEntry(inner, textvariable=variavel, height=35)\
            .pack(side="left", fill="x", expand=True, padx=5, pady=5)

        ctk.CTkButton(inner, text="...", width=40, command=comando)\
            .pack(side="right", padx=5)

    # ================= PROCESSAMENTO =================

    def executar_thread(self):
        if not self.pdf_var.get():
            messagebox.showerror("Erro", "Selecione o PDF!")
            return

        self.processando = True
        self.progress.pack(pady=10)

        threading.Thread(target=self.animar_loading).start()
        threading.Thread(target=self.executar).start()

    def animar_loading(self):
        valor = 0
        while self.processando:
            valor = (valor + 0.02) % 1
            self.progress.set(valor)
            self.update_idletasks()

    def executar(self):
        try:
            config = carregar_config()

            if self.output_var.get():
                config["pasta_saida"] = self.output_var.get()

            pasta, tipo = processar(
                self.pdf_var.get(),
                self.energia_var.get(),
                self.agua_var.get(),
                config
            )

            self.processando = False
            self.progress.set(1)

            self.tipo_label.configure(text=f"✔ Tipo: {tipo}", text_color="#22c55e")

            self.historico.append({"tipo": tipo, "pasta": pasta})

            messagebox.showinfo("Sucesso", f"Arquivos salvos em:\n{pasta}")

            if config.get("abrir_pasta_apos_processamento", True):
                os.startfile(pasta)

        except Exception as e:
            self.processando = False
            self.tipo_label.configure(text="Erro", text_color="#ef4444")
            messagebox.showerror("Erro", str(e))

    # ================= UTIL =================

    def selecionar_pdf(self):
        caminho = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if caminho:
            self.pdf_var.set(caminho)

    def selecionar_energia(self):
        caminho = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if caminho:
            self.energia_var.set(caminho)

    def selecionar_agua(self):
        caminho = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if caminho:
            self.agua_var.set(caminho)

    def selecionar_pasta(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.output_var.set(caminho)

    def selecionar_pasta_config(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.config_output.set(caminho)

    def mostrar_suporte(self):
        messagebox.showinfo(
            "Suporte",
            "Sistema de Faturas\n\nDesenvolvedor: Lincon Matheus\nEmail: lincon.silva.estagio@prf.gov.br"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()