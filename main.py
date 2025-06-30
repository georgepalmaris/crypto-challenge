#!/usr/bin/env python3
"""
Crypto Challenge - Main Script
A Python script for cryptographic challenges and exercises.
"""

import argparse
import sys

from typing import Optional
from challenges.challenge_01 import run_challenge as run_challenge_1
from challenges.challenge_02 import run_challenge as run_challenge_2
from challenges.challenge_03 import run_challenge as run_challenge_3
from challenges.challenge_04 import run_challenge as run_challenge_4
from challenges.challenge_05 import run_challenge as run_challenge_5
from challenges.challenge_06 import run_challenge as run_challenge_6
from challenges.challenge_07 import run_challenge as run_challenge_7

# from challenges.challenge_08 import run_challenge as run_challenge_8


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
    """Return dictionary of available challenges."""
    return {
        1: "Convert hex to base64",
        2: "Fixed XOR",
        3: "Single-byte XOR cipher",
        4: "Detect single-character XOR",
        5: "Implement repeating-key XOR",
        6: "Break repeating-key XOR",
        7: "AES in ECB mode",
        8: "Detect AES in ECB mode",
        # Add more challenges as you implement them
    }


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
        if challenge_num == 1:
            run_challenge_1(input_data)
        elif challenge_num == 2:
            run_challenge_2(input_data)
        elif challenge_num == 3:
            run_challenge_3(input_data)
        elif challenge_num == 4:
            run_challenge_4(input_data)
        elif challenge_num == 5:
            run_challenge_5(input_data)
        elif challenge_num == 6:
            run_challenge_6(input_data)
        elif challenge_num == 7:
            run_challenge_7(input_data)
        # elif challenge_num == 8:
        #     run_challenge_8(input_data)
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
