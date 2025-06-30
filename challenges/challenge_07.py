# https://cryptopals.com/sets/1/challenges/7

# """Challenge 7: AES in ECB mode
# This challenge involves implementing AES encryption in ECB mode.
# The input is a plaintext string, and the key is a fixed 16-byte key.
# The challenge is to correctly implement the AES algorithm and handle padding.
# The output should be the decrypted ciphertext in hex format - this is to avoid issues with byte padding in ECB mode.
# """

import os

from base64 import b64decode
from Crypto.Cipher import AES

AES_KEY = b"YELLOW SUBMARINE"  # Fixed 16-byte key for AES in ECB mode


def run_challenge(input_data: str):
    """Challenge 7: AES in ECB mode."""
    print("🔐 Implementing AES encryption in ECB mode...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_07.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (base64):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_07.txt", "r") as f:
        result_plaintext = f.read().strip()

    print("🏁 Expected Result (hex):", result_plaintext)

    # Decode the base64 input data
    try:
        ciphertext = b64decode(input_data)
    except Exception as e:
        print(f"❌ Error decoding input data: {e}")
        return

    print("🔓 Decrypting ciphertext...")

    try:
        plaintext = aes_ecb_decrypt(ciphertext, AES_KEY).hex()
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return

    print("🔓 Decrypted Ciphertext (hex):", plaintext)

    if plaintext == result_plaintext:
        print("✅ Decryption successful!")
    else:
        print("❌ Decryption did not match expected result.")


def aes_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt ciphertext using AES in ECB mode with the given key."""
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)
