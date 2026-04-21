"""Caesar cipher helpers used by the Tkinter app."""


ALPHABET_SIZE = 26


def normalize_shift(value):
    """Return a shift value in the range 0-25."""
    try:
        return int(value) % ALPHABET_SIZE
    except (TypeError, ValueError):
        return 0


def caesar_cipher(message, shift, mode="encrypt"):
    """Encrypt or decrypt a message with a Caesar cipher."""
    shift = normalize_shift(shift)
    if mode == "decrypt":
        shift = -shift

    result = []
    for character in message:
        if character.isalpha():
            base = ord("A") if character.isupper() else ord("a")
            offset = (ord(character) - base + shift) % ALPHABET_SIZE
            result.append(chr(base + offset))
        else:
            result.append(character)

    return "".join(result)


def generate_all_shifts(message):
    """Return every possible Caesar decryption for a non-empty message."""
    if not message:
        return []

    return [
        {"shift": shift, "text": caesar_cipher(message, shift, mode="decrypt")}
        for shift in range(ALPHABET_SIZE)
    ]
