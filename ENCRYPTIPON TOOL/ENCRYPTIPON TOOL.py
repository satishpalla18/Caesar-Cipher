"""Secret Agent Chatbox GUI and CLI for the SPN Cipher project."""

import argparse
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from cipher import brute_force_caesar
from cipher import caesar_cipher
from cipher import decrypt
from cipher import encrypt


CIPHER_SPN = "SPN Cipher"
CIPHER_CAESAR = "Caesar Cipher"


THEMES = {
    "Dark": {
        "root": "#0b1020",
        "panel": "#111827",
        "chat": "#070b16",
        "input": "#0f172a",
        "text": "#e5e7eb",
        "muted": "#9ca3af",
        "heading": "#e5f9ff",
        "accent": "#38bdf8",
        "agent": "#92f7c8",
        "user": "#8dd8ff",
        "result": "#fef08a",
        "error": "#fca5a5",
        "status": "#172033",
        "button": "#263244",
        "button_hover": "#334155",
        "encrypt": "#16a34a",
        "encrypt_hover": "#22c55e",
        "decrypt": "#38bdf8",
        "decrypt_hover": "#7dd3fc",
    },
    "Light": {
        "root": "#eef2ff",
        "panel": "#ffffff",
        "chat": "#f8fafc",
        "input": "#eef2ff",
        "text": "#111827",
        "muted": "#475569",
        "heading": "#0f172a",
        "accent": "#2563eb",
        "agent": "#047857",
        "user": "#1d4ed8",
        "result": "#854d0e",
        "error": "#b91c1c",
        "status": "#e0f2fe",
        "button": "#dbeafe",
        "button_hover": "#bfdbfe",
        "encrypt": "#86efac",
        "encrypt_hover": "#bbf7d0",
        "decrypt": "#93c5fd",
        "decrypt_hover": "#bfdbfe",
    },
}


