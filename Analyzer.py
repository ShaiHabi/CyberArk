#Shay Habi
import os
import sys


def extract_content_safely(file):
    """
    Extracts the file's content securely in order to give it to PHI4 model.
    Minimizing the risk of executing the file, which may be malicious.
    """
    try:
        with open(file, "r") as f:
            content = f.read()
            return content

    except Exception as error:
        message = "Reading File Error: {}.".format(error)
        failure_message(message)


def using_PHI4(content, path_to_phi4):

    # Trying to use the model:
    try:
        pass

    except Exception as error:
        message = "Using PHI4 Error: {}.".format(error)
        failure_message(message)


def failure_message(message):
    print(message)
    print("Due to the error above, analyzing stopped.\n")
    sys.exit(1)


def main():

    # Checking the input arguments:
    length = len(sys.argv)
    if length not in [2,3]:
        message = "Invalid Input Error: A valid input must contain a C\\C++ file, and a path to local PHI4 (optional)."
        failure_message(message)

    file = sys.argv[1]
    extension = os.path.splitext(file)[1].lower()
    if extension not in [".c", ".cpp"]:
        message = "Invalid Input Error: Incorrect file extension."
        failure_message(message)

    if length == 3:
        path_to_phi4 = sys.argv[2]
        if not (os.path.exists(path_to_phi4)):  # Just validating the existence of the path, not its content
            message = "Invalid Input Error: Invalid PHI4' path."
            failure_message(message)

    else:  # length == 2
        print("Clarification: No path to local PHI4 was given. Using default path instead.")
        path_to_phi4 = "default_PHI4_model"

    content = extract_content_safely(file)
    using_PHI4(content, path_to_phi4)


if __name__ == "__main__":
    main()