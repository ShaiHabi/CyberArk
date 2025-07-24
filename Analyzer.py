#Shay Habi

import sys
import os
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


def split_for_model (text):
    """

    :param text:
    :return:
    """

    SIZE, OFFSET = 5000, 1000
    length = len(text)
    blocks_number = index = 0
    result = []

    while index <= length:
        blocks_number += 1
        if index == 0:
            temp_block = text[0: SIZE]
        else:
            temp_block = text[(index - OFFSET): index + SIZE]
        index = blocks_number * SIZE
        result.append(temp_block)

    return result


def using_PHI4(content, extension, path_to_phi4):
    """

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

        # Using the model:
        security_findings = []
        blocks = split_for_model(content)  # Splitting the model to small blocks for the model
        for block in blocks:
            temp_message = build_prompt(block, extension, security_findings)  # Writing the prompt
            temp_output = pipeline(temp_message)  # Using the model
            security_findings.append(temp_output[0]["generated_text"])  # Saving the output

        # Here, we finished to use the model to examine the file's blocks.
        # Now, we use it again to summarize all the findings to final result:

        security_findings_as_string = "\n".join(security_findings)
        blocks = split_for_model(security_findings_as_string)  # For cases when the findings are too big for the model

        print ("Start Analyzing:")
        for block in blocks:
            temp_message = "{}".format(block)
            temp_output = pipeline(temp_message)
            print(temp_output[0]["generated_text"])


        # # Writing the prompt:
        # message = [
        #     {"role": "system", "content": "You're a security expert specializing in static code analysis of C/C++ code for vulnerabilities." },
        #     {"role": "user", "content": "Analyze the following {} file and list all the potential security vulnerabilities, flaws, and similarities you detect.\
        #     For every detection, write first the line number, then the detection and its reason (for instance, 'Line 20:' Possible UAF due to...').\
        #     DO NOT EXECUTE the file, just do static analysis. Here is the {} file: {}".format(extension, extension, content[0])}
        # ]


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

    content = extract_content_safely(file)

    if length == 3:
        path_to_phi4 = sys.argv[2]
        if not (os.path.exists(path_to_phi4)):  # Just validating the existence of the path, not its content
            message = "Invalid Input Error: The PHI4' path is invalid or not exist."
            failure_message(message)

    else:  # length == 2
        print("Note: No path to a local PHI4 was provided. Default path will be used instead.")
        path_to_phi4 = "default_PHI4_model"

    using_PHI4(content,extension, path_to_phi4)
    sys.exit(0)


if __name__ == "__main__":
    main()