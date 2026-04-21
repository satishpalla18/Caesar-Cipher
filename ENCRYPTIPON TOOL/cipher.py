"""SPN Cipher (Shift-Permutation-Noise).

This module contains the full encryption and decryption logic for the project.
The algorithm is educational, custom, and reversible when the same key and
round count are used.
"""

import base64
import random
import string


NOISE_INTERVAL = 3
MESSAGE_MARKER = "SPN_OK::"
KEY_MISMATCH_ERROR = "Key not match."


def _validate_inputs(message, key, rounds):
    """Check common input rules before encrypting or decrypting."""
    if message == "":
        raise ValueError("Message cannot be empty.")
    if key == "":
        raise ValueError("Key cannot be empty.")
    if rounds < 1:
        raise ValueError("Rounds must be at least 1.")


def _key_shifts(key):
    """Convert each key character into a numeric shift using ASCII mod 26."""
    return [ord(character) % 26 for character in key]


def _shift_letter(character, shift):
    """Shift uppercase and lowercase letters inside their own alphabets."""
    if character.islower():
        base = ord("a")
    else:
        base = ord("A")

    return chr(base + ((ord(character) - base + shift) % 26))


def _shift_digit(character, shift):
    """Shift digits inside 0-9."""
    return str((int(character) + shift) % 10)


def _dynamic_shift(text, key, decrypt=False):
    """Stage 1: apply or reverse cyclic key-based shifting."""
    shifts = _key_shifts(key)
    shifted_text = []

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
    """Encode final encrypted text so it is easy to copy and paste."""
    raw_bytes = text.encode("utf-8")
    return base64.urlsafe_b64encode(raw_bytes).decode("ascii")


def _decode_base64(text):
    """Decode Base64 text before decrypting."""
    try:
        raw_bytes = base64.urlsafe_b64decode(text.encode("ascii"))
        return raw_bytes.decode("utf-8")
    except Exception as error:
        raise ValueError("Encrypted message is not valid Base64.") from error


def encrypt(message, key, rounds=1, use_base64=True):
    """Encrypt a message with the SPN Cipher."""
    _validate_inputs(message, key, rounds)
    encrypted_text = MESSAGE_MARKER + message

    for _round in range(rounds):
        encrypted_text = _dynamic_shift(encrypted_text, key)
        encrypted_text = _permute_blocks(encrypted_text, key)
        encrypted_text = _inject_noise(encrypted_text)

    if use_base64:
        encrypted_text = _encode_base64(encrypted_text)

    return encrypted_text


def decrypt(message, key, rounds=1, use_base64=True):
    """Decrypt a message created by encrypt()."""
    _validate_inputs(message, key, rounds)
    decrypted_text = _decode_base64(message) if use_base64 else message

    for _round in range(rounds):
        decrypted_text = _remove_noise(decrypted_text)
        decrypted_text = _permute_blocks(decrypted_text, key)
        decrypted_text = _dynamic_shift(decrypted_text, key, decrypt=True)

    if not decrypted_text.startswith(MESSAGE_MARKER):
        raise ValueError(KEY_MISMATCH_ERROR)

    return decrypted_text[len(MESSAGE_MARKER) :]
