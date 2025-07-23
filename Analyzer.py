#Shay Habi

import sys


def main():
    if len(sys.argv) != 2:
        print("Error: Expected one input only of C or C++ input file.")
        sys.exit(1)

    file = sys.argv[1]
    extension = (file.split(".")[-1]).lower()
    if extension not in ["c", "cpp"]:
        print("Error: Invalid input file.")
        sys.exit(1)


if __name__ == "__main__":
    main()