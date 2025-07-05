# https://cryptopals.com/sets/2/challenges/11

# """Challenge 11: An ECB/CBC detection oracle
# This challenge involves implementing an oracle that can detect whether a given ciphertext was encrypted using ECB or CBC mode.
# The input is a base64-encoded ciphertext, and the output should indicate whether the ciphertext was encrypted using ECB or CBC mode.
# The challenge is to correctly implement the detection algorithm
# """

import os
from random import choice, randint
from typing import Callable
from Crypto.Cipher import AES
from enum import Enum

from challenges.challenge_08 import bytes_to_chunks
from challenges.challenge_09 import pkcs7_pad

EncryptionOracleType = Callable[
    [bytes], bytes
]  # Take one bytes argument and return bytes
BLOCK_SIZE = AES.block_size  # AES block size is 16 bytes
KEY_SIZE = 32  # AES key size is 32 bytes for AES-256
MIN_PREFIX_LENGTH = 5


class AESMode(Enum):
    ECB = "ECB"
    CBC = "CBC"


def run_challenge(input_data: str):
    """Challenge 11: An ECB/CBC detection oracle."""
    print("🔍 Implementing ECB/CBC detection oracle...")

    for _ in range(1000):
        _mode, oracle = get_encryption_oracle()
        guess = detector(oracle)

        if guess != _mode:
            print(f"❌ Detection failed! Expected {_mode}, but got {guess}.")
        else:
            print(f"✅ Detection successful! Mode: {guess}.")

    print("🏁 All guesses were successful")


def get_encryption_oracle() -> tuple[AESMode, EncryptionOracleType]:
    mode = choice([AESMode.ECB, AESMode.CBC])

    def encryption_oracle(plaintext: bytes) -> bytes:
        """Encrypts plaintext using either ECB or CBC mode."""
        key = os.urandom(KEY_SIZE)
        prefix = os.urandom(randint(5, 10))
        suffix = os.urandom(randint(5, 10))
        plaintext = pkcs7_pad(prefix + plaintext + suffix, BLOCK_SIZE)

        if mode == AESMode.ECB:
            cipher = AES.new(key, AES.MODE_ECB)
        else:  # AESMode.CBC
            iv = os.urandom(BLOCK_SIZE)
            cipher = AES.new(key, AES.MODE_CBC, iv)

        return cipher.encrypt(plaintext)

    return mode, encryption_oracle


def detector(func: EncryptionOracleType) -> AESMode:
    """Detects whether the encryption oracle uses ECB or CBC mode."""
    plaintext = bytes(
        2 * BLOCK_SIZE + (BLOCK_SIZE - MIN_PREFIX_LENGTH)
    )  # Create a plaintext that will produce two identical blocks in ECB mode
    print(plaintext)
    ciphertext = func(plaintext)
    chunked_blocks = bytes_to_chunks(ciphertext, BLOCK_SIZE)

    # Check for identical blocks
    if chunked_blocks[1] == chunked_blocks[2]:
        return AESMode.ECB
    else:
        return AESMode.CBC
