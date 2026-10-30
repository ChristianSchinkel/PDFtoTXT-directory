#!/usr/bin/env python3
"""App startup script."""
import sys
from src.main import main as main_func


def main() -> None:
    """Run the main function from src.main."""
    raise SystemExit(main_func(sys.argv[1:]))


if __name__ == "__main__":
    main()
