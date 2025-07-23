#Shay Habi
import os
import sys


def extract_content_safely(file):
    """
    Extracts the file's content securely in order to give it to PHI4.
    Minimizing the risk of executing the file, which may be malicious.
    """
    try:
        with open(file, "r") as f:
            content = f.read()
            return content, True

    except Exception as error:
        print("Reading File Error: {}.\n".format(error))
        return None, False


def using_PHI4(content, path_to_phi4):
    pass


def main():

    # Checking the input arguments:
    length = len(sys.argv)
    if length not in [2,3]:
        print("Invalid Input Error: A valid input must contain a C\\C++ input file, and a path to local PHI4 (optional).\n")
        sys.exit(1)

    file = sys.argv[1]
    extension = os.path.splitext(file)[1].lower()
    if extension not in [".c", ".cpp"]:
        print("Invalid Input Error: Incorrect file extension.\n")
        sys.exit(1)

    if length == 3:
        path_to_phi4 = sys.argv[2]
    else:  # length == 2
        path_to_phi4 = "TOCOMPLETE" ###

    content, status = extract_content_safely(file)
    if not(status):
        sys.exit(1)

    print("Analyzing {}:".format(file))
    using_PHI4(content, path_to_phi4)




if __name__ == "__main__":
    main()