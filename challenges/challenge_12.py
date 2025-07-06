# https://cryptopals.com/sets/2/challenges/12

# """Challenge 12: Byte-at-a-time ECB decryption (Simple)
# This challenge involves implementing a byte-at-a-time ECB decryption algorithm.
# The input is a base64-encoded ciphertext, and the output should be the decrypted plaintext.
# The challenge is to correctly implement the decryption algorithm and handle padding.
# The output should be the decrypted plaintext in hex format.
# """

from time import sleep
import os

from base64 import b64decode
from typing import Callable
from Crypto.Cipher import AES
from itertools import count

from challenges.challenge_08 import bytes_to_chunks
from challenges.challenge_09 import pkcs7_pad

EncryptionOracleType = Callable[
    [bytes], bytes
]  # Take one bytes argument and return bytes
BLOCK_SIZE = AES.block_size  # AES block size is 16 bytes
KEY_SIZE = 32  # AES key size is 32 bytes for AES-256


def run_challenge(input_data: str):
    """Challenge 12: Byte-at-a-time ECB decryption (Simple)"""
    print("🔍 Implementing byte-at-a-time ECB decryption...")

    oracle = make_encryption_oracle()

    print("Step 1: Determine block size and postfix length")

    block_size, postfix_length = find_block_size_and_postfix_length(oracle)
    print(f"Block size: {block_size} bytes")
    print(f"Postfix length: {postfix_length} bytes")
    assert block_size == BLOCK_SIZE, "Block size does not match AES block size"
    assert postfix_length > 0, "Postfix length must be positive"

    print("✅ Step 1 completed successfully.")

    print("Step 2: Detect if the oracle is using ECB mode")
    assert detect_ecb_mode(oracle), "Oracle is not using ECB mode"

    print("✅ Step 2 completed successfully.")

    print("Step 3: Create a transposed/flattened list of ciphertexts")

    ciphertexts = [
        bytes_to_chunks(oracle(bytes(15 - i)), BLOCK_SIZE) for i in range(BLOCK_SIZE)
    ]
    transposed_ciphertext = [block for blocks in zip(*ciphertexts) for block in blocks]
    blocks_to_attack = transposed_ciphertext[:postfix_length]

    print("✅ Step 3 completed successfully.")

    print("Step 4: Guess each byte of the secret postfix")
    postfix = bytes(15)
    for block in blocks_to_attack:
        postfix += guess_byte(postfix[-15:], block, oracle)
        print(postfix[15:])
        # sleep(0.1)  # Sleep for fun
    postfix = postfix[15:]

    print("✅ Step 4 completed successfully.")
    print("Decrypted Postfix:", postfix.decode("utf-8", errors="ignore"))

    with open(f"{os.getcwd()}/challenges/results/challenge_12.txt", "r") as f:
        expected_result = f.read().strip()

    if postfix.decode("utf-8", errors="ignore").strip() == expected_result:
        print("✅ Decryption successful!")
    else:
        print("❌ Decryption did not match expected result.")


def make_encryption_oracle() -> EncryptionOracleType:
    """Create an encryption oracle that encrypts plaintext using AES in ECB mode."""
    _key = os.urandom(KEY_SIZE)

    with open(f"{os.getcwd()}/challenges/inputs/challenge_12.txt", "rb") as f:
        _secret_postfix = b64decode(f.read())

    def encryption_oracle(plaintext: bytes) -> bytes:
        """Encrypts plaintext using AES in ECB mode."""
        cipher = AES.new(_key, AES.MODE_ECB)
        padded_plaintext = pkcs7_pad(plaintext + _secret_postfix, BLOCK_SIZE)
        return cipher.encrypt(padded_plaintext)

    return encryption_oracle


def find_block_size_and_postfix_length(oracle: EncryptionOracleType) -> tuple[int, int]:
    """Find the block size and length of the secret postfix."""
    block_size = None
    postfix_length = None

    l = len(oracle(b"A"))
    for i in count(2):
        l2 = len(oracle(b"A" * i))
        if l2 > l:
            block_size = l2 - l
            postfix_length = l - i
            break

    assert block_size is not None, "Block size not found"
    assert postfix_length is not None, "Postfix length not found"
    return block_size, postfix_length


def detect_ecb_mode(oracle: EncryptionOracleType) -> bool:
    """Detect if the oracle is using ECB mode."""
    ciphertext = oracle(b"A" * (2 * BLOCK_SIZE))
    chunks = bytes_to_chunks(ciphertext, BLOCK_SIZE)
    if chunks[0] == chunks[1]:
        return True
    return False


def guess_byte(prefix: bytes, target: bytes, oracle: EncryptionOracleType) -> bytes:
    """Guess a single byte of the secret postfix."""
    for b in range(256):
        guess = prefix + bytes([b])
        if oracle(guess)[:BLOCK_SIZE] == target:
            return bytes([b])
    raise ValueError("No matching byte found")