class SecretAgentChatbox(tk.Tk):
    """Modern Tkinter interface for encryption and decryption."""

    def __init__(self):
        """Create the app window and initialize Tkinter variables."""
        super().__init__()
        self.title("SPN Cipher - Secret Agent Chatbox")
        self.geometry("980x720")
        self.minsize(820, 620)

        self.cipher_type = tk.StringVar(value=CIPHER_SPN)
        self.key = tk.StringVar(value="")
        self.caesar_shift = tk.StringVar(value="3")
        self.rounds = tk.StringVar(value="2")
        self.use_base64 = tk.BooleanVar(value=True)
        self.theme_name = tk.StringVar(value="Dark")
        self.status = tk.StringVar(value="Channel secure. Awaiting transmission.")

        self.last_output = ""
        self.chat_entries = []
        self.buttons = []

        self._configure_window()
        self._build_ui()
        self._apply_theme()
        self._bind_shortcuts()
        self._update_cipher_controls()
        self._add_agent_message(
            "Agent SPN online.\n"
            "Choose a cipher, enter a message, and press Enter to encrypt."
        )

    def _configure_window(self):
        """Configure the root grid for responsive resizing."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _build_ui(self):
        """Build all widgets."""
        self.root_frame = ttk.Frame(self, style="Root.TFrame", padding=22)
        self.root_frame.grid(row=0, column=0, sticky="nsew")
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(1, weight=1)

        self._build_header()
        self._build_chat_panel()
        self._build_controls()
        self._build_status_bar()

    def _build_header(self):
        """Build the title area."""
        self.header_frame = ttk.Frame(self.root_frame, style="Root.TFrame")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.header_frame.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(
            self.header_frame,
            text="SPN Cipher Chatbox",
            style="Header.TLabel",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ttk.Label(
            self.header_frame,
            text="Secret-agent encryption console with SPN and Caesar modes",
            style="Subheader.TLabel",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(3, 0))

        self.theme_button = ttk.Button(
            self.header_frame,
            text="Light Mode",
            style="Ghost.TButton",
            command=self.toggle_theme,
        )
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e")
        self.buttons.append(self.theme_button)

    def _build_chat_panel(self):
        """Build the scrollable chat area."""
        self.chat_panel = ttk.Frame(
            self.root_frame,
            style="Panel.TFrame",
            padding=14,
        )
        self.chat_panel.grid(row=1, column=0, sticky="nsew")
        self.chat_panel.columnconfigure(0, weight=1)
        self.chat_panel.rowconfigure(0, weight=1)

        self.chat_log = tk.Text(
            self.chat_panel,
            relief="flat",
            wrap="word",
            padx=18,
            pady=18,
            state="disabled",
            font=("Menlo", 12),
            spacing1=4,
            spacing2=3,
            spacing3=14,
        )
        self.chat_log.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(
            self.chat_panel,
            orient="vertical",
            command=self.chat_log.yview,
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_log.configure(yscrollcommand=self.scrollbar.set)

    def _build_controls(self):
        """Build message, options, and action controls."""
        self.controls = ttk.Frame(
            self.root_frame,
            style="Panel.TFrame",
            padding=14,
        )
        self.controls.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        self.controls.columnconfigure(0, weight=1)

        self.message_label = ttk.Label(
            self.controls,
            text="Message",
            style="Field.TLabel",
        )
        self.message_label.grid(row=0, column=0, columnspan=6, sticky="w")

        self.message_text = tk.Text(
            self.controls,
            height=4,
            relief="flat",
            wrap="word",
            padx=10,
            pady=10,
            font=("Helvetica", 12),
            undo=True,
        )
        self.message_text.grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="ew",
            pady=(6, 12),
        )

        self._build_option_row()
        self._build_button_row()

    def _build_option_row(self):
        """Build cipher option controls."""
        self.cipher_label = ttk.Label(
            self.controls,
            text="Cipher",
            style="Field.TLabel",
        )
        self.cipher_label.grid(row=2, column=0, sticky="w")

        self.cipher_menu = ttk.Combobox(
            self.controls,
            textvariable=self.cipher_type,
            values=(CIPHER_SPN, CIPHER_CAESAR),
            state="readonly",
            width=18,
        )
        self.cipher_menu.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        self.cipher_menu.bind(
            "<<ComboboxSelected>>",
            lambda _event: self._update_cipher_controls(),
        )

        self.key_label = ttk.Label(self.controls, text="Key", style="Field.TLabel")
        self.key_label.grid(row=2, column=1, sticky="w")

        self.key_entry = ttk.Entry(self.controls, textvariable=self.key, width=18)
        self.key_entry.grid(row=3, column=1, sticky="ew", padx=(0, 10))

        self.shift_label = ttk.Label(
            self.controls,
            text="Shift",
            style="Field.TLabel",
        )
        self.shift_label.grid(row=2, column=2, sticky="w")

        self.shift_spinbox = ttk.Spinbox(
            self.controls,
            from_=0,
            to=25,
            textvariable=self.caesar_shift,
            width=7,
            justify="center",
        )
        self.shift_spinbox.grid(row=3, column=2, sticky="ew", padx=(0, 10))

        self.rounds_label = ttk.Label(
            self.controls,
            text="Rounds",
            style="Field.TLabel",
        )
        self.rounds_label.grid(row=2, column=3, sticky="w")

        self.rounds_spinbox = ttk.Spinbox(
            self.controls,
            from_=1,
            to=5,
            textvariable=self.rounds,
            width=7,
            justify="center",
        )
        self.rounds_spinbox.grid(row=3, column=3, sticky="ew", padx=(0, 10))

        self.base64_check = ttk.Checkbutton(
            self.controls,
            text="Base64",
            variable=self.use_base64,
        )
        self.base64_check.grid(row=3, column=4, sticky="w", padx=(0, 10))

    def _build_button_row(self):
        """Build action buttons."""
        actions = ttk.Frame(self.controls, style="Panel.TFrame")
        actions.grid(row=4, column=0, columnspan=6, sticky="ew", pady=(12, 0))
        actions.columnconfigure(6, weight=1)

        button_specs = [
            ("Encrypt", "Encrypt.TButton", self.encrypt_message),
            ("Decrypt", "Decrypt.TButton", self.decrypt_message),
            ("Brute Force", "Ghost.TButton", self.brute_force_decrypt),
            ("Copy Output", "Ghost.TButton", self.copy_output),
            ("Clear Input", "Ghost.TButton", self.clear_input),
            ("Clear Chat", "Ghost.TButton", self.clear_chat),
            ("Export Chat", "Ghost.TButton", self.export_chat),
        ]

        for column, (text, style, command) in enumerate(button_specs):
            button = ttk.Button(
                actions,
                text=text,
                style=style,
                command=command,
            )
            button.grid(row=0, column=column, sticky="w", padx=(0, 8))
            self.buttons.append(button)

    def _build_status_bar(self):
        """Build the bottom status bar."""
        self.status_label = ttk.Label(
            self.root_frame,
            textvariable=self.status,
            style="Status.TLabel",
        )
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(14, 0))

    def _configure_style(self):
        """Create ttk styles for the active theme."""
        colors = THEMES[self.theme_name.get()]
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Root.TFrame", background=colors["root"])
        style.configure("Panel.TFrame", background=colors["panel"])
        style.configure(
            "Header.TLabel",
            background=colors["root"],
            foreground=colors["heading"],
            font=("Helvetica", 24, "bold"),
        )
        style.configure(
            "Subheader.TLabel",
            background=colors["root"],
            foreground=colors["accent"],
            font=("Helvetica", 11),
        )
        style.configure(
            "Field.TLabel",
            background=colors["panel"],
            foreground=colors["muted"],
            font=("Helvetica", 10, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=colors["status"],
            foreground=colors["agent"],
            padding=(12, 8),
        )
        style.configure(
            "TEntry",
            fieldbackground=colors["input"],
            foreground=colors["text"],
            insertcolor=colors["text"],
            borderwidth=0,
        )
        style.configure(
            "TSpinbox",
            fieldbackground=colors["input"],
            foreground=colors["text"],
            insertcolor=colors["text"],
            borderwidth=0,
        )
        style.configure(
            "TCombobox",
            fieldbackground=colors["input"],
            foreground=colors["text"],
            arrowcolor=colors["text"],
        )
        style.configure(
            "TCheckbutton",
            background=colors["panel"],
            foreground=colors["text"],
        )
        style.map(
            "TCheckbutton",
            background=[("active", colors["panel"])],
            foreground=[("active", colors["heading"])],
        )
        style.configure(
            "Encrypt.TButton",
            background=colors["encrypt"],
            foreground="#06130b",
            font=("Helvetica", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Encrypt.TButton", background=[("active", colors["encrypt_hover"])])
        style.configure(
            "Decrypt.TButton",
            background=colors["decrypt"],
            foreground="#06121f",
            font=("Helvetica", 10, "bold"),
            padding=(12, 8),
        )
        style.map("Decrypt.TButton", background=[("active", colors["decrypt_hover"])])
        style.configure(
            "Ghost.TButton",
            background=colors["button"],
            foreground=colors["text"],
            padding=(12, 8),
        )
        style.map("Ghost.TButton", background=[("active", colors["button_hover"])])

    def _apply_theme(self):
        """Apply colors to ttk and classic Tk widgets."""
        colors = THEMES[self.theme_name.get()]
        self._configure_style()
        self.configure(bg=colors["root"])

        self.chat_log.configure(
            bg=colors["chat"],
            fg=colors["text"],
            insertbackground=colors["text"],
            selectbackground=colors["accent"],
        )
        self.chat_log.tag_configure(
            "agent",
            foreground=colors["agent"],
            lmargin1=8,
            lmargin2=8,
            rmargin=80,
        )
        self.chat_log.tag_configure(
            "user",
            foreground=colors["user"],
            lmargin1=60,
            lmargin2=60,
            rmargin=12,
            justify="right",
        )
        self.chat_log.tag_configure(
            "result",
            foreground=colors["result"],
            lmargin1=8,
            lmargin2=8,
            rmargin=40,
        )
        self.chat_log.tag_configure(
            "error",
            foreground=colors["error"],
            lmargin1=8,
            lmargin2=8,
            rmargin=40,
        )

        self.message_text.configure(
            bg=colors["input"],
            fg=colors["text"],
            insertbackground=colors["text"],
            selectbackground=colors["accent"],
        )
        self.theme_button.configure(
            text="Dark Mode" if self.theme_name.get() == "Light" else "Light Mode"
        )

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts for the message input."""
        self.message_text.bind("<Return>", self._handle_enter_key)
        self.message_text.bind("<Shift-Return>", self._handle_shift_enter_key)

    def _handle_enter_key(self, _event):
        """Encrypt when Enter is pressed."""
        self.encrypt_message()
        return "break"

    def _handle_shift_enter_key(self, _event):
        """Insert a newline when Shift+Enter is pressed."""
        self.message_text.insert("insert", "\n")
        return "break"

    def toggle_theme(self):
        """Switch between dark and light themes."""
        next_theme = "Light" if self.theme_name.get() == "Dark" else "Dark"
        self.theme_name.set(next_theme)
        self._apply_theme()
        self.status.set(f"{next_theme} theme active.")

    def encrypt_message(self):
        """Encrypt the current input message."""
        self._process_message("encrypt")

    def decrypt_message(self):
        """Decrypt the current input message."""
        self._process_message("decrypt")

    def brute_force_decrypt(self):
        """Show all Caesar decryptions for the current message."""
        message = self._get_message()
        self._add_user_message(message or "(empty message)")

        try:
            if self.cipher_type.get() != CIPHER_CAESAR:
                raise ValueError("Brute Force Decrypt is only for Caesar Cipher.")

            self._set_loading("Brute forcing Caesar shifts...")
            results = brute_force_caesar(message)
        except ValueError as error:
            self._add_error_message(str(error))
            self.status.set(str(error))
            return

        output = "\n".join(
            f"Shift {item['shift']:02d}: {item['text']}" for item in results
        )
        self._add_result_message("Caesar brute force results", output)
        self.last_output = output
        self.status.set("Brute force results ready.")

    def copy_output(self):
        """Copy the latest result to the clipboard."""
        if not self.last_output:
            self.status.set("No output to copy.")
            return

        self.clipboard_clear()
        self.clipboard_append(self.last_output)
        self.status.set("Output copied to clipboard.")

    def clear_input(self):
        """Clear only the message input box."""
        self.message_text.delete("1.0", "end")
        self.status.set("Input cleared.")

    def clear_chat(self):
        """Clear the chat history."""
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        self.chat_log.configure(state="disabled")
        self.chat_entries.clear()
        self.last_output = ""
        self.status.set("Channel cleared. Ready for the next mission.")

    def export_chat(self):
        """Export chat history to a text file."""
        if not self.chat_entries:
            self.status.set("No chat history to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export chat",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_path:
            self.status.set("Export canceled.")
            return

        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n\n".join(self.chat_entries))
        except OSError as error:
            self._add_error_message(f"Could not export chat: {error}")
            self.status.set("Export failed.")
            return

        self.status.set(f"Chat exported to {file_path}")

    def _process_message(self, action):
        """Run encrypt or decrypt with validation and friendly errors."""
        message = self._get_message()
        self._add_user_message(message or "(empty message)")

        try:
            self._validate_input(action)
            self._set_loading("Encrypting..." if action == "encrypt" else "Decrypting...")
            result = self._run_cipher_action(action, message)
        except ValueError as error:
            self._add_error_message(str(error))
            self.status.set(str(error))
            return
        except Exception as error:
            self._add_error_message(f"Unexpected error: {error}")
            self.status.set("Unexpected error occurred.")
            return

        heading = "Encrypted transmission" if action == "encrypt" else "Decrypted message"
        self._add_result_message(heading, result)
        self.last_output = result
        self.message_text.delete("1.0", "end")
        self.status.set(f"{heading} ready.")

    def _run_cipher_action(self, action, message):
        """Dispatch the selected cipher action."""
        if self.cipher_type.get() == CIPHER_CAESAR:
            mode = "encrypt" if action == "encrypt" else "decrypt"
            return caesar_cipher(message, self.caesar_shift.get(), mode=mode)

        if action == "encrypt":
            return encrypt(
                message,
                self.key.get(),
                rounds=self.rounds.get(),
                use_base64=self.use_base64.get(),
            )

        return decrypt(
            message,
            self.key.get(),
            rounds=self.rounds.get(),
            use_base64=self.use_base64.get(),
        )

    def _validate_input(self, action):
        """Validate GUI fields before processing."""
        message = self._get_message()
        if message == "":
            raise ValueError("Message cannot be empty.")

        if self.cipher_type.get() == CIPHER_CAESAR:
            caesar_cipher(message, self.caesar_shift.get(), mode=action)
            return

        if self.key.get() == "":
            raise ValueError("Key cannot be empty.")

        rounds = self._get_rounds()
        if not 1 <= rounds <= 5:
            raise ValueError("Rounds must be between 1 and 5.")

    def _get_rounds(self):
        """Read rounds as an integer."""
        try:
            return int(self.rounds.get())
        except (TypeError, ValueError) as error:
            raise ValueError("Rounds must be a number from 1 to 5.") from error

    def _get_message(self):
        """Return the current message input."""
        return self.message_text.get("1.0", "end-1c")

    def _update_cipher_controls(self):
        """Show the controls that matter for the selected cipher."""
        is_spn = self.cipher_type.get() == CIPHER_SPN
        spn_state = "normal" if is_spn else "disabled"
        caesar_state = "disabled" if is_spn else "normal"

        self.key_entry.configure(state=spn_state)
        self.rounds_spinbox.configure(state=spn_state)
        self.base64_check.configure(state=spn_state)
        self.shift_spinbox.configure(state=caesar_state)

        if is_spn:
            self.status.set("SPN Cipher selected.")
        else:
            self.status.set("Caesar Cipher selected.")

    def _set_loading(self, message):
        """Display a short loading status and refresh the window."""
        self.status.set(message)
        self.update_idletasks()

    def _add_agent_message(self, body):
        """Append an agent message."""
        self._append_chat("AGENT", body, "agent")

    def _add_user_message(self, body):
        """Append a user message."""
        self._append_chat("YOU", body, "user")

    def _add_result_message(self, heading, body):
        """Append a cipher result message."""
        self._append_chat("RESULT", f"{heading}\n{body}", "result")

    def _add_error_message(self, body):
        """Append an error message."""
        self._append_chat("ALERT", body, "error")

    def _append_chat(self, sender, body, tag):
        """Append a timestamped message to the chat log."""
        timestamp = datetime.now().strftime("%I:%M %p")
        entry = f"[{timestamp}] {sender}\n{body}"
        self.chat_entries.append(entry)

        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"{entry}\n\n", tag)
        self.chat_log.see("end")
        self.chat_log.configure(state="disabled")


