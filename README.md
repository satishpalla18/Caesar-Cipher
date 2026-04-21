# SPN Cipher - Secret Agent Chatbox

A dark themed Python encryption app that uses a custom **SPN Cipher (Shift-Permutation-Noise)** algorithm. The project includes both a Tkinter GUI and a simple command-line mode.

## Features

- Custom SPN encryption algorithm
- Encrypt and decrypt messages
- Dark secret-agent chatbox GUI
- Key-based encryption
- Multiple encryption rounds
- Base64 output always enabled for easy copying
- Wrong key detection with `Key not match.`
- CLI mode for terminal users
- Beginner-friendly code structure

## How The Algorithm Works

The SPN Cipher has three main stages:

1. **Dynamic Key-Based Shift**
   - Converts each key character into a numeric shift using ASCII value mod 26.
   - Shifts lowercase letters inside `a-z`.
   - Shifts uppercase letters inside `A-Z`.
   - Shifts digits inside `0-9`.
   - Keeps special characters unchanged.

2. **Block Permutation**
   - Splits the text into blocks based on the key length.
   - Reverses each block.

3. **Noise Injection**
   - Adds a random lowercase character after every 3 characters.
   - Uses Python's built-in `random` module.

During decryption, the app reverses these steps:

- Removes noise
- Reverses block permutation
- Reverses key-based shifting
- Checks whether the key matched

## Project Files

```text
ENCRYPTIPON TOOL.py   # Main GUI and CLI program
cipher.py             # SPN Cipher encryption/decryption logic
.vscode/settings.json # VS Code Python runner settings
README.md             # Project documentation
```

## Requirements

- Python 3
- Tkinter

Tkinter usually comes pre-installed with Python on macOS and many other systems.

## Run The GUI

Open the project folder in VS Code, then run:

```bash
python3 "ENCRYPTIPON TOOL.py"
```

Or press the VS Code run button if your Python interpreter is configured.

## Run In CLI Mode

```bash
python3 "ENCRYPTIPON TOOL.py" --cli
```

Then follow the prompts:

```text
Choose Encrypt or Decrypt (e/d):
Enter message:
Enter key:
Rounds (default 1):
```

## Example

Input:

```text
Message: Hello123
Key: mysecret
Rounds: 2
```

Output:

```text
Encrypted transmission:
<Base64 encrypted text>
```

To decrypt, paste the encrypted output, use the same key, and select the same number of rounds.

## Wrong Key Behavior

If the wrong key is used during decryption, the app displays:

```text
Key not match.
```

## GitHub Upload Note

Do not upload generated or system files such as:

```text
__pycache__/
.DS_Store
```

Only upload the source files and documentation.

## Important Note

This project is made for learning and demonstration. It is a custom educational cipher, not a replacement for professional cryptography libraries used in real security systems.
