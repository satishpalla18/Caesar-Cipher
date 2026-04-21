#  SPN Cipher - Secret Agent Chatbox

A modern **Python encryption tool** with a dark-themed **chat-style GUI**, powered by a custom **SPN (Shift–Permutation–Noise) Cipher**.
Supports both **GUI (Tkinter)** and **CLI (Terminal)** modes for flexible usage.


##  Features

*  Custom SPN encryption algorithm
*  Encrypt and decrypt messages
*  Stylish **Secret-Agent Chatbox UI**
*  Key-based encryption system
*  Multiple encryption rounds
*  Base64 encoding for safe output
*  Wrong key detection (`Key not match`)
*  CLI mode support
*  Beginner-friendly and well-structured code


##  How the Algorithm Works

The **SPN Cipher** follows 3 main stages:

### 1.  Dynamic Key-Based Shift

* Each key character → numeric shift using ASCII % 26
* Applies shifting on:

  * `a-z` (lowercase letters)
  * `A-Z` (uppercase letters)
  * `0-9` (digits)
* Special characters remain unchanged


### 2. Block Permutation

* Splits message into blocks (based on key length)
* Reverses each block


### 3. Noise Injection

* Adds a random lowercase character after every 3 characters
* Uses Python’s built-in `random` module


###  Decryption Process

Reverse of encryption:

1. Remove noise
2. Reverse block permutation
3. Reverse key-based shift
4. Validate key


## Project Structure

```
ENCRYPTIPON TOOL/
│
├── ENCRYPTIPON TOOL.py   # GUI + CLI main application
├── cipher.py             # SPN encryption/decryption logic
├── README.md             # Project documentation
```


##  Requirements

* Python 3.x
* Tkinter (usually pre-installed)


##  Run the Application

###  GUI Mode

```bash
python "ENCRYPTIPON TOOL.py"
```


### CLI Mode

```bash
python "ENCRYPTIPON TOOL.py" --cli
```

Then follow prompts:

```
Choose Encrypt or Decrypt (e/d):
Enter message:
Enter key:
Rounds (default 1):
```


##  Example

**Input:**

```
Message: Hello123
Key: mysecret
Rounds: 2
```

**Output:**

```
Encrypted transmission:
<Base64 encoded encrypted text>
```


##  Wrong Key Behavior

If incorrect key is used during decryption:

```
Key not match.
```


##  Future Improvements

* Add multiple cipher options (Caesar, AES, etc.)
* Copy-to-clipboard feature
* Light/Dark theme toggle
* Export chat history
* Brute-force decryption mode


##  Notes

* This project is built for **learning and demonstration purposes**
* Not intended for real-world secure communication


##  Author

**Satish**
Student | Python Developer | Encryption Enthusiast



