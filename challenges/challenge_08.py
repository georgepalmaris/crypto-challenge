# https://cryptopals.com/sets/1/challenges/8

# """Challenge 8: Detect AES in ECB mode
# This challenge involves detecting whether a given ciphertext is encrypted using AES in ECB mode.
# The input is a list of hexadecimal strings, and the output is the index of the string
# that is likely encrypted in ECB mode.
# The challenge is to identify the string with repeated blocks, which is a characteristic of ECB mode
# """

import os

BLOCK_SIZE = 16


def run_challenge(input_data: str):
    """Challenge 8: Detect AES in ECB mode."""
    print("🔍 Detecting AES in ECB mode...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_08.txt", "r") as f:
            input_data = f.read().splitlines()

    print("📥 Input (hex strings):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_08.txt", "r") as f:
        expected_result = f.read().strip()

    print("🏁 Expected Result (hex):", expected_result)

    ciphertexts = [bytes.fromhex(line.strip()) for line in input_data]

    for index, ciphertext in enumerate(ciphertexts):
        num_blocks = len(ciphertext) // BLOCK_SIZE
        num_unique_blocks = len(
            set(bytes_to_chunks(ciphertext, BLOCK_SIZE))
        )  # Set will only retrieve unique results
        num_repeated_blocks = num_blocks - num_unique_blocks

        # If there are no repeated blocks, it is likely not ECB mode
        if num_repeated_blocks == 0:
            continue

        # If we reach this point, we have found a candidate for ECB mode
        print()
        print("🔑 Found potential ECB mode ciphertext at index:", index)
        print("   Number of blocks:", num_blocks)
        print("   Number of unique blocks:", num_unique_blocks)
        print("   Number of repeated blocks:", num_repeated_blocks)

        if ciphertext.hex() == expected_result:
            print("✅ This ciphertext matches the expected result!")
            break
        else:
            print("❌ This ciphertext does not match the expected result.")


def bytes_to_chunks(b: bytes, chunk_size: int, quiet_mode=True) -> list[bytes]:
    """Convert bytes to chunks of a specified size."""
    chunks = [b[i : i + chunk_size] for i in range(0, len(b), chunk_size)]

    if not quiet_mode:
        print(
            f"🔢 Converted {len(b)} bytes into {len(chunks)} chunks of size {chunk_size} bytes each."
        )

    return chunks
