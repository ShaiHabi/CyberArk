#Shay Habi
import os
import sys
import transformers

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


def using_PHI4(content, extension, path_to_phi4):
    """

    :param content:
    :param extension:
    :param path_to_phi4:
    :return:
    """


    try:
        # Trying to use the model as required in the model's ReadMe file:
        # Loading the model:
        pipeline = transformers.pipeline(
            "text-generation",
            model="{}".format(path_to_phi4),
            model_kwargs={"torch_dtype": "auto"},
            device_map="auto",
        )

        # Writing the prompt:
        message = [
            {"role": "system", "content": "You're a security expert specializing in static code analysis of C/C++ code for vulnerabilities." },
            {"role": "user", "content": "Analyze the following {} file and list all the potential security vulnerabilities, flaws, and similarities you detect.\
            For every detection, write first the line number, then the detection and its reason (for instance, 'Line 20:' Possible UAF due to...').\
            Here is the {} file: {}".format(extension, extension, content)}
        ]

        # Output:
        outputs = pipeline(message)
        print ("Start Analyzing:")
        print(outputs[0]["generated_text"])

    except Exception as error:
        message = "Using PHI4 Error: {}.".format(error)
        failure_message(message)


def failure_message(message):
    print(message)
    print("Analysis stopped due to the error above.\n")
    sys.exit(1)


def main():

    # Checking the input arguments:
    length = len(sys.argv)
    if length not in [2,3]:
        message = "Invalid Input Error: A valid input must contain a C/C++ file, and a path to local PHI4 (optional)."
        failure_message(message)

    file = sys.argv[1]
    extension = os.path.splitext(file)[1].lower()
    if extension not in [".c", ".cpp"]:
        message = "Invalid Input Error: Incorrect file extension."
        failure_message(message)

    if length == 3:
        path_to_phi4 = sys.argv[2]
        if not (os.path.exists(path_to_phi4)):  # Just validating the existence of the path, not its content
            message = "Invalid Input Error: The PHI4' path is invalid or not exist."
            failure_message(message)

    else:  # length == 2
        print("Note: No path to a local PHI4 was provided. Default path will be used instead.")
        path_to_phi4 = "default_PHI4_model"

    content = extract_content_safely(file)
    using_PHI4(content,extension, path_to_phi4)
    sys.exit(0)


if __name__ == "__main__":
    main()