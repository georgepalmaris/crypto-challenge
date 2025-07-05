# https://cryptopals.com/sets/2/challenges/9

# """Challenge 9: Implement PKCS#7 padding
# This challenge involves implementing PKCS#7 padding for a given plaintext.
# The input is a plaintext string, and the output is the padded string.
# The challenge is to correctly apply the padding rules according to the PKCS#7 standard.
# The padding should be added to make the plaintext a multiple of the block size (16 bytes).
# """

import os

BLOCK_SIZE = 16


def run_challenge(input_data: str):
    """Challenge 9: Implement PKCS#7 padding."""
    print("🔍 Implementing PKCS#7 padding...")

    with open(f"{os.getcwd()}/challenges/inputs/challenge_09.txt", "r") as f:
        input_data = f.read().strip()

    print("📥 Input (plaintext):", input_data)

    if not input_data:
        print("❌ No input data provided!")
        return

    with open(f"{os.getcwd()}/challenges/results/challenge_09.txt", "r") as f:
        expected_result = f.read().strip()

    print("🏁 Expected Result (plaintext):", expected_result)

    # Convert input data to bytes
    input_bytes = input_data.encode("utf-8", errors="ignore")

    print("📥 Input (bytes):", input_bytes)

    input_with_padding = pkcs7_pad(input_bytes, BLOCK_SIZE)

    print("🔒 Padded Input (bytes):", input_with_padding)

    # Remove padding to verify correctness
    try:
        padded_text = pkcs7_unpad(input_with_padding).decode("utf-8", errors="ignore")
    except ValueError as e:
        print(f"❌ Error during unpadding: {e}")
        return

    print("🔒 Unpadded Input (text):", padded_text)

    if padded_text == expected_result:
        print("✅ Padding opertions successful!")
    else:
        print("❌ Padding did not match expected result.")


class PaddingError(Exception):
    """Custom exception for padding errors."""

    pass


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    """Apply PKCS#7 padding to the input data."""
    if block_size == 16:
        padding_length = block_size - (len(data) & 15)
    else:
        padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding


def pkcs7_unpad(data: bytes) -> bytes:
    """Remove PKCS#7 padding from the input data."""

    padding_length = data[-1]
    if (
        padding_length == 0
        or len(data) < padding_length
        or data.endswith(bytes([padding_length]) * padding_length) is False
    ):
        raise PaddingError
    return data[:-padding_length]
