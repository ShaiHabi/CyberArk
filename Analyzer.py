#Shay Habi

import sys
import os
import transformers


def extract_content_safely(file):
    """
    Extracts the file's content lines securely in order to give it to PHI4 model.
    Minimizing the risk of executing the file, which may be malicious.
    """
    try:
        with open(file, "r") as f:
            lines = f.readlines()  # List of strings
            result = ["{}: {}".format(i+1, line.strip()) for i, line in enumerate(lines)]
            return result

    except Exception as error:
        message = "Reading File Error: {}.".format(error)
        failure_message(message)


def split_for_model(text_lines, size=6000):
    """

    :param text_lines:
    :param size: chars
    :return:
    """

    number_of_lines = len(text_lines)
    line_index = 0
    blocks = []

    while line_index < number_of_lines:  # While we're still reading the text
        temp_block = []
        temp_total_chars = 0
        start = line_index


        # Creating the new block of lines
        while (line_index < number_of_lines) and (temp_total_chars + len(text_lines[line_index]) < size):
            temp_block.append(text_lines[line_index])
            temp_total_chars += len(text_lines[line_index])
            line_index += 1

        if start == line_index:  # len(line)> size. Extremely edge case.
            line = text_lines[line_index]
            temp_blocks = [line[j:j+size] for j in range(0, len(line), size) ]
            blocks.extend(temp_blocks)  # Each new block is already a string
            line_index += 1

        else:
            block_as_string = "\n".join(temp_block)
            blocks.append(block_as_string)

    return blocks


def build_prompt(text, classification, extension, relevant_data=None):
    """

    :param text:
    :param classification:
    :param extension:
    :param relevant_data:
    :param lines:
    :return:
    """

    system = {
        "role": "system",
        "content": "You're a security expert specializing in static code analysis of C/C++ code for vulnerabilities."
    }

    if classification == "file":
        prompt = ("You're conducting a static analysis for a {} code file to detect potential vulnerabilities and security flaws."
                  "The following block is part of the overall code, which was split to small sizes-blocks."
                  "Read it and carefully analyze this block and identify any potential vulnerabilities and security flaws."
                  "For each finding, your response should be as follow:"
                  "Line X: Possible <flaw/vulnerability> due to <give the reason here>.\n"
                  "Here is the {} code block: {}.".format(extension, extension, text))



    else:  # classification == "summarize"
        prompt = ("You've conducted a static analysis for a {} code file to detect potential vulnerabilities and security flaws."
                  "The following block is part of your overall findings."
                  "Read it carefully; If you have new conclusions, mention them in the reasoning section below."
                  "Otherwise, just repeat what is already written."
                  "Your response should follow this format, when you have the basic data you need in the block:"
                  "Line X : Possible <flaw/vulnerability> due to <give the reason here> \n."
                  "Here is the {} code block: {}". format(extension, extension, text))


    user = {"role": "user", "content": prompt}
    message = [system, user]
    return message


def using_model(content_lines, extension, path_to_phi4):
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
        blocks = split_for_model(content_lines)  # Splitting the content to small blocks for the model
        for block in blocks:
            temp_message = build_prompt(block, "file", extension, security_findings)  # Writing the prompt
            temp_output = pipeline(temp_message)  # Using the model
            security_findings.append(temp_output[0]["generated_text"])  # Saving the output

        # Here, we finished to use the model to examine the file's blocks.
        # Now, we use it again to summarize all the findings to final result:

        security_findings_as_string = "\n".join(security_findings)
        blocks = split_for_model(security_findings_as_string)  # For cases when the findings are too big for the model

        print ("Start Analyzing:")
        for block in blocks:
            temp_message = build_prompt(block, "summarize", extension)
            temp_output = pipeline(temp_message)
            print(temp_output[0]["generated_text"])

    except Exception as error:
        message = "Using Model Error: {}.".format(error)
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

    content_lines = extract_content_safely(file)

    if length == 3:
        path_to_phi4 = sys.argv[2]
        if not (os.path.exists(path_to_phi4)):  # Just validating the existence of the path, not its content
            message = "Invalid Input Error: The PHI4' path is invalid or not exist."
            failure_message(message)

    else:  # length == 2
        print("Note: No path to a local PHI4 was provided. Default path will be used instead.")
        path_to_phi4 = "default_PHI4_model"

    using_model(content_lines,extension, path_to_phi4)
    sys.exit(0)


if __name__ == "__main__":
    main()