import argparse

from config import DEFAULT_OUTPUT_FILE


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch information about a VK user.")
    parser.add_argument("user_id", nargs="?", default="self", help="VK user ID (default is the current user).")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Path to the output file (default is {DEFAULT_OUTPUT_FILE}).",
    )
    return parser.parse_args()
