import sys
import pytest


def main():
    args = [
        "-q",
        "/home/src/tests",
    ]
    exit_code = pytest.main(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
