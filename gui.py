import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import massdm_api
import os
import time
import json


class MassDMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asgard Mass DM Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2f3136")

        # Estado do envio
        self.running = False
        self.paused = False

        # Carregar configurações iniciais
        self.config = self.load_config()

        # Labels
        tk.Label(
            self.root,
            text="Configurações",
            font=("Arial", 14),
            bg="#2f3136",
            fg="white",
        ).pack(pady=5)

        # Campos de configuração
        config_frame = tk.Frame(self.root, bg="#2f3136")
        config_frame.pack(pady=5)

        tk.Label(
            config_frame,
            text="Delay entre mensagens (segundos):",
            bg="#2f3136",
            fg="white",
        ).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_delay_msg = tk.Entry(config_frame, width=10)
        self.entry_delay_msg.grid(row=0, column=1, padx=5)
        self.entry_delay_msg.insert(
            0, str(self.config.get("DELAY_BETWEEN_MESSAGES", 180))
        )

        tk.Label(
            config_frame, text="Delay entre lotes (segundos):", bg="#2f3136", fg="white"
        ).grid(row=1, column=0, sticky="w", padx=5)
        self.entry_delay_batch = tk.Entry(config_frame, width=10)
        self.entry_delay_batch.grid(row=1, column=1, padx=5)
        self.entry_delay_batch.insert(
            0, str(self.config.get("DELAY_BETWEEN_BATCHES", 1800))
        )

        tk.Label(config_frame, text="Tamanho do Lote:", bg="#2f3136", fg="white").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.entry_batch_size = tk.Entry(config_frame, width=10)
        self.entry_batch_size.grid(row=2, column=1, padx=5)
        self.entry_batch_size.insert(0, str(self.config.get("BATCH_SIZE", 20)))

        tk.Button(config_frame, text="Salvar", command=self.save_config).grid(
            row=0, column=2, rowspan=3, padx=10
        )

        # Botões principais
        btn_frame = tk.Frame(self.root, bg="#2f3136")
        btn_frame.pack(pady=10)

        self.btn_scrape = tk.Button(
            btn_frame, text="Raspar Membros", width=20, command=self.start_scrape
        )
        self.btn_scrape.pack(side="left", padx=5)

        self.btn_send = tk.Button(
            btn_frame, text="Enviar Mensagens", width=20, command=self.start_send
        )
        self.btn_send.pack(side="left", padx=5)

        # Status e barra de progresso
        self.status_label = tk.Label(
            self.root,
            text="Status: Parado",
            font=("Arial", 12),
            bg="#2f3136",
            fg="lightgray",
        )
        self.status_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=500, mode="determinate"
        )
        self.progress_bar.pack(pady=5)

        # Área de Logs
        self.log_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=12,
            bg="#1e1f22",
            fg="lightgreen",
            font=("Courier", 10),
        )
        self.log_area.pack(pady=10)

        # Botões de controle
        control_frame = tk.Frame(self.root, bg="#2f3136")
        control_frame.pack(pady=5)

        self.btn_pause = tk.Button(
            control_frame,
            text="Pausar",
            width=15,
            state=tk.DISABLED,
            command=self.pause_send,
        )
        self.btn_pause.pack(side="left", padx=5)

        self.btn_resume = tk.Button(
            control_frame,
            text="Continuar",
            width=15,
            state=tk.DISABLED,
            command=self.resume_send,
        )
        self.btn_resume.pack(side="left", padx=5)

        self.btn_stop = tk.Button(
            control_frame,
            text="Parar",
            width=15,
            state=tk.DISABLED,
            command=self.stop_send,
        )
        self.btn_stop.pack(side="left", padx=5)

        exit_button = tk.Button(
            self.root,
            text="Sair",
            width=15,
            bg="red",
            fg="white",
            command=self.exit_app,
        )
        exit_button.pack(pady=10)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")
        self.root.update_idletasks()

    def load_config(self):
        try:
            with open("config/app_settings.json") as f:
                return json.load(f)
        except Exception as e:
            print(f"[INFO] Usando configurações padrão. Arquivo não encontrado: {e}")
            return {
                "DELAY_BETWEEN_MESSAGES": 180,  # 3 minutos
                "DELAY_BETWEEN_BATCHES": 1800,  # 30 minutos
                "BATCH_SIZE": 20,
            }

    def save_config(self):
        try:
            DELAY_BETWEEN_MESSAGES = int(self.entry_delay_msg.get())
            DELAY_BETWEEN_BATCHES = int(self.entry_delay_batch.get())
            BATCH_SIZE = int(self.entry_batch_size.get())

            with open("config/app_settings.json", "w") as f:
                json.dump(
                    {
                        "DELAY_BETWEEN_MESSAGES": DELAY_BETWEEN_MESSAGES,
                        "DELAY_BETWEEN_BATCHES": DELAY_BETWEEN_BATCHES,
                        "BATCH_SIZE": BATCH_SIZE,
                    },
                    f,
                    indent=4,
                )

            messagebox.showinfo("Sucesso", "Configurações salvas!")
        except:
            messagebox.showerror("Erro", "Valores inválidos nos campos.")

    def start_scrape(self):
        def run():
            self.log("[INFO] Iniciando raspagem de membros...")

            all_users = set()
            for server in massdm_api.SERVERS:
                guild_id = server["guild_id"]
                invite_code = server["invite_code"]

                self.log(f"[+] Entrando no servidor {guild_id}...")
                if massdm_api.join_guild(invite_code):
                    self.log(f"[✓] Entrou no servidor {guild_id}")
                else:
                    self.log(f"[!] Falha ao entrar no servidor {guild_id}")

                time.sleep(5)

                users = massdm_api.scrape_users_from_channels(server["channel_ids"])
                all_users.update(users)
                time.sleep(5)

            with open("members.txt", "w", encoding="utf-8") as file:
                for user in sorted(all_users):
                    file.write(user + "\n")

            self.log(f"[✓] {len(all_users)} membros salvos em 'members.txt'.")
            self.update_status("Pronto")

        threading.Thread(target=run).start()

    def start_send(self):
        if self.running:
            self.log("[!] Já há um envio em andamento.")
            return

        self.running = True
        self.paused = False
        self.update_status("Rodando")

        self.btn_pause.config(state=tk.NORMAL)
        self.btn_resume.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        def run():
            try:
                with open("members.txt", "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                self.log("[ERRO] Arquivo 'members.txt' não encontrado.")
                messagebox.showerror("Erro", "members.txt não encontrado.")
                self.stop_send()
                return

            total = len(lines)
            count = 0

            # Carregar configurações da interface
            config = self.load_config()
            DELAY_BETWEEN_MESSAGES = config["DELAY_BETWEEN_MESSAGES"]
            DELAY_BETWEEN_BATCHES = config["DELAY_BETWEEN_BATCHES"]
            BATCH_SIZE = config["BATCH_SIZE"]

            tokens = massdm_api.tokens
            num_tokens = len(tokens)

            success_list = []
            failed_list = []

            contacted = set()
            if os.path.exists("contacted.txt"):
                with open("contacted.txt", "r") as f:
                    contacted.update(line.strip() for line in f)

            self.log(
                f"[✓] Iniciando envio para {total} usuários com {num_tokens} contas"
            )

            self.progress_bar["maximum"] = total
            self.progress_bar["value"] = 0

            for i, line in enumerate(lines):
                if not self.running:
                    break
                while self.paused:
                    time.sleep(1)

                user_id = line.strip().split(" - ")[0]
                if user_id in contacted:
                    self.log(f"[!] PULADO - Já contatado: {user_id}")
                    continue

                token_index = (i % num_tokens) if num_tokens > 0 else 0
                current_token = tokens[token_index]

                self.log(
                    f"[+] Usando conta {token_index + 1} para enviar para {user_id}"
                )

                if massdm_api.send_embed(user_id, current_token):
                    count += 1
                    success_list.append(user_id)
                    contacted.add(user_id)

                percent = int((i + 1) / total * 100)
                self.progress_bar["value"] = i + 1
                self.root.update_idletasks()

                time.sleep(DELAY_BETWEEN_MESSAGES)

                if (i + 1) % BATCH_SIZE == 0 and i > 0:
                    self.log("[!] Aguardando antes do próximo lote...")
                    time.sleep(DELAY_BETWEEN_BATCHES)

            # Salva relatório final
            with open("contacted.txt", "w") as f:
                for user in sorted(contacted):
                    f.write(user + "\n")

            with open("relatorio_envios.txt", "w") as f:
                f.write("=== RELATÓRIO DE ENVIO ===\n")
                f.write(f"Total de membros: {total}\n")
                f.write(f"Enviado com sucesso: {len(success_list)}\n")
                f.write(f"Falhas: {len(failed_list)}\n\n")
                f.write("SUCESSO:\n")
                for user in success_list:
                    f.write(f"{user}\n")
                f.write("\nFALHAS:\n")
                for user in failed_list:
                    f.write(f"{user}\n")

            self.log(f"[✓] Total de mensagens enviadas: {count}")
            self.stop_send()
            messagebox.showinfo("Concluído", f"Mensagens enviadas: {count}")

        self.current_thread = threading.Thread(target=run)
        self.current_thread.start()

    def pause_send(self):
        self.paused = True
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_resume.config(state=tk.NORMAL)
        self.log("[!] Envio pausado.")
        self.update_status("Pausado")

    def resume_send(self):
        self.paused = False
        self.btn_pause.config(state=tk.NORMAL)
        self.btn_resume.config(state=tk.DISABLED)
        self.log("[✓] Envio retomado.")
        self.update_status("Rodando")

    def stop_send(self):
        self.running = False
        self.paused = False
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_resume.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.DISABLED)
        self.update_status("Parado")

    def exit_app(self):
        self.stop_send()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MassDMApp(root)
    root.mainloop()
