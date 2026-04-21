"""Cipher helpers for the Secret Agent Chatbox project.

The module exposes two cipher families:

- SPN Cipher (Shift-Permutation-Noise), the custom educational cipher.
- Caesar Cipher, a classic shift cipher with brute-force support.

The functions raise ValueError for invalid input so both the GUI and CLI can
show friendly error messages instead of crashing.
"""

import base64
import binascii
import random
import string


NOISE_INTERVAL = 3
MESSAGE_MARKER = "SPN_OK::"
KEY_MISMATCH_ERROR = "Key not match."
MIN_ROUNDS = 1
MAX_ROUNDS = 5
ALPHABET_SIZE = 26
DIGIT_SIZE = 10


def validate_rounds(rounds):
    """Return a valid round count between 1 and 5."""
    try:
        round_count = int(rounds)
    except (TypeError, ValueError) as error:
        raise ValueError("Rounds must be a number from 1 to 5.") from error

    if not MIN_ROUNDS <= round_count <= MAX_ROUNDS:
        raise ValueError("Rounds must be between 1 and 5.")

    return round_count


def validate_message_and_key(message, key, rounds):
    """Validate shared SPN inputs."""
    if message == "":
        raise ValueError("Message cannot be empty.")
    if key == "":
        raise ValueError("Key cannot be empty.")

    return validate_rounds(rounds)


def normalize_shift(value):
    """Return a Caesar shift value in the range 0-25."""
    try:
        return int(value) % ALPHABET_SIZE
    except (TypeError, ValueError) as error:
        raise ValueError("Shift must be a number from 0 to 25.") from error


def _key_shifts(key):
    """Convert each key character into a numeric shift using ASCII mod 26."""
    return [ord(character) % ALPHABET_SIZE for character in key]


def _shift_letter(character, shift):
    """Shift uppercase and lowercase letters inside their own alphabets."""
    base = ord("a") if character.islower() else ord("A")
    offset = (ord(character) - base + shift) % ALPHABET_SIZE
    return chr(base + offset)


def _shift_digit(character, shift):
    """Shift digits inside 0-9."""
    return str((int(character) + shift) % DIGIT_SIZE)


def _dynamic_shift(text, key, decrypt=False):
    """Stage 1: apply or reverse cyclic key-based shifting."""
    shifted_text = []
    shifts = _key_shifts(key)

    for index, character in enumerate(text):
        shift = shifts[index % len(shifts)]
        if decrypt:
            shift = -shift

        if character.isalpha():
            shifted_text.append(_shift_letter(character, shift))
        elif character.isdigit():
            shifted_text.append(_shift_digit(character, shift))
        else:
            shifted_text.append(character)

    return "".join(shifted_text)


def _permute_blocks(text, key):
    """Stage 2: split into key-sized chunks and reverse each chunk."""
    block_size = len(key)
    chunks = []

    for start in range(0, len(text), block_size):
        chunk = text[start : start + block_size]
        chunks.append(chunk[::-1])

    return "".join(chunks)


def _inject_noise(text):
    """Stage 3: add one random lowercase character after every 3 characters."""
    noisy_text = []

    for index, character in enumerate(text, start=1):
        noisy_text.append(character)
        if index % NOISE_INTERVAL == 0:
            noisy_text.append(random.choice(string.ascii_lowercase))

    return "".join(noisy_text)


def _remove_noise(text):
    """Reverse Stage 3 by removing each injected fourth character."""
    cleaned_text = []

    for index, character in enumerate(text, start=1):
        if index % (NOISE_INTERVAL + 1) != 0:
            cleaned_text.append(character)

    return "".join(cleaned_text)


def _encode_base64(text):
    """Encode encrypted text so it is easy to copy and paste."""
    raw_bytes = text.encode("utf-8")
    return base64.urlsafe_b64encode(raw_bytes).decode("ascii")


def _decode_base64(text):
    """Decode Base64 text before decrypting."""
    try:
        raw_bytes = base64.urlsafe_b64decode(text.encode("ascii"))
        return raw_bytes.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, UnicodeEncodeError) as error:
        raise ValueError("Encrypted message is not valid Base64.") from error


def encrypt(message, key, rounds=1, use_base64=True):
    """Encrypt a message with the SPN Cipher."""
    round_count = validate_message_and_key(message, key, rounds)
    encrypted_text = MESSAGE_MARKER + message

    for _ in range(round_count):
        encrypted_text = _dynamic_shift(encrypted_text, key)
        encrypted_text = _permute_blocks(encrypted_text, key)
        encrypted_text = _inject_noise(encrypted_text)

    if use_base64:
        encrypted_text = _encode_base64(encrypted_text)

    return encrypted_text


def decrypt(message, key, rounds=1, use_base64=True):
    """Decrypt a message created by encrypt()."""
    round_count = validate_message_and_key(message, key, rounds)
    decrypted_text = _decode_base64(message) if use_base64 else message

    for _ in range(round_count):
        decrypted_text = _remove_noise(decrypted_text)
        decrypted_text = _permute_blocks(decrypted_text, key)
        decrypted_text = _dynamic_shift(decrypted_text, key, decrypt=True)

    if not decrypted_text.startswith(MESSAGE_MARKER):
        raise ValueError(KEY_MISMATCH_ERROR)

    return decrypted_text[len(MESSAGE_MARKER) :]


def caesar_cipher(message, shift, mode="encrypt"):
    """Encrypt or decrypt a message with a Caesar shift."""
    if message == "":
        raise ValueError("Message cannot be empty.")

    normalized_shift = normalize_shift(shift)
    if mode == "decrypt":
        normalized_shift = -normalized_shift

    transformed_text = []
    for character in message:
        if character.isalpha():
            transformed_text.append(_shift_letter(character, normalized_shift))
        elif character.isdigit():
            transformed_text.append(_shift_digit(character, normalized_shift))
        else:
            transformed_text.append(character)

    return "".join(transformed_text)


def brute_force_caesar(message):
    """Return all possible Caesar decryptions for shifts 0-25."""
    if message == "":
        raise ValueError("Message cannot be empty.")

    results = []
    for shift in range(ALPHABET_SIZE):
        results.append(
            {
                "shift": shift,
                "text": caesar_cipher(message, shift, mode="decrypt"),
            }
        )

    return results
