# https://cryptopals.com/sets/1/challenges/3

# """Challenge 3: Single-byte XOR cipher
# This challenge involves decoding a single-byte XOR cipher.
# The input is a hexadecimal string, and the output is the decoded ASCII string.
# The challenge is to find the single byte that was used for the XOR operation.
# We used Frankenstein.txt as the text to analyze the frequency of letters.
# """

import os
import plotext as plt

from collections import Counter
from string import ascii_lowercase
from typing import Optional
from challenges.challenge_02 import bytes_xor
from dataclasses import dataclass, astuple


@dataclass(order=True)
class ScoredGuess:
    """Data class to hold a scored guess for the single-byte XOR cipher."""

    score: float = float("inf")  # Initialize with a high score
    key: Optional[bytes] = None  # The cipher key used for XOR
    ciphertext: Optional[bytes] = None  # The ciphertext being decoded
    plaintext: Optional[bytes] = None  # The resulting plaintext after decoding

    @classmethod
    def from_key(
        cls, ciphertext: bytes, key: bytes, english_frequencies: dict[str, float]
    ) -> "ScoredGuess":
        """Create a ScoredGuess from ciphertext and key."""
        full_key = bytes([key]) * len(
            ciphertext
        )  # Repeat key to match ciphertext length
        plaintext = bytes_xor(ciphertext, full_key)
        score = fitting_quotient(plaintext, english_frequencies)
        return cls(score=score, key=key, ciphertext=ciphertext, plaintext=plaintext)


def run_challenge(input_data: str):
    """Challenge 3: Single-byte XOR cipher."""
    print("⊕ Attempting to decode a single-byte XOR cipher...")

    if not input_data:
        with open(f"{os.getcwd()}/challenges/inputs/challenge_03.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (hex):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_03.txt", "r") as f:
        result_text = f.read().strip()

    print("🏁 Expected Result (text):", result_text)

    with open(f"{os.getcwd()}/challenges/assets/frankenstein.txt", "r") as f:
        book = f.read()

    english_frequencies = get_freqs(text=book, letters=ascii_lowercase)
    
    print(f"📊 Letter Frequencies in Frankenstein.txt:")

    plot_letter_frequencies(english_frequencies)

    if input_data:
        try:
            input_bytes = bytes.fromhex(input_data)
            print()
            print("🔓 Decoding input...")

            guess = crack_single_byte_xor(input_bytes, english_frequencies)

            print(f"🏁 Best guess for the single-byte XOR cipher:")

            print()
            guess_frequencies = get_freqs(guess.plaintext.decode("utf-8", errors="ignore"), ascii_lowercase)
            plot_letter_frequencies(english_frequencies, guess_frequencies, title=f"Best Guess (Key: {chr(guess.key)})")
            print()
   
            score, key, _, plaintext = astuple(guess)
            print(
                f"Key: {chr(key)}, Score: {score:.4f}, Decoded Text: {plaintext.decode('utf-8', errors='ignore')}"
            )

            if guess.plaintext.decode("utf-8", errors="ignore") == result_text:
                print("✅ Decoding successful!")
            else:
                print("❌ Decoding did not match expected result.")
        except Exception as e:
            print(f"❌ Error processing input: {e}")
    else:
        print("❌ No input data provided.")


def get_freqs(text, letters) -> dict[str, float]:
    """Calculate frequency of letters in the text."""

    counts = Counter()

    for letter in letters:
        counts[letter] += text.count(letter)
    total = sum(counts.values())
    return {letter: counts[letter] / total for letter in letters}


def fitting_quotient(text: bytes, english_frequencies: dict[str, float]) -> float:
    """Score the text based on letter frequency."""
    score = 0.0
    l = len(text)

    for letter, frequency_expected in english_frequencies.items():
        frequency_actual = text.count(ord(letter)) / l
        score += abs(frequency_expected - frequency_actual)

    return score


def crack_single_byte_xor(
    ciphertext: bytes, english_frequencies: dict[str, float]
) -> ScoredGuess:
    """Crack a single-byte XOR cipher."""

    best_guess = ScoredGuess()

    for candidate_key in range(256):
        guess = ScoredGuess.from_key(ciphertext, candidate_key, english_frequencies)
        best_guess = min(best_guess, guess, key=lambda g: g.score)

    if best_guess.key is None or best_guess.plaintext is None:
        exit("❌ No valid key found for the single-byte XOR cipher.")

    return best_guess

def plot_letter_frequencies(frequencies: dict[str, float], compared_frequencies: dict[str, float] = None, title: str = "📊 Letter Frequency Distribution"):
    """Plot letter frequencies using plotext."""
    letters = list(frequencies.keys())
    values = list(frequencies.values())

    plt.clear_data()
    x_positions = list(range(len(letters)))
    plt.plot(x_positions, values, marker="braille", color="green")
    plt.title(title)

    if compared_frequencies:
        compared_values = list(compared_frequencies.values())
        plt.plot(x_positions, compared_values, marker="braille", color="blue")

    plt.xlabel("Letters (a-z)")
    plt.ylabel("Frequency")
    plt.plotsize(80, 20)
    plt.xticks([i for i in range(len(letters))], [letters[i] for i in range(len(letters))])
    plt.show()