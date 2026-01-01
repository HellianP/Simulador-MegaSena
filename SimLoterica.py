import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
import time
import threading
from itertools import combinations

# Tabela de preços da Mega-Sena (valores atualizados 2024)
PRECOS = {
    6: 6.00,
    7: 42.00,
    8: 168.00,
    9: 504.00,
    10: 1260.00,
    11: 2772.00,
    12: 5544.00,
    13: 10296.00,
    14: 18018.00,
    15: 30030.00,
    16: 48048.00,
    17: 74256.00,
    18: 111384.00,
    19: 162792.00,
    20: 232560.00
}

class SeletorNumeros(tk.Toplevel):
    """Janela popup para seleção visual de números"""
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Selecionar Dezenas")
        self.geometry("650x550")
        self.configure(bg="#1e1e2e")
        self.callback = callback
        self.numeros_selecionados = set()
        
        # Frame superior com instruções
        frame_top = tk.Frame(self, bg="#2e2e3e", padx=10, pady=10)
        frame_top.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_top, text="Clique nos números para selecionar (mín: 6, máx: 20)", 
                bg="#2e2e3e", fg="white", font=("Arial", 11, "bold")).pack()
        
        self.label_contador = tk.Label(frame_top, text="Selecionados: 0", 
                                       bg="#2e2e3e", fg="#4aff4a", font=("Arial", 12, "bold"))
        self.label_contador.pack(pady=5)
        
        # Frame com grid de números
        frame_numeros = tk.Frame(self, bg="#1e1e2e", padx=10, pady=10)
        frame_numeros.pack(fill="both", expand=True, padx=10)
        
        self.botoes = {}
        for i in range(1, 61):
            row = (i - 1) // 10
            col = (i - 1) % 10
            
            btn = tk.Button(frame_numeros, text=f"{i:02d}", 
                          width=4, height=2, font=("Arial", 10, "bold"),
                          bg="#4a4a6a", fg="white",
                          command=lambda num=i: self.toggle_numero(num))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.botoes[i] = btn
        
        # Frame de botões
        frame_botoes = tk.Frame(self, bg="#2e2e3e", padx=10, pady=10)
        frame_botoes.pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame_botoes, text="Limpar", command=self.limpar,
                 bg="#ff4a4a", fg="white", font=("Arial", 10, "bold"), 
                 padx=20).pack(side="left", padx=5)
        
        tk.Button(frame_botoes, text="Confirmar", command=self.confirmar,
                 bg="#4aff4a", fg="black", font=("Arial", 10, "bold"), 
                 padx=20).pack(side="right", padx=5)
    
    def toggle_numero(self, numero):
        if numero in self.numeros_selecionados:
            self.numeros_selecionados.remove(numero)
            self.botoes[numero].config(bg="#4a4a6a", fg="white")
        else:
            if len(self.numeros_selecionados) < 20:
                self.numeros_selecionados.add(numero)
                self.botoes[numero].config(bg="#4aff4a", fg="black")
            else:
                messagebox.showwarning("Limite", "Máximo de 20 dezenas!")
        
        self.label_contador.config(text=f"Selecionados: {len(self.numeros_selecionados)}")
    
    def limpar(self):
        self.numeros_selecionados.clear()
        for btn in self.botoes.values():
            btn.config(bg="#4a4a6a", fg="white")
        self.label_contador.config(text="Selecionados: 0")
    
    def confirmar(self):
        if len(self.numeros_selecionados) < 6:
            messagebox.showwarning("Aviso", "Selecione pelo menos 6 dezenas!")
            return
        
        self.callback(sorted(list(self.numeros_selecionados)))
        self.destroy()

class MegaSenaSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Mega-Sena")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e2e")
        
        self.jogos = []
        self.numeros_sorteados = []
        self.sorteio_ativo = False
        self.thread_sorteio = None
        
        # Variáveis para simulação automática
        self.simulacao_ativa = False
        self.historico_sorteios = []
        self.total_sorteios = 0
        self.jogos_simulacao = []
        self.parar_em_quadra = tk.BooleanVar(value=False)
        self.parar_em_quina = tk.BooleanVar(value=False)
        self.parar_em_sena = tk.BooleanVar(value=True)
        
        self.criar_interface()
        
    def criar_interface(self):
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba 1: Sorteio Manual
        self.aba_manual = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.aba_manual, text="Sorteio Manual")
        
        # Aba 2: Simulação Automática
        self.aba_simulacao = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.aba_simulacao, text="Simulação Automática")
        
        self.criar_aba_manual()
        self.criar_aba_simulacao()
        
    def criar_aba_manual(self):
        # Frame superior - Entrada de jogos
        frame_entrada = tk.Frame(self.aba_manual, bg="#2e2e3e", padx=10, pady=10)
        frame_entrada.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_entrada, text="Digite suas dezenas (separadas por vírgula):", 
                bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(anchor="w")
        
        self.entry_dezenas = tk.Entry(frame_entrada, font=("Arial", 12), width=60)
        self.entry_dezenas.pack(pady=5, fill="x")
        
        frame_botoes = tk.Frame(frame_entrada, bg="#2e2e3e")
        frame_botoes.pack(pady=5)
        
        tk.Button(frame_botoes, text="Adicionar Jogo", command=self.adicionar_jogo,
                 bg="#4a9eff", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        tk.Button(frame_botoes, text="Seletor Visual", command=lambda: self.abrir_seletor_visual(self.adicionar_jogo_direto),
                 bg="#9a4aff", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        tk.Button(frame_botoes, text="Jogo Aleatório", command=self.adicionar_jogo_aleatorio,
                 bg="#ff4a9a", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        tk.Button(frame_botoes, text="Limpar Jogos", command=self.limpar_jogos,
                 bg="#ff4a4a", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        tk.Button(frame_botoes, text="Iniciar Sorteio", command=self.iniciar_sorteio,
                 bg="#4aff4a", fg="black", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        tk.Button(frame_botoes, text="Parar Sorteio", command=self.parar_sorteio,
                 bg="#ffaa4a", fg="black", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=3)
        
        # Frame do meio - Informações dos jogos
        frame_info = tk.Frame(self.aba_manual, bg="#2e2e3e", padx=10, pady=10)
        frame_info.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(frame_info, text="Seus Jogos:", bg="#2e2e3e", fg="white", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.text_jogos = scrolledtext.ScrolledText(frame_info, height=10, 
                                                     font=("Courier", 10), bg="#1a1a2a", fg="#00ff00")
        self.text_jogos.pack(fill="both", expand=True, pady=5)
        
        # Frame de números sorteados
        frame_sorteio = tk.Frame(self.aba_manual, bg="#2e2e3e", padx=10, pady=15)
        frame_sorteio.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_sorteio, text="Números Sorteados:", bg="#2e2e3e", fg="white",
                font=("Arial", 14, "bold")).pack()
        
        self.frame_numeros = tk.Frame(frame_sorteio, bg="#2e2e3e")
        self.frame_numeros.pack(pady=10)
        
        self.labels_sorteados = []
        for i in range(6):
            label = tk.Label(self.frame_numeros, text="--", bg="#4a4a6a", fg="white",
                           font=("Arial", 20, "bold"), width=3, height=1, relief="raised", bd=3)
            label.pack(side="left", padx=5)
            self.labels_sorteados.append(label)
        
        # Frame de estatísticas
        frame_stats = tk.Frame(self.aba_manual, bg="#2e2e3e", padx=10, pady=10)
        frame_stats.pack(fill="x", padx=10, pady=5)
        
        self.label_stats = tk.Label(frame_stats, text="Aguardando sorteio...", 
                                    bg="#2e2e3e", fg="#ffff00", font=("Arial", 11, "bold"))
        self.label_stats.pack()
    
    def criar_aba_simulacao(self):
        # Frame superior - Configuração
        frame_config = tk.Frame(self.aba_simulacao, bg="#2e2e3e", padx=10, pady=10)
        frame_config.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_config, text="SIMULAÇÃO AUTOMÁTICA DE SORTEIOS", 
                bg="#2e2e3e", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Frame de gerenciamento de jogos
        frame_jogos_sim = tk.LabelFrame(frame_config, text="Seus Jogos", 
                                        bg="#2e2e3e", fg="white", font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_jogos_sim.pack(pady=10, fill="both")
        
        # Entrada de dezenas
        frame_entrada_sim = tk.Frame(frame_jogos_sim, bg="#2e2e3e")
        frame_entrada_sim.pack(fill="x", pady=5)
        
        tk.Label(frame_entrada_sim, text="Dezenas:", 
                bg="#2e2e3e", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        
        self.entry_dezenas_sim = tk.Entry(frame_entrada_sim, font=("Arial", 11), width=40)
        self.entry_dezenas_sim.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botões para adicionar jogos
        frame_btn_add = tk.Frame(frame_jogos_sim, bg="#2e2e3e")
        frame_btn_add.pack(pady=5)
        
        tk.Button(frame_btn_add, text="Adicionar Jogo", command=self.adicionar_jogo_simulacao,
                 bg="#4a9eff", fg="white", font=("Arial", 9, "bold"), padx=10).pack(side="left", padx=3)
        
        tk.Button(frame_btn_add, text="Seletor Visual", 
                 command=lambda: self.abrir_seletor_visual(self.adicionar_jogo_simulacao_direto),
                 bg="#9a4aff", fg="white", font=("Arial", 9, "bold"), padx=10).pack(side="left", padx=3)
        
        tk.Button(frame_btn_add, text="Jogo Aleatório", command=self.adicionar_jogo_simulacao_aleatorio,
                 bg="#ff4a9a", fg="white", font=("Arial", 9, "bold"), padx=10).pack(side="left", padx=3)
        
        tk.Button(frame_btn_add, text="Limpar Jogos", command=self.limpar_jogos_simulacao,
                 bg="#ff4a4a", fg="white", font=("Arial", 9, "bold"), padx=10).pack(side="left", padx=3)
        
        # Lista de jogos
        self.text_jogos_sim = scrolledtext.ScrolledText(frame_jogos_sim, height=5, 
                                                        font=("Courier", 9), bg="#1a1a2a", fg="#00ff00")
        self.text_jogos_sim.pack(fill="both", expand=True, pady=5)
        
        # Quantidade de sorteios
        frame_qtd = tk.Frame(frame_config, bg="#2e2e3e")
        frame_qtd.pack(pady=10)
        
        tk.Label(frame_qtd, text="Quantidade de sorteios (0 = ilimitado):", 
                bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(side="left", padx=5)
        
        self.entry_qtd_sorteios = tk.Entry(frame_qtd, font=("Arial", 12), width=15)
        self.entry_qtd_sorteios.insert(0, "0")
        self.entry_qtd_sorteios.pack(side="left", padx=5)
        
        # Condições de parada
        frame_parada = tk.LabelFrame(frame_config, text="Condições de Parada", 
                                     bg="#2e2e3e", fg="white", font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_parada.pack(pady=10, fill="x")
        
        tk.Checkbutton(frame_parada, text="Parar ao acertar QUADRA (4 números)", 
                      variable=self.parar_em_quadra, bg="#2e2e3e", fg="white", 
                      selectcolor="#4a4a6a", font=("Arial", 10)).pack(anchor="w")
        
        tk.Checkbutton(frame_parada, text="Parar ao acertar QUINA (5 números)", 
                      variable=self.parar_em_quina, bg="#2e2e3e", fg="white", 
                      selectcolor="#4a4a6a", font=("Arial", 10)).pack(anchor="w")
        
        tk.Checkbutton(frame_parada, text="Parar ao acertar SENA (6 números)", 
                      variable=self.parar_em_sena, bg="#2e2e3e", fg="white", 
                      selectcolor="#4a4a6a", font=("Arial", 10)).pack(anchor="w")
        
        # Botões
        frame_botoes_sim = tk.Frame(frame_config, bg="#2e2e3e")
        frame_botoes_sim.pack(pady=10)
        
        tk.Button(frame_botoes_sim, text="Iniciar Simulação", command=self.iniciar_simulacao,
                 bg="#4aff4a", fg="black", font=("Arial", 11, "bold"), padx=30, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame_botoes_sim, text="Parar Simulação", command=self.parar_simulacao,
                 bg="#ff4a4a", fg="white", font=("Arial", 11, "bold"), padx=30, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame_botoes_sim, text="Limpar Histórico", command=self.limpar_historico,
                 bg="#ffaa4a", fg="black", font=("Arial", 11, "bold"), padx=30, pady=5).pack(side="left", padx=5)
        
        # Frame de estatísticas da simulação
        frame_stats_sim = tk.Frame(self.aba_simulacao, bg="#2e2e3e", padx=10, pady=10)
        frame_stats_sim.pack(fill="x", padx=10, pady=5)
        
        self.label_stats_sim = tk.Label(frame_stats_sim, text="Aguardando início da simulação...", 
                                        bg="#2e2e3e", fg="#ffff00", font=("Arial", 11, "bold"))
        self.label_stats_sim.pack()
        
        # Frame de histórico
        frame_historico = tk.Frame(self.aba_simulacao, bg="#2e2e3e", padx=10, pady=10)
        frame_historico.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(frame_historico, text="Histórico de Sorteios:", bg="#2e2e3e", fg="white", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.text_historico = scrolledtext.ScrolledText(frame_historico, height=12, 
                                                        font=("Courier", 8), bg="#1a1a2a", fg="#00ff00")
        self.text_historico.pack(fill="both", expand=True, pady=5)
    
    def abrir_seletor_visual(self, callback):
        SeletorNumeros(self.root, callback)
    
    def calcular_probabilidade(self, qtd_dezenas):
        """Calcula a probabilidade de ganhar com X dezenas"""
        combinacoes_possiveis = self.combinar(60, 6)
        combinacoes_jogo = self.combinar(qtd_dezenas, 6)
        probabilidade = (combinacoes_jogo / combinacoes_possiveis) * 100
        return probabilidade
    
    def combinar(self, n, k):
        """Calcula combinação C(n,k)"""
        from math import factorial
        return factorial(n) / (factorial(k) * factorial(n - k))
    
    def adicionar_jogo_direto(self, dezenas):
        """Adiciona jogo a partir da lista de dezenas"""
        dezenas_ordenadas = sorted(dezenas)
        preco = PRECOS[len(dezenas)]
        probabilidade = self.calcular_probabilidade(len(dezenas))
        
        self.jogos.append({
            'dezenas': dezenas_ordenadas,
            'preco': preco,
            'probabilidade': probabilidade
        })
        
        print(f"\n{'='*60}")
        print(f"JOGO ADICIONADO!")
        print(f"Dezenas: {dezenas_ordenadas}")
        print(f"Quantidade: {len(dezenas)} dezenas")
        print(f"Preço: R$ {preco:.2f}")
        print(f"Probabilidade: {probabilidade:.8f}%")
        print(f"{'='*60}")
        
        self.atualizar_display_jogos()
    
    def adicionar_jogo(self):
        try:
            texto = self.entry_dezenas.get().strip()
            if not texto:
                messagebox.showwarning("Aviso", "Digite as dezenas!")
                return
            
            dezenas = [int(x.strip()) for x in texto.split(",")]
            
            # Validações
            if len(dezenas) < 6 or len(dezenas) > 20:
                messagebox.showerror("Erro", "Escolha entre 6 e 20 dezenas!")
                return
            
            if len(set(dezenas)) != len(dezenas):
                messagebox.showerror("Erro", "Há dezenas repetidas!")
                return
            
            if any(d < 1 or d > 60 for d in dezenas):
                messagebox.showerror("Erro", "Dezenas devem estar entre 1 e 60!")
                return
            
            self.adicionar_jogo_direto(dezenas)
            self.entry_dezenas.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números separados por vírgula!")
    
    def adicionar_jogo_aleatorio(self):
        """Adiciona um jogo com números aleatórios"""
        qtd = random.randint(6, 15)  # Gera entre 6 e 15 dezenas
        dezenas = random.sample(range(1, 61), qtd)
        self.adicionar_jogo_direto(dezenas)
        messagebox.showinfo("Jogo Aleatório", f"Jogo com {qtd} dezenas criado!")
    
    def atualizar_display_jogos(self):
        self.text_jogos.delete(1.0, tk.END)
        
        if not self.jogos:
            self.text_jogos.insert(tk.END, "Nenhum jogo adicionado ainda.\n")
            return
        
        total_gasto = sum(j['preco'] for j in self.jogos)
        prob_total = sum(j['probabilidade'] for j in self.jogos)
        
        self.text_jogos.insert(tk.END, f"{'='*80}\n")
        self.text_jogos.insert(tk.END, f"RESUMO DOS JOGOS\n")
        self.text_jogos.insert(tk.END, f"{'='*80}\n\n")
        
        for idx, jogo in enumerate(self.jogos, 1):
            self.text_jogos.insert(tk.END, f"Jogo {idx}: {jogo['dezenas']}\n")
            self.text_jogos.insert(tk.END, f"  └─ {len(jogo['dezenas'])} dezenas | ")
            self.text_jogos.insert(tk.END, f"R$ {jogo['preco']:.2f} | ")
            self.text_jogos.insert(tk.END, f"Chance: {jogo['probabilidade']:.8f}%\n\n")
        
        self.text_jogos.insert(tk.END, f"{'-'*80}\n")
        self.text_jogos.insert(tk.END, f"TOTAL GASTO: R$ {total_gasto:.2f}\n")
        self.text_jogos.insert(tk.END, f"PROBABILIDADE TOTAL: {prob_total:.8f}%\n")
        self.text_jogos.insert(tk.END, f"Isso é 1 em {int(1/(prob_total/100)):,}\n")
        self.text_jogos.insert(tk.END, f"{'='*80}\n")
    
    def limpar_jogos(self):
        self.jogos = []
        self.atualizar_display_jogos()
        print("\n" + "="*60)
        print("JOGOS LIMPOS!")
        print("="*60)
    
    # ========== FUNÇÕES SIMULAÇÃO ==========
    
    def adicionar_jogo_simulacao_direto(self, dezenas):
        """Adiciona jogo na simulação a partir da lista"""
        dezenas_ordenadas = sorted(dezenas)
        preco = PRECOS[len(dezenas)]
        probabilidade = self.calcular_probabilidade(len(dezenas))
        
        self.jogos_simulacao.append({
            'dezenas': dezenas_ordenadas,
            'preco': preco,
            'probabilidade': probabilidade
        })
        
        print(f"\n{'='*60}")
        print(f"JOGO ADICIONADO À SIMULAÇÃO!")
        print(f"Dezenas: {dezenas_ordenadas}")
        print(f"Preço: R$ {preco:.2f} | Chance: {probabilidade:.8f}%")
        print(f"{'='*60}")
        
        self.atualizar_display_jogos_simulacao()
    
    def adicionar_jogo_simulacao(self):
        try:
            texto = self.entry_dezenas_sim.get().strip()
            if not texto:
                messagebox.showwarning("Aviso", "Digite as dezenas!")
                return
            
            dezenas = [int(x.strip()) for x in texto.split(",")]
            
            if len(dezenas) < 6 or len(dezenas) > 20:
                messagebox.showerror("Erro", "Escolha entre 6 e 20 dezenas!")
                return
            
            if len(set(dezenas)) != len(dezenas):
                messagebox.showerror("Erro", "Há dezenas repetidas!")
                return
            
            if any(d < 1 or d > 60 for d in dezenas):
                messagebox.showerror("Erro", "Dezenas devem estar entre 1 e 60!")
                return
            
            self.adicionar_jogo_simulacao_direto(dezenas)
            self.entry_dezenas_sim.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números válidos!")
    
    def adicionar_jogo_simulacao_aleatorio(self):
        qtd = random.randint(6, 15)
        dezenas = random.sample(range(1, 61), qtd)
        self.adicionar_jogo_simulacao_direto(dezenas)
        messagebox.showinfo("Jogo Aleatório", f"Jogo com {qtd} dezenas adicionado!")
    
    def atualizar_display_jogos_simulacao(self):
        self.text_jogos_sim.delete(1.0, tk.END)
        
        if not self.jogos_simulacao:
            self.text_jogos_sim.insert(tk.END, "Nenhum jogo adicionado.\n")
            return
        
        total_gasto = sum(j['preco'] for j in self.jogos_simulacao)
        
        for idx, jogo in enumerate(self.jogos_simulacao, 1):
            self.text_jogos_sim.insert(tk.END, f"Jogo {idx}: {jogo['dezenas']} ")
            self.text_jogos_sim.insert(tk.END, f"| R$ {jogo['preco']:.2f} ")
            self.text_jogos_sim.insert(tk.END, f"| {jogo['probabilidade']:.8f}%\n")
        
        self.text_jogos_sim.insert(tk.END, f"\nTotal: {len(self.jogos_simulacao)} jogos | R$ {total_gasto:.2f}\n")
    
    def limpar_jogos_simulacao(self):
        self.jogos_simulacao = []
        self.atualizar_display_jogos_simulacao()
        print("\n" + "="*60)
        print("JOGOS DA SIMULAÇÃO LIMPOS!")
        print("="*60)
    
    def iniciar_sorteio(self):
        if not self.jogos:
            messagebox.showwarning("Aviso", "Adicione pelo menos um jogo!")
            return
        
        if self.sorteio_ativo:
            return
        
        self.sorteio_ativo = True
        self.numeros_sorteados = []
        
        for label in self.labels_sorteados:
            label.config(text="--", bg="#4a4a6a")
        
        print("\n" + "="*60)
        print("INICIANDO SORTEIO...")
        print("="*60)
        
        self.thread_sorteio = threading.Thread(target=self.sortear_numeros, daemon=True)
        self.thread_sorteio.start()
    
    def parar_sorteio(self):
        self.sorteio_ativo = False
        print("\n" + "="*60)
        print("SORTEIO INTERROMPIDO!")
        print("="*60)
    
    def sortear_numeros(self):
        numeros_disponiveis = list(range(1, 61))
        
        for i in range(6):
            if not self.sorteio_ativo:
                break
            
            time.sleep(5)
            
            numero = random.choice(numeros_disponiveis)
            numeros_disponiveis.remove(numero)
            self.numeros_sorteados.append(numero)
            
            print(f"\nNÚMERO #{i+1}: {numero:02d}")
            print(f"Sorteados: {sorted(self.numeros_sorteados)}")
            
            self.root.after(0, self.atualizar_sorteio, i, numero)
            self.root.after(0, self.verificar_acertos)
        
        if self.sorteio_ativo:
            self.sorteio_ativo = False
            print("\n" + "="*60)
            print("SORTEIO FINALIZADO!")
            print(f"Números: {sorted(self.numeros_sorteados)}")
            print("="*60)
            self.root.after(0, self.exibir_resultado_final)
    
    def atualizar_sorteio(self, indice, numero):
        self.labels_sorteados[indice].config(text=f"{numero:02d}", bg="#4aff4a", fg="black")
    
    def verificar_acertos(self):
        if len(self.numeros_sorteados) < 4:
            self.label_stats.config(text=f"Aguardando... ({len(self.numeros_sorteados)}/6)")
            return
        
        stats_text = f"Números sorteados: {len(self.numeros_sorteados)}/6\n\n"
        
        for idx, jogo in enumerate(self.jogos, 1):
            acertos = len(set(jogo['dezenas']) & set(self.numeros_sorteados))
            
            premio = ""
            if acertos == 4:
                premio = " 🎉 QUADRA!"
            elif acertos == 5:
                premio = " 🎊 QUINA!"
            elif acertos == 6:
                premio = " 🏆 SENA!"
            
            stats_text += f"Jogo {idx}: {acertos} acertos{premio}\n"
            print(f"  Jogo {idx}: {acertos} acertos{premio}")
        
        self.label_stats.config(text=stats_text)
    
    def exibir_resultado_final(self):
        resultado = "RESULTADO FINAL\n\n"
        resultado += f"Números: {sorted(self.numeros_sorteados)}\n\n"
        
        ganhou_algo = False
        
        for idx, jogo in enumerate(self.jogos, 1):
            acertos = len(set(jogo['dezenas']) & set(self.numeros_sorteados))
            resultado += f"Jogo {idx}: {acertos} acertos\n"
            
            if acertos >= 4:
                ganhou_algo = True
                if acertos == 4:
                    resultado += "  → QUADRA! 🎉\n"
                elif acertos == 5:
                    resultado += "  → QUINA! 🎊\n"
                elif acertos == 6:
                    resultado += "  → SENA! 🏆\n"
        
        if not ganhou_algo:
            resultado += "\nSem prêmios. 😢"
        
        messagebox.showinfo("Resultado", resultado)
        self.label_stats.config(text=resultado)
    
    # ========== SIMULAÇÃO AUTOMÁTICA ==========
    
    def iniciar_simulacao(self):
        if self.simulacao_ativa:
            messagebox.showinfo("Info", "Simulação já em andamento!")
            return
        
        if not self.jogos_simulacao:
            messagebox.showwarning("Aviso", "Adicione pelo menos um jogo!")
            return
        
        try:
            qtd_sorteios = int(self.entry_qtd_sorteios.get())
            if qtd_sorteios < 0:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return
            
            self.qtd_max_sorteios = qtd_sorteios
            self.simulacao_ativa = True
            self.total_sorteios = 0
            self.historico_sorteios = []
            
            print("\n" + "="*80)
            print("INICIANDO SIMULAÇÃO")
            print(f"Jogos: {len(self.jogos_simulacao)}")
            print(f"Sorteios: {'Ilimitado' if qtd_sorteios == 0 else qtd_sorteios}")
            print("="*80)
            
            thread_sim = threading.Thread(target=self.executar_simulacao, daemon=True)
            thread_sim.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido!")
    
    def executar_simulacao(self):
        melhor_resultado = 0
        total_quadras = 0
        total_quinas = 0
        total_senas = 0
        custo_por_sorteio = sum(j['preco'] for j in self.jogos_simulacao)
        
        while self.simulacao_ativa:
            if self.qtd_max_sorteios > 0 and self.total_sorteios >= self.qtd_max_sorteios:
                self.simulacao_ativa = False
                break
            
            sorteio = sorted(random.sample(range(1, 61), 6))
            self.total_sorteios += 1
            
            # Verifica acertos em cada jogo
            resultados_jogos = []
            melhor_acerto_sorteio = 0
            parar = False
            
            for jogo in self.jogos_simulacao:
                acertos = len(set(jogo['dezenas']) & set(sorteio))
                resultados_jogos.append(acertos)
                
                if acertos > melhor_acerto_sorteio:
                    melhor_acerto_sorteio = acertos
                
                if acertos == 4:
                    total_quadras += 1
                    if self.parar_em_quadra.get():
                        parar = True
                elif acertos == 5:
                    total_quinas += 1
                    if self.parar_em_quina.get():
                        parar = True
                elif acertos == 6:
                    total_senas += 1
                    if self.parar_em_sena.get():
                        parar = True
            
            if melhor_acerto_sorteio > melhor_resultado:
                melhor_resultado = melhor_acerto_sorteio
            
            premio = ""
            if melhor_acerto_sorteio == 4:
                premio = "QUADRA! 🎉"
            elif melhor_acerto_sorteio == 5:
                premio = "QUINA! 🎊"
            elif melhor_acerto_sorteio == 6:
                premio = "SENA! 🏆"
            
            info_sorteio = {
                'numero': self.total_sorteios,
                'sorteio': sorteio,
                'resultados': resultados_jogos,
                'melhor': melhor_acerto_sorteio,
                'premio': premio
            }
            self.historico_sorteios.append(info_sorteio)
            
            self.root.after(0, self.atualizar_interface_simulacao, 
                          melhor_resultado, total_quadras, total_quinas, total_senas, custo_por_sorteio)
            
            self.root.after(0, self.adicionar_linha_historico, info_sorteio)
            
            if self.total_sorteios % 100 == 0:
                print(f"Sorteio #{self.total_sorteios}: Melhor={melhor_resultado} | Q={total_quadras} Qi={total_quinas} S={total_senas}")
            
            if parar:
                print(f"\nCONDIÇÃO DE PARADA! {premio}")
                self.simulacao_ativa = False
                self.root.after(0, self.exibir_resultado_simulacao, 
                              melhor_resultado, total_quadras, total_quinas, total_senas, custo_por_sorteio)
                break
            
            time.sleep(0.001)
        
        if self.simulacao_ativa:
            self.simulacao_ativa = False
            self.root.after(0, self.exibir_resultado_simulacao, 
                          melhor_resultado, total_quadras, total_quinas, total_senas, custo_por_sorteio)
    
    def atualizar_interface_simulacao(self, melhor, quadras, quinas, senas, custo):
        total_gasto = self.total_sorteios * custo
        texto = f"Sorteios: {self.total_sorteios:,} | Gasto: R$ {total_gasto:,.2f}\n"
        texto += f"Melhor: {melhor} acertos\n"
        texto += f"Quadras: {quadras} | Quinas: {quinas} | Senas: {senas}"
        
        self.label_stats_sim.config(text=texto)
    
    def adicionar_linha_historico(self, info):
        if len(self.historico_sorteios) > 500:
            self.text_historico.delete(1.0, tk.END)
            for sorteio in self.historico_sorteios[-500:]:
                self.escrever_linha_historico(sorteio)
        else:
            self.escrever_linha_historico(info)
        
        self.text_historico.see(tk.END)
    
    def escrever_linha_historico(self, info):
        # Calcula probabilidade total dos jogos
        prob_total = sum(j['probabilidade'] for j in self.jogos_simulacao)
        
        linha = f"#{info['numero']:6d} | {str(info['sorteio']):30s} | "
        linha += f"Acertos: {info['resultados']} | Melhor: {info['melhor']}"
        
        if info['premio']:
            linha += f" | {info['premio']}"
        
        linha += f" | Prob: {prob_total:.8f}%"
        linha += "\n"
        
        self.text_historico.insert(tk.END, linha)
    
    def parar_simulacao(self):
        self.simulacao_ativa = False
        print("\nSIMULAÇÃO INTERROMPIDA!")
    
    def limpar_historico(self):
        self.historico_sorteios = []
        self.total_sorteios = 0
        self.text_historico.delete(1.0, tk.END)
        self.label_stats_sim.config(text="Histórico limpo.")
        print("\nHISTÓRICO LIMPO!")
    
    def exibir_resultado_simulacao(self, melhor, quadras, quinas, senas, custo_sorteio):
        total_gasto = self.total_sorteios * custo_sorteio
        
        resultado = "SIMULAÇÃO FINALIZADA!\n\n"
        resultado += f"Total de sorteios: {self.total_sorteios:,}\n"
        resultado += f"Custo por sorteio: R$ {custo_sorteio:.2f}\n"
        resultado += f"💰 TOTAL GASTO: R$ {total_gasto:,.2f}\n\n"
        resultado += f"Melhor resultado: {melhor} acertos\n\n"
        resultado += f"Prêmios obtidos:\n"
        resultado += f"  • Quadras: {quadras}\n"
        resultado += f"  • Quinas: {quinas}\n"
        resultado += f"  • Senas: {senas}\n\n"
        
        if senas > 0:
            custo_para_sena = total_gasto / senas
            resultado += f"🏆 SENA em {senas} vez(es)!\n"
            resultado += f"Custo médio por SENA: R$ {custo_para_sena:,.2f}\n"
            resultado += f"Sorteios até primeira SENA: ~{self.total_sorteios // max(1, senas):,}"
        elif quinas > 0:
            custo_para_quina = total_gasto / quinas
            resultado += f"🎊 QUINA em {quinas} vez(es)!\n"
            resultado += f"Custo médio por QUINA: R$ {custo_para_quina:,.2f}"
        elif quadras > 0:
            custo_para_quadra = total_gasto / quadras
            resultado += f"🎉 QUADRA em {quadras} vez(es)!\n"
            resultado += f"Custo médio por QUADRA: R$ {custo_para_quadra:,.2f}"
        else:
            resultado += f"😢 Sem prêmios nesta simulação."
        
        messagebox.showinfo("Resultado da Simulação", resultado)
        print("\n" + "="*80)
        print(resultado)
        print("="*80)

def main():
    print("="*80)
    print("SIMULADOR DE MEGA-SENA")
    print("="*80)
    print("\nInstruções:")
    print("\n[SORTEIO MANUAL]")
    print("• Digite dezenas ou use Seletor Visual")
    print("• Botão 'Jogo Aleatório' cria jogo automático")
    print("• Sorteio a cada 5 segundos")
    print("\n[SIMULAÇÃO AUTOMÁTICA]")
    print("• Adicione vários jogos")
    print("• Configure quantidade e condições de parada")
    print("• Veja quanto gastaria para ganhar!")
    print("="*80 + "\n")
    
    root = tk.Tk()
    app = MegaSenaSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()