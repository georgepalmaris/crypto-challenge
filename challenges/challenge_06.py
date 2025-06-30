# https://cryptopals.com/sets/1/challenges/4

# """Challenge 6: Break repeating-key XOR
# This challenge involves breaking a repeating-key XOR cipher.
# The input is a ciphertext string and the goal is to recover the original plaintext.
# The challenge is to identify the key used for encryption and decrypt the ciphertext.
# The output should be the recovered plaintext.
# """

import os

from challenges.challenge_02 import bytes_xor
from challenges.challenge_03 import crack_single_byte_xor
from challenges.challenge_05 import repeating_key_xor
from itertools import combinations
from base64 import b64decode
from pprint import pprint

MAX_KEY_SIZE = 40  # Maximum key size to consider for the repeating-key XOR cipher


def run_challenge(input_data: str):
    """Challenge 6: Break repeating-key XOR."""

    print(f"{hamming_distance(b'this is a test', b'wokka wokka!!!')=}  ")
    if hamming_distance(b"this is a test", b"wokka wokka!!!") != 37:
        exit("Hamming distance test failed! :(")

    print("🔓 Attempting to break a repeating-key XOR cipher...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_06.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (base64):=\n")
    print(input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_06.txt", "r") as f:
        result_text = f.read().strip()

    print()
    print("🏁 Expected Result (text)=\n")
    print(result_text)

    # Decode the base64 input data
    try:
        ciphertext = b64decode(input_data)
    except Exception as e:
        print(f"❌ Error decoding input data: {e}")
        return

    key_sizes = guess_key_size(ciphertext, num_guesses=5)

    print()
    print("🔑 Guessed Key Sizes (confidence, size):")
    pprint(key_sizes)
    print()

    candidates = [crack_repeating_key_xor(ciphertext, size) for _, size in key_sizes]
    candidates.sort()
    best_candidate = candidates[0]
    best_key = best_candidate[1]

    print(f"🏆 Best Key: {best_key}, Score: {best_candidate[0]:.4f}")
    print("🔓 Attempting to decrypt with the best key...")

    plaintext = (
        repeating_key_xor(best_key, ciphertext).decode("utf-8", errors="ignore").strip()
    )

    print()
    print("plaintext =\n")
    print(plaintext)

    if plaintext == result_text:
        print("✅ Decoding successful!")
    else:
        print("❌ Decoding did not match expected result.")


def crack_repeating_key_xor(ciphertext: bytes, key_size: int) -> tuple[float, bytes]:
    """Crack a repeating-key XOR cipher given the ciphertext and key size."""
    # Split the ciphertext into chunks of each byte with a gap of the given key size.
    chunks = [ciphertext[i::key_size] for i in range(key_size)]
    cracks = [crack_single_byte_xor(chunk) for chunk in chunks]

    combined_score = sum(guess.score for guess in cracks) / key_size
    key = bytes(guess.key for guess in cracks)
    return combined_score, key


def guess_key_size(ciphertext: bytes, num_guesses: int = 1) -> list[tuple[float, int]]:
    """Guess the key size for a repeating-key XOR cipher based on Hamming distance."""

    def get_score(size: int) -> float:
        # This is 4 KEYSIZE chunks of the ciphertext.
        chunks = (
            ciphertext[:size],
            ciphertext[size : 2 * size],
            ciphertext[2 * size : 3 * size],
            ciphertext[3 * size : 4 * size],
        )

        # Calculate the Hamming distance between each pair of chunks
        # This is the sum of the average hamming distance between each pair of chunks
        chunk_combinations = combinations(chunks, 2)
        average_distance = sum(
            hamming_distance(a, b) for a, b in chunk_combinations
        ) / (sum(1 for _ in chunk_combinations) or 1)
        return average_distance / size

    # Generate scores for key sizes from 2 to MAX_KEY_SIZE
    scores = [(get_score(size), size) for size in range(2, MAX_KEY_SIZE + 1)]
    scores.sort()
    return scores[:num_guesses]


# This is crucial for finding the repeating XOR key size.
# It calculates the Hamming distance between two byte strings.
# The Hamming distance is the number of differing bits between two strings of equal length.
def hamming_distance(s1: bytes, s2: bytes) -> int:
    """Calculate the Hamming distance between two byte strings."""
    if len(s1) != len(s2):
        raise ValueError("Strings must be of equal length")

    # Count the number of differing bits
    return sum([hamming_weight(byte) for byte in bytes_xor(s1, s2)])


# This function calculates the Hamming weight of a byte.
# The Hamming weight is the number of 1 bits in the binary representation of the byte
def hamming_weight(byte: bytes) -> int:
    """Calculate the Hamming weight (number of 1 bits) in a byte."""
    return bin(byte).count("1")
