# https://cryptopals.com/sets/1/challenges/4

# """Challenge 4: Detect single-character XOR
# This challenge involves detecting a single-character XOR cipher in a list of hexadecimal strings.
# The input is a file containing multiple lines of hexadecimal strings, and the output is the decoded
# string with the highest score based on letter frequency analysis.
# """

import os

from challenges.challenge_03 import ScoredGuess, crack_single_byte_xor, get_freqs
from dataclasses import astuple
from string import ascii_lowercase


def run_challenge(input_data: str):
    """Challenge 4: Detect single-character XOR."""

    print("🔍 Attempting to find a single-byte XOR cipher...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_04.txt", "r") as f:
            input_data = [line.strip() for line in f if line.strip()]

    print("📥 Input (hexs):", input_data)

    lines = [bytes.fromhex(line) for line in input_data]

    with open(f"{os.getcwd()}/challenges/results/challenge_04.txt", "r") as f:
        result_text = f.read().strip()

    print("🏁 Expected Result (text):", result_text)

    with open(f"{os.getcwd()}/challenges/assets/frankenstein.txt", "r") as f:
        book = f.read()

    english_frequencies = get_freqs(text=book, letters=ascii_lowercase)

    print("🔍 Analyzing hexadecimal strings")

    overall_best = ScoredGuess()
    for line in lines:
        print(end=".", flush=True)
        candidate = crack_single_byte_xor(line, english_frequencies)
        overall_best = min(overall_best, candidate)

    score, key, _, plaintext = astuple(overall_best)
    print()
    print(
        f"Key: {chr(key)}, Score: {score:.4f}, Decoded Text: {plaintext.decode('utf-8', errors='ignore')}"
    )

    if plaintext.decode("utf-8", errors="ignore").strip() == result_text:
        print("✅ Decoding successful!")
    else:
        print("❌ Decoding did not match expected result.")  