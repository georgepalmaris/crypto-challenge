# https://cryptopals.com/sets/1/challenges/4

# """Challenge 5: Implement repeating-key XOR
# This challenge involves implementing a repeating-key XOR cipher.
# The input is a plaintext string and a key, and the output is the ciphertext.
# The challenge is to correctly apply the XOR operation using the repeating key.
# The key is repeated to match the length of the plaintext.
# The output is then encoded in hexadecimal format.
# """

import os

from itertools import cycle, islice

from challenges.challenge_02 import bytes_xor


def run_challenge(input_data: str):
    """Challenge 5: Implement repeating-key XOR."""

    print("🔄 Implementing repeating-key XOR cipher...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_05.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (text):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_05.txt", "r") as f:
        result_hex = f.read().strip()

    print("🏁 Expected Result (hex):", result_hex)

    key = b"ICE"
    plaintext = input_data.encode("utf-8")

    ciphertext = repeating_key_xor(key, plaintext)
    ciphertext_hex = ciphertext.hex()

    print("🔐 Ciphertext (hex):", ciphertext_hex)

    if ciphertext_hex == result_hex:
        print("✅ Encoding successful!")
    else:
        print("❌ Encoding did not match expected result.")


def repeating_key_xor(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt plaintext using repeating-key XOR with the given key."""
    # Repeat the key to match the length of the plaintext
    repeated_key = bytes(islice(cycle(key), len(plaintext)))
    return bytes_xor(plaintext, repeated_key)
