#!/usr/bin/env python3
"""
Crypto Challenge - Main Script
A Python script for cryptographic challenges and exercises.
"""

import argparse
import sys
import os
import importlib
import re

from typing import Optional


def load_challenges():
    """Dynamically load all challenge modules from the challenges directory."""
    challenges_dir = os.path.join(os.getcwd(), "challenges")
    challenge_modules = {}

    if not os.path.exists(challenges_dir):
        print("❌ Challenges directory not found!")
        return {}

    # Find all challenge_XX.py files
    for filename in sorted(os.listdir(challenges_dir)):
        if filename.startswith("challenge_") and filename.endswith(".py"):
            # Extract challenge number from filename
            match = re.match(r"challenge_(\d+)\.py", filename)
            if match:
                challenge_num = int(match.group(1))
                module_name = f"challenges.challenge_{challenge_num:02d}"

                try:
                    # Dynamically import the module
                    module = importlib.import_module(module_name)
                    if hasattr(module, "run_challenge"):
                        challenge_modules[challenge_num] = module.run_challenge
                        print(f"✅ Loaded challenge {challenge_num}")
                    else:
                        print(
                            f"⚠️  Challenge {challenge_num} missing run_challenge function"
                        )
                except ImportError as e:
                    print(f"❌ Failed to import challenge {challenge_num}: {e}")

    return challenge_modules


# Load all available challenges dynamically
CHALLENGE_FUNCTIONS = load_challenges()


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Crypto Challenge Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python main.py --list                    # List all available challenges
            python main.py --challenge 1             # Run challenge 1
            python main.py -c 1                      # Short form
            python main.py --challenge 1 --input "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
            python main.py --all                     # Run all challenges
        """,
    )

    parser.add_argument(
        "-c", "--challenge", type=int, help="Run specific challenge number"
    )

    parser.add_argument("-i", "--input", type=str, help="Input data for the challenge")

    parser.add_argument(
        "-l", "--list", action="store_true", help="List all available challenges"
    )

    parser.add_argument("--all", action="store_true", help="Run all challenges")

    args = parser.parse_args()

    # Display banner
    print("🔐 Crypto Challenge Runner")
    print("=" * 40)

    if args.list:
        list_challenges()
    elif args.all:
        run_all_challenges()
    elif args.challenge:
        run_challenge(args.challenge, args.input)
    else:
        # Interactive mode if no arguments provided
        interactive_mode()


def list_challenges():
    """List all available challenges."""
    challenges = get_challenge_list()
    print("\nAvailable Challenges:")
    print("-" * 20)
    for num, desc in challenges.items():
        print(f"{num:2d}. {desc}")
    print(f"\nTotal: {len(challenges)} challenges")


def get_challenge_list():
    """Return dictionary of available challenges based on loaded modules."""
    # Default descriptions for known challenges
    challenge_descriptions = {
        1: "Convert hex to base64",
        2: "Fixed XOR",
        3: "Single-byte XOR cipher",
        4: "Detect single-character XOR",
        5: "Implement repeating-key XOR",
        6: "Break repeating-key XOR",
        7: "AES in ECB mode",
        8: "Detect AES in ECB mode",
        9: "Implement PKCS#7 padding",
        10: "Implement CBC mode encryption",
    }

    # Build list from actually loaded challenges
    available_challenges = {}
    for challenge_num in sorted(CHALLENGE_FUNCTIONS.keys()):
        description = challenge_descriptions.get(
            challenge_num, f"Challenge {challenge_num}"
        )
        available_challenges[challenge_num] = description

    return available_challenges


def run_challenge(challenge_num: int, input_data: Optional[str] = None):
    """Run a specific challenge."""
    challenges = get_challenge_list()

    if challenge_num not in challenges:
        print(f"❌ Challenge {challenge_num} not found!")
        print("Use --list to see available challenges.")
        return

    print(f"\n🚀 Running Challenge {challenge_num}: {challenges[challenge_num]}")
    print("-" * 50)

    try:
        # Use the dynamically loaded function
        if challenge_num in CHALLENGE_FUNCTIONS:
            CHALLENGE_FUNCTIONS[challenge_num](input_data)
        else:
            print(f"⚠️  Challenge {challenge_num} not implemented yet!")

    except Exception as e:
        print(f"❌ Error running challenge {challenge_num}: {e}")


def run_all_challenges():
    """Run all implemented challenges."""
    challenges = get_challenge_list()
    print(f"\n🏃 Running all {len(challenges)} challenges...\n")

    for challenge_num in challenges.keys():
        run_challenge(challenge_num)
        print()  # Add spacing between challenges


def interactive_mode():
    """Interactive mode for selecting challenges."""
    while True:
        print("\n📋 Interactive Mode")
        print("1. Run specific challenge")
        print("2. List challenges")
        print("3. Run all challenges")
        print("4. Exit")

        try:
            choice = input("\nSelect an option (1-4): ").strip()

            if choice == "1":
                challenge_num = int(input("Enter challenge number: "))
                input_data = input(
                    "Enter input data (optional, press Enter to skip): "
                ).strip()
                if not input_data:
                    input_data = None
                run_challenge(challenge_num, input_data)
            elif choice == "2":
                list_challenges()
            elif choice == "3":
                run_all_challenges()
            elif choice == "4":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid option. Please choose 1-4.")

        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
