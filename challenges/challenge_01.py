# https://cryptopals.com/sets/1/challenges/1

# """Challenge 1: Hex to Base64
# This challenge converts a hexadecimal string to Base64 encoding.
# The input is a hexadecimal string, and the output is printed in Base64 format.
# The expected result is also provided for verification.
# """

import os

from base64 import b16decode, b64encode


def run_challenge(input_data: str):
    """Challenge 1: Hex to Base64."""
    print("🔄 Base16 Decode the hexadecimal string")

    if not input_data:
        with open(f"{os.getcwd()}/challenges/inputs/challenge_01.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (hex):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_01.txt", "r") as f:
        result_b64 = f.read().strip()

    print("🏁 Expected Result (Base64):", result_b64)

    if input_data:
        try:
            decoded = b16decode(input_data, casefold=True)
            print(f"Decoded: {decoded}")

            encoded = b64encode(decoded)
            print(f"Encoded (Base64): {encoded}")

            if encoded.decode() == result_b64:
                print("✅ Encoding successful!")
            else:
                print("❌ Encoding did not match expected result.")
        except Exception as e:
            print(f"❌ Error processing input: {e}")
    else:
        print("❌ No input data provided.")
