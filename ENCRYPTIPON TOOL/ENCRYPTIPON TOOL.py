import argparse
import tkinter as tk
from tkinter import ttk

from cipher import decrypt, encrypt


class SecretAgentChatbox(tk.Tk):
    """Dark chat-style interface for the SPN Cipher."""

    def __init__(self):
        super().__init__()
        self.title("SPN Cipher - Secret Agent Chatbox")
        self.geometry("900x680")
        self.minsize(760, 580)

        self.key = tk.StringVar(value="")
        self.rounds = tk.IntVar(value=2)
        self.status = tk.StringVar(value="Channel secure. Awaiting transmission.")

        self._configure_style()
        self._build_ui()
        self._add_agent_message(
            "🕵️ Agent SPN online.\n"
            "Send a message, choose Encrypt or Decrypt, and I will secure the transmission."
        )

    def _configure_style(self):
        self.configure(bg="#0b1020")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Root.TFrame", background="#0b1020")
        style.configure("Panel.TFrame", background="#111827")
        style.configure("Header.TLabel", background="#0b1020", foreground="#e5f9ff", font=("Helvetica", 24, "bold"))
        style.configure("Subheader.TLabel", background="#0b1020", foreground="#8dd8ff", font=("Helvetica", 11))
        style.configure("Field.TLabel", background="#111827", foreground="#cbd5e1", font=("Helvetica", 10, "bold"))
        style.configure("Status.TLabel", background="#172033", foreground="#92f7c8", padding=(12, 8))
        style.configure("Encrypt.TButton", background="#16a34a", foreground="#06130b", font=("Helvetica", 11, "bold"), padding=(14, 8))
        style.map("Encrypt.TButton", background=[("active", "#22c55e")])
        style.configure("Decrypt.TButton", background="#38bdf8", foreground="#06121f", font=("Helvetica", 11, "bold"), padding=(14, 8))
        style.map("Decrypt.TButton", background=[("active", "#7dd3fc")])
        style.configure("Ghost.TButton", background="#263244", foreground="#e2e8f0", padding=(12, 8))
        style.map("Ghost.TButton", background=[("active", "#334155")])

    def _build_ui(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=22)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root, style="Root.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="🔐 SPN Cipher Chatbox", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Shift-Permutation-Noise encrypted messages for secret-agent style communication ✦ ∴ ⊕",
            style="Subheader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        chat_panel = ttk.Frame(root, style="Panel.TFrame", padding=14)
        chat_panel.grid(row=1, column=0, sticky="nsew")
        chat_panel.columnconfigure(0, weight=1)
        chat_panel.rowconfigure(0, weight=1)

        self.chat_log = tk.Text(
            chat_panel,
            bg="#070b16",
            fg="#dbeafe",
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
            padx=16,
            pady=16,
            state="disabled",
            font=("Menlo", 12),
        )
        self.chat_log.grid(row=0, column=0, sticky="nsew")
        self.chat_log.tag_configure("agent", foreground="#92f7c8", spacing3=10)
        self.chat_log.tag_configure("user", foreground="#8dd8ff", spacing3=10)
        self.chat_log.tag_configure("result", foreground="#fef08a", spacing3=14)
        self.chat_log.tag_configure("error", foreground="#fca5a5", spacing3=10)

        scrollbar = ttk.Scrollbar(chat_panel, orient="vertical", command=self.chat_log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_log.configure(yscrollcommand=scrollbar.set)

        controls = ttk.Frame(root, style="Panel.TFrame", padding=14)
        controls.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=0)

        ttk.Label(controls, text="Message", style="Field.TLabel").grid(row=0, column=0, sticky="w")
        self.message_text = tk.Text(
            controls,
            height=4,
            bg="#0f172a",
            fg="#eef2ff",
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
            padx=10,
            pady=10,
            font=("Helvetica", 12),
        )
        self.message_text.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(6, 12))

        ttk.Label(controls, text="Key", style="Field.TLabel").grid(row=2, column=0, sticky="w")
        key_entry = tk.Entry(
            controls,
            textvariable=self.key,
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#ffffff",
            relief="flat",
            width=22,
            font=("Helvetica", 12),
        )
        key_entry.grid(row=3, column=0, sticky="ew", padx=(0, 12), ipady=8)

        ttk.Label(controls, text="Rounds", style="Field.TLabel").grid(row=2, column=1, sticky="w")
        rounds_spinbox = tk.Spinbox(
            controls,
            from_=1,
            to=5,
            textvariable=self.rounds,
            width=6,
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#ffffff",
            relief="flat",
            justify="center",
            font=("Helvetica", 12),
        )
        rounds_spinbox.grid(row=3, column=1, sticky="w", padx=(0, 12), ipady=7)

        ttk.Button(controls, text="Encrypt 🔒", style="Encrypt.TButton", command=self.encrypt_message).grid(
            row=3, column=2, sticky="e", padx=(0, 8)
        )
        ttk.Button(controls, text="Decrypt 🔓", style="Decrypt.TButton", command=self.decrypt_message).grid(
            row=3, column=3, sticky="e", padx=(0, 8)
        )
        ttk.Button(controls, text="Clear", style="Ghost.TButton", command=self.clear_chat).grid(row=3, column=4, sticky="e")

        ttk.Label(root, textvariable=self.status, style="Status.TLabel").grid(row=3, column=0, sticky="ew", pady=(14, 0))

    def encrypt_message(self):
        self._process_message("encrypt")

    def decrypt_message(self):
        self._process_message("decrypt")

    def clear_chat(self):
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        self.chat_log.configure(state="disabled")
        self.status.set("Channel cleared. Ready for the next mission.")

    def _process_message(self, action):
        message = self._get_message()
        key = self.key.get()
        rounds = self._get_rounds()
        use_base64 = True

        self._add_user_message(message or "(empty message)")

        try:
            if action == "encrypt":
                result = encrypt(message, key, rounds=rounds, use_base64=use_base64)
                heading = "🔒 Encrypted transmission"
                self.status.set("Encrypted message ready.")
            else:
                result = decrypt(message, key, rounds=rounds, use_base64=use_base64)
                heading = "🔓 Decrypted message"
                self.status.set("Decrypted message ready.")
        except ValueError as error:
            self._add_error_message(str(error))
            self.status.set(str(error))
            return

        self._add_result_message(f"{heading}\n{result}")
        self.message_text.delete("1.0", "end")

    def _get_message(self):
        return self.message_text.get("1.0", "end-1c")

    def _get_rounds(self):
        try:
            return max(1, int(self.rounds.get()))
        except (TypeError, ValueError):
            return 1

    def _add_agent_message(self, message):
        self._append_chat(f"AGENT 007\n{message}\n\n", "agent")

    def _add_user_message(self, message):
        self._append_chat(f"YOU\n{message}\n\n", "user")

    def _add_result_message(self, message):
        self._append_chat(f"SPN RESULT\n{message}\n\n", "result")

    def _add_error_message(self, message):
        self._append_chat(f"ALERT\n{message}\n\n", "error")

    def _append_chat(self, message, tag):
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", message, tag)
        self.chat_log.see("end")
        self.chat_log.configure(state="disabled")


def run_cli():
    """Simple terminal interface for the SPN Cipher."""
    print("=== SPN Cipher (Shift-Permutation-Noise) ===")
    choice = input("Choose Encrypt or Decrypt (e/d): ").strip().lower()
    message = input("Enter message: ")
    key = input("Enter key: ")

    try:
        rounds = int(input("Rounds (default 1): ") or "1")
    except ValueError:
        rounds = 1

    use_base64 = True

    try:
        if choice.startswith("d"):
            result = decrypt(message, key, rounds=rounds, use_base64=use_base64)
            print("\nDecrypted message:")
        else:
            result = encrypt(message, key, rounds=rounds, use_base64=use_base64)
            print("\nEncrypted message:")
        print(result)
    except ValueError as error:
        print(f"\nError: {error}")


def main():
    parser = argparse.ArgumentParser(description="SPN Cipher secret-agent chatbox")
    parser.add_argument("--cli", action="store_true", help="run in terminal mode")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        app = SecretAgentChatbox()
        app.mainloop()


if __name__ == "__main__":
    main()
