# https://cryptopals.com/sets/1/challenges/7

# """Challenge 7: AES in ECB mode
# This challenge involves implementing AES encryption in ECB mode.
# The input is a plaintext string, and the key is a fixed 16-byte key.
# The challenge is to correctly implement the AES algorithm and handle padding.
# The output should be the decrypted ciphertext in hex format - this is to avoid issues with byte padding in ECB mode.
# """

import os

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto import Random
from PIL import Image

AES_KEY = b"YELLOW SUBMARINE"  # Fixed 16-byte key for AES in ECB mode


def run_challenge(input_data: str):
    """Challenge 7: AES in ECB mode."""
    print("🔐 Implementing AES encryption in ECB mode...")

    if not input_data:
        # Load input data from file if not provided
        with open(f"{os.getcwd()}/challenges/inputs/challenge_07.txt", "r") as f:
            input_data = f.read().strip()

    print("📥 Input (base64):", input_data)

    with open(f"{os.getcwd()}/challenges/results/challenge_07.txt", "r") as f:
        result_plaintext = f.read().strip()

    print("🏁 Expected Result (hex):", result_plaintext)

    # Decode the base64 input data
    try:
        ciphertext = b64decode(input_data)
    except Exception as e:
        print(f"❌ Error decoding input data: {e}")
        return

    print("🔓 Decrypting ciphertext...")

    try:
        plaintext = aes_ecb_decrypt(ciphertext, AES_KEY).hex()
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return

    print("🔓 Decrypted Ciphertext (hex):", plaintext)

    if plaintext == result_plaintext:
        print("✅ Decryption successful!")
    else:
        print("❌ Decryption did not match expected result.")

    print("🖼️ Bonus: Encrypting the penguin image...")

    image = Image.open(f"{os.getcwd()}/challenges/assets/penguin.png").convert('RGBA').convert('RGB')
    key = Random.new().read(AES.key_size[0])  # Generate a random key of the appropriate size

    print("🔒 Encrypting image in ECB mode...")
    encrypt_image(image, key, AES.MODE_ECB).save(
        f"{os.getcwd()}/challenges/assets/encrypted_penguin_ecb.png"
    )

    print("🔒 Encrypting image in CBC mode...")
    iv = Random.new().read(AES.block_size)
    encrypt_image(image, key, AES.MODE_CBC, iv).save(
        f"{os.getcwd()}/challenges/assets/encrypted_penguin_cbc.png"
    )


def aes_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt ciphertext using AES in ECB mode with the given key."""
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def encrypt_image(image: Image, key: bytes, mode: int = AES.MODE_ECB, iv: bytes = b'') -> Image:
    image_array = bytes(image.tobytes())
    padding_length = AES.block_size - len(image_array) % AES.block_size
    image_array += bytes(padding_length * ".", "UTF-8")  # Just an arbitrary padding byte

    if mode == AES.MODE_CBC and not iv:
        raise ValueError("IV must be provided for CBC mode")
    elif mode not in (AES.MODE_ECB, AES.MODE_CBC):
        raise ValueError("Unsupported AES mode. Use AES.MODE_ECB or AES.MODE_CBC.")
    
    if mode == AES.MODE_CBC:
        aes = AES.new(key, mode, iv)
    else:
        aes = AES.new(key, mode)

    encrypted_image = aes.encrypt(image_array)
    encrypted_image = encrypted_image[:-padding_length]

    return Image.frombytes("RGB", image.size, encrypted_image, "raw", "RGB")