def run_cli():
    """Run the terminal interface without breaking GUI mode."""
    print("=== Secret Agent Cipher Chatbox CLI ===")
    print("1. SPN Cipher")
    print("2. Caesar Cipher")

    cipher_choice = input("Choose cipher (1/2): ").strip()
    action_choice = input("Choose Encrypt or Decrypt (e/d): ").strip().lower()
    message = input("Enter message: ")

    try:
        if cipher_choice == "2":
            shift = input("Enter Caesar shift (0-25): ")
            mode = "decrypt" if action_choice.startswith("d") else "encrypt"
            result = caesar_cipher(message, shift, mode=mode)
        else:
            key = input("Enter key: ")
            rounds = input("Rounds (1-5, default 1): ") or "1"
            use_base64 = input("Use Base64? (Y/n): ").strip().lower() != "n"

            if action_choice.startswith("d"):
                result = decrypt(message, key, rounds=rounds, use_base64=use_base64)
            else:
                result = encrypt(message, key, rounds=rounds, use_base64=use_base64)
    except ValueError as error:
        print(f"\nError: {error}")
        return

    print("\nResult:")
    print(result)


def main():
    """Parse command-line arguments and launch CLI or GUI mode."""
    parser = argparse.ArgumentParser(
        description="SPN Cipher secret-agent chatbox",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="run in terminal mode",
    )
    args = parser.parse_args()

    if args.cli:
        run_cli()
        return

    app = SecretAgentChatbox()
    app.mainloop()


if __name__ == "__main__":
    main()
