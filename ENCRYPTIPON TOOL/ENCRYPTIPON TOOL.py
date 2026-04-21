import tkinter as tk
from tkinter import ttk

from cipher import caesar_cipher, generate_all_shifts, normalize_shift


class CaesarCipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caesar Cipher")
        self.geometry("760x620")
        self.minsize(640, 520)

        self.mode = tk.StringVar(value="encrypt")
        self.shift = tk.StringVar(value="3")
        self.status = tk.StringVar(value="Ready")

        self._configure_style()
        self._build_ui()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f7f8fb")
        style.configure("Header.TLabel", background="#f7f8fb", font=("Helvetica", 22, "bold"))
        style.configure("Subheader.TLabel", background="#f7f8fb", foreground="#5f6673")
        style.configure("TLabel", background="#f7f8fb", font=("Helvetica", 11))
        style.configure("TRadiobutton", background="#f7f8fb", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11), padding=(12, 7))
        style.configure("Primary.TButton", font=("Helvetica", 11, "bold"), padding=(14, 8))
        style.configure("Status.TLabel", background="#edf1f7", foreground="#4d5563", padding=(10, 6))

    def _build_ui(self):
        root = ttk.Frame(self, padding=24)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(4, weight=1)

        ttk.Label(root, text="Caesar Cipher", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            root,
            text="Encrypt, decrypt, or inspect every possible shift.",
            style="Subheader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 18))

        input_frame = ttk.Frame(root)
        input_frame.grid(row=2, column=0, sticky="nsew")
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        ttk.Label(input_frame, text="Message").grid(row=0, column=0, sticky="w")
        self.input_text = tk.Text(input_frame, height=8, wrap="word", undo=True)
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(6, 16))

        controls = ttk.Frame(root)
        controls.grid(row=3, column=0, sticky="ew", pady=(0, 16))
        controls.columnconfigure(3, weight=1)

        ttk.Label(controls, text="Mode").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Radiobutton(controls, text="Encrypt", variable=self.mode, value="encrypt").grid(
            row=0, column=1, sticky="w", padx=(0, 10)
        )
        ttk.Radiobutton(controls, text="Decrypt", variable=self.mode, value="decrypt").grid(
            row=0, column=2, sticky="w", padx=(0, 24)
        )

        ttk.Label(controls, text="Shift").grid(row=0, column=3, sticky="e", padx=(0, 8))
        shift_spinbox = ttk.Spinbox(
            controls,
            from_=0,
            to=25,
            width=5,
            textvariable=self.shift,
            wrap=True,
            justify="center",
        )
        shift_spinbox.grid(row=0, column=4, sticky="e", padx=(0, 16))

        ttk.Button(controls, text="Run", style="Primary.TButton", command=self.run_cipher).grid(
            row=0, column=5, padx=(0, 8)
        )
        ttk.Button(controls, text="All Shifts", command=self.show_all_shifts).grid(
            row=0, column=6, padx=(0, 8)
        )
        ttk.Button(controls, text="Clear", command=self.clear).grid(row=0, column=7)

        output_frame = ttk.Frame(root)
        output_frame.grid(row=4, column=0, sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)

        ttk.Label(output_frame, text="Output").grid(row=0, column=0, sticky="w")
        self.output_text = tk.Text(output_frame, height=10, wrap="word", state="disabled")
        self.output_text.grid(row=1, column=0, sticky="nsew", pady=(6, 16))

        ttk.Label(root, textvariable=self.status, style="Status.TLabel").grid(
            row=5, column=0, sticky="ew"
        )

    def run_cipher(self):
        message = self._get_message()
        shift = normalize_shift(self.shift.get())
        mode = self.mode.get()

        self._set_output(caesar_cipher(message, shift, mode=mode))
        self.status.set(f"{mode.title()}ed with shift {shift}.")

    def show_all_shifts(self):
        message = self._get_message()
        shifts = generate_all_shifts(message)

        if not shifts:
            self._set_output("")
            self.status.set("Enter a message to generate all shifts.")
            return

        output = "\n\n".join(f"Shift {item['shift']:02d}: {item['text']}" for item in shifts)
        self._set_output(output)
        self.status.set("Showing all possible decryptions.")

    def clear(self):
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self.status.set("Cleared.")

    def _get_message(self):
        return self.input_text.get("1.0", "end-1c")

    def _set_output(self, value):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", value)
        self.output_text.configure(state="disabled")


if __name__ == "__main__":
    app = CaesarCipherApp()
    app.mainloop()