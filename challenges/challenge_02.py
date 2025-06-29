# https://cryptopals.com/sets/1/challenges/2

# """Challenge 2: Fixed XOR
# This challenge performs a fixed XOR operation between two equal-length buffers.
# The first buffer is a fixed byte string, and the second is provided as input.
# The result is printed in both hexadecimal and ASCII formats.
# """

import os


def run_challenge(input_data: str):
    """Challenge 2: Fixed XOR."""
    print("⊕ XORing two equal-length buffers...")

    if not input_data:
        with open(f"{os.getcwd()}/challenges/inputs/challenge_02.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (hex):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_02.txt", "r") as f:
        result_hex = f.read().strip()

    print("🏁 Expected Result (hex):", result_hex)

    if input_data:
        try:
            input_bytes = bytes.fromhex(input_data)
            fixed_xor_compare_bytes = bytes.fromhex(
                "686974207468652062756c6c277320657965"
            )

            if len(input_bytes) != len(fixed_xor_compare_bytes):
                raise ValueError(
                    "Input data must be of equal length to the fixed XOR bytes."
                )

            # Zip function pairs bytes from both inputs into a list of tuples
            xor_result = bytes_xor(input_bytes, fixed_xor_compare_bytes)

            print(f"Result (XOR): {xor_result.hex()}")
            print(f"Result (ASCII): {xor_result.decode('utf-8', errors='ignore')}")

            if xor_result.hex() == result_hex:
                print("✅ XOR operation successful!")
            else:
                print("❌ XOR operation did not match expected result.")
        except Exception as e:
            print(f"❌ Error processing input: {e}")
    else:
        print("❌ No input data provided.")


def bytes_xor(a: bytes, b: bytes) -> bytes:
    """Perform XOR operation on two byte sequences."""
    if len(a) != len(b):
        raise ValueError("Byte sequences must be of equal length.")

    return bytes(x ^ y for x, y in zip(a, b))
