**Analyzer.py**
Author: Shay Habi

**1. Goal:**
This Python tool is a LLM-based analyzer that scans C/C++ source code files for potential vulnerabilities and security issues using Google's **GEMMA-3B:1B** model.  
It analyzes the provided code and prints a list of detected vulnerabilities or security-relevant patterns found in the file.
The tool runs entirely locally, with no internet connection required.

**2. Requirements:**
To use this tool, make sure that:
a. Google's gemma31b moodle is already downloaded and available locally in your computer.
b. The following Python libraries are installed: transformers, torch, safetensors, huggingface\_hub.

**3. Usage:**
To run this tool via Terminals, provide the following arguments:
a. Source File(required):
A C/CPP file - MUST.
b. Model Folder Path (Optional):
A path to a folder containing gemma31b's files. Notice:
i. If provided, one must enter the actual(not relative) path to the relevant folder.
ii. If no path is provided, the tool uses a default **relative** path named "default\_gemma31b\_model".  
In that case, make sure that this folder exists in the **same folder as "Analyzer.py"**, and that it contains all the required model files.
c. Example usage:
To run this tool, write the following in the Terminal:
> python  Analyzer.py file\_name  path\_to\_model
For instance: > py Analyzer.py notes.cpp C:\\Users\\Shay\\Desktop\\gemma\_model (actuacl path)
For instance: > py Analyzer.py notes.cpp default\_gemma31b\_model (relative path)



Note: The analysis process may take some time, depending on the size of the input file.



**4. Project's architecture:**
The project is divided into three main stages:
a. Safe Reading:
The tool safely reads the file's contents **without executing it**, line by line, and numbering the lines.
Notice, that even empty lines (in the original file) are numbered.
b. Block Splitting:
The lines are grouped into blocks (up to max size of 750 chars), to ensure compatibility with the model's input constraints.
c. Model Inference:
Each block is passed to the model for analysis. The model's response for each block is printed to the user.

