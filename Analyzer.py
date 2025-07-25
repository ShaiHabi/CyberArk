#Shay Habi

import sys
import os
import transformers


def extract_content_safely(file):
    """
    Extracts the file's content lines securely, while minimizing the risk of executing the file, which may be malicious.
    Numbering each line according to its order.

    :param file: String
    :return: List of strings
    """
    try:
        with open(file, "r") as f:
            lines = f.readlines()  # List of strings
            result = ["Line {}: {}".format(i+1, line.strip()) for i, line in enumerate(lines)]
            return result

    except Exception as error:
        message = "Reading File Error: {}.".format(error)
        failure_message(message)


def join_for_model(text_lines, size=750):
    """
    Joins separated lines to blocks of maximum size, in order to give to Gemma3 and not exceeding the model's size limit.
    The blocks help the model to have "the bigger picture" instead of analyze each line separately.

    :param text_lines: List of strings (each index is separated line)
    :param size: int (maximum number of chars in each block)
    :return: List of *Strings*
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

        if start == line_index:  # len(line)> size. In rare cases when a single line might exceed the block size limit.
            line = text_lines[line_index]
            temp_blocks = [line[j:j+size] for j in range(0, len(line), size) ]
            blocks.extend(temp_blocks)  # Each new block is already a string
            line_index += 1

        else:
            block_as_string = "\n".join(temp_block)
            blocks.append(block_as_string)

    return blocks


def writing_prompt(text, extension):
    """
    Writing a prompt for gemma31b model.

    :param text: String (file's lines)
    :param extension: String
    :return: List of dictionaries
    """

    system = {
        "role": "system",
        "content": "You're a security expert specializing in static code analysis of C/C++ code for vulnerabilities.\n"
    }

    prompt = (
        "You conduct a static analysis for {} code file to detect potential vulnerabilities and security flaws.\n"
        "The following is segment of the whole code: \n {} \n" 
        "DO NOT REPORT lines without threat, vulnerability or security flaw. DO NOT REPORT safe code lines. \n"
        "You must report any line with potential threat, such as UAF, stack based buffer overflows, DOS, etc.\n"
        "NOTICE - DO NOT COPY THE LINE ITSELF, JUST THE NUMBER.\n"
        "Each report MUST be in this format:\n"
        "Line <number>: Possible <issue>, due to <few words reason>\n. \n".format(extension, text)
    )

    # return prompt
    user = {"role": "user", "content": prompt}
    message = [system, user]
    return message


def using_model(file_name, content_lines, extension, path_to_gemma3):
    """
    Model Analysis of the file's lines. This model calls for "join_for_model" method.
    For each block, the model's analysis is saved and later all the findings are sent for final conclusion.

    :param file_name: String
    :param content_lines: List of strings
    :param extension: String (file type)
    :param path_to_gemma3: String (path to relevant folder)
    :return: None
    """


    try:
        # Trying to use the model as required in the model's ReadMe file:
        # Loading the model:
        pipeline = transformers.pipeline(
            "text-generation",
            model="{}".format(path_to_gemma3),  # User's input or default path to gemma3 folder
            model_kwargs={"torch_dtype": "auto"},
            device_map="auto",
            max_new_tokens=1024
        )

        # Using the model:
        blocks = join_for_model(content_lines)  # Splitting the content to small blocks for the model
        print("\n=== Analyze {} ===".format(file_name))

        for block in blocks:
            temp_message = writing_prompt(block, extension)  # Writing the prompt
            temp_output = pipeline(temp_message)  # Using the model
            separated_lines = temp_output[0]["generated_text"][2]["content"]  # Model's generated text response only
            print(separated_lines)

        print(" === End of Analysis === ")

    except Exception as error:
        message = "Using Model Error: {}.".format(error)
        failure_message(message)


def failure_message(message):
    """
    Prints an error message to the user and terminates the program.

    :param message: String
    :return: None
    """
    print(message)
    print("Analysis stopped due to the error above.\n")
    sys.exit(1)


def main():
    # Checking the provided arguments:
    length = len(sys.argv)
    if length not in [2,3]:
        message = "Invalid Input Error: A valid input must contain a C/C++ file, and a path to local gemma31b (optional)."
        failure_message(message)

    file = sys.argv[1]
    extension = os.path.splitext(file)[1].lower()
    if extension not in [".c", ".cpp"]:
        message = "Invalid Input Error: Unsupported file extension."
        failure_message(message)

    # Extracting and numbering the file's lines:
    content_lines = extract_content_safely(file)  # returns a list of strings

    # Path to the model's files:
    if length == 3:
        path_to_gemma3 = sys.argv[2]

    else:  # length == 2
        print("Note: No path to a local gemma3:1b was provided. Default path will be used instead.")
        path_to_gemma3 = "default_gemma31b_model"

    if not (os.path.exists(path_to_gemma3)):  # Just validating the existence of the path, not its content
        message = "Invalid Input Error: The gemma3b1 path is invalid or does not exist."
        failure_message(message)

    # Sending to the model analysis:
    using_model(file, content_lines,extension, path_to_gemma3)
    sys.exit(0)


if __name__ == "__main__":
    main()