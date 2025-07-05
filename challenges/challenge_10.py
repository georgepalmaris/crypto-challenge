# https://cryptopals.com/sets/2/challenges/10

# """Challenge 10: Implement CBC mode decryption
# This challenge involves implementing CBC (Cipher Block Chaining) mode decryption.
# The input is a base64-encoded ciphertext, and the output should be the decrypted plaintext.
# The challenge is to correctly implement the CBC mode decryption algorithm.
# """

import os

from base64 import b64decode
from challenges.challenge_02 import bytes_xor
from challenges.challenge_07 import aes_ecb_decrypt
from challenges.challenge_08 import bytes_to_chunks
from challenges.challenge_09 import pkcs7_unpad
from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size  # AES block size is 16 bytes


def run_challenge(input_data: str):
    """Challenge 10: Implement CBC mode decryption."""
    print("🔍 Implementing CBC mode decryption...")

    with open(f"{os.getcwd()}/challenges/inputs/challenge_10.txt", "r") as f:
        input_data = f.read().strip()

    print("📥 Input (ciphertext):", input_data)

    if not input_data:
        print("❌ No input data provided!")
        return

    with open(f"{os.getcwd()}/challenges/results/challenge_10.txt", "r") as f:
        expected_result = f.read().strip()

    print("🏁 Expected Result (plaintext):", expected_result)

    # Decode the base64 input data
    try:
        ciphertext = b64decode(input_data)
    except ValueError as e:
        print(f"❌ Error decoding input data: {e}")
        return

    print("🔓 Decrypting ciphertext...")

    # Use a fixed key and IV for this challenge
    key: bytes = b"YELLOW SUBMARINE"  # Fixed 16-byte key for
    iv: bytes = bytes(BLOCK_SIZE)  # Fixed IV of BLOCK_SIZE null bytes

    try:
        plaintext = aes_cbc_decrypt(ciphertext, key, iv)
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return

    print("🔓 Decrypted Ciphertext (text):", plaintext.decode("utf-8", errors="ignore"))

    if plaintext.decode("utf-8", errors="ignore").strip() == expected_result:
        print("✅ Decryption successful!")
    else:
        print("❌ Decryption did not match expected result.")


def aes_cbc_decrypt(
    ciphertext: bytes, key: bytes, iv: bytes, use_pkcs7: bool = True
) -> bytes:
    """Decrypts ciphertext using AES in CBC mode."""
    blocks: list[bytes] = bytes_to_chunks(ciphertext, BLOCK_SIZE)
    previous_ciphertext: bytes = iv
    plaintext: bytes = b""

    for block in blocks:
        raw_decrypted_block: bytes = aes_ecb_decrypt(block, key)
        plaintext += bytes_xor(raw_decrypted_block, previous_ciphertext)
        previous_ciphertext = block

    if use_pkcs7:
        plaintext = pkcs7_unpad(plaintext)
    return plaintext
