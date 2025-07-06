# https://cryptopals.com/sets/2/challenges/13

# """Challenge 13: ECB cut-and-paste
# This challenge involves exploiting the fact that ECB mode is deterministic.
# The goal is to create a valid ciphertext by manipulating the blocks of an existing ciphertext.
# The challenge is to correctly implement the cut-and-paste attack and produce a valid ciphertext.
# The output should be the decrypted plaintext in hex format.
# """

import os

from Crypto.Cipher import AES

from challenges.challenge_09 import pkcs7_pad, pkcs7_unpad

KEY_SIZE = 32  # AES key size is 32 bytes for AES-256
_key = os.urandom(KEY_SIZE)  # Randomly generated key for AES encryption


def run_challenge(input_data: str):
    """Challenge 13: ECB cut-and-paste"""
    print("🔍 Implementing ECB cut-and-paste attack...")

    print("Step 1: Parse the profile string into a dictionary")

    with open(f"{os.getcwd()}/challenges/inputs/challenge_13.txt", "r") as f:
        input_data = f.read().strip().encode("utf-8")

    print("📥 Input (profile string):", input_data)

    if not input_data:
        print("❌ No input data provided!")
        return

    profile = profile_parse(input_data)

    print("Parsed Profile Dictionary:", profile)

    print("✅ Step 1 completed successfully.")

    print("Step 2: Build a profile string from a tuple of key-value pairs")

    profile_tuple = tuple((key, value) for key, value in profile.items())
    profile_string = profile_build(profile_tuple)

    print("Profile String (text):", profile_string.decode("utf-8", errors="ignore"))

    print("✅ Step 2 completed successfully.")

    print("Step 3: Create a profile string for the given email")

    email = b"test@example.com"
    profile_for_email = profile_for(email)

    print(
        "Profile for Email (text):", profile_for_email.decode("utf-8", errors="ignore")
    )

    print("✅ Step 3 completed successfully.")

    print("Step 4: Escalate privileges by manipulating the profile string")

    user_1 = b"foooo@bar.com"
    user_2 = user_1[:10] + pkcs7_pad(b"admin", AES.block_size) + user_1[10:]
    user_1_ciphertext: bytes = encrypt_profile(user_1)
    user_2_ciphertext: bytes = encrypt_profile(user_2)
    malicious_ciphertext: bytes = user_1_ciphertext[:32] + user_2_ciphertext[16:32]
    decrypted_malicious_profile = decrypt_profile(malicious_ciphertext)

    print(
        "Decrypted Malicious Profile (text):",
        decrypted_malicious_profile.decode("utf-8", errors="ignore"),
    )

    print("✅ Step 4 completed successfully.")

    role = decrypted_malicious_profile.split(b"&")[2].split(b"=")[
        1
    ]  # Extract the role from the profile
    if role == b"admin":
        print("🎉 Privilege escalation successful! User is now an admin.")
    else:
        print("❌ Privilege escalation failed. User is not an admin.")


def profile_parse(profile: bytes) -> dict[bytes, bytes]:
    """Parse the profile string into a dictionary."""
    kv_pairs = profile.split(b"&")
    parsed_dict = {key: value for key, value in [pair.split(b"=") for pair in kv_pairs]}
    return parsed_dict


def profile_build(t: tuple[tuple[bytes, bytes], ...]) -> bytes:
    """Build a profile string from a tuple of key-value pairs."""
    result = b"&".join(key + b"=" + value for key, value in t)
    return result


def profile_for(email: bytes) -> bytes:
    """Create a profile string for the given email."""
    email = email.translate(None, b"&=")  # Remove '&' and '=' characters
    profile = profile_build(
        (
            (b"email", email),
            (b"uid", b"10"),  # Fixed user ID
            (b"role", b"user"),  # Default role
        )
    )
    return profile


def encrypt_profile(email: bytes) -> bytes:
    """Encrypt the profile string for the given email."""
    profile = profile_for(email)
    cipher = AES.new(_key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(profile, AES.block_size))


def decrypt_profile(ciphertext: bytes) -> bytes:
    """Decrypt the profile string for the given email."""
    cipher = AES.new(_key, AES.MODE_ECB)
    return pkcs7_unpad(cipher.decrypt(ciphertext))
