** Analyzer.py **

1. Goal:
  This Python tool is a LLM-driven tool, that looks for code vulnerabilities in C\C++ code files.
  Thus, by using Google's GEMMA3B:1B  model.
  The tool works locally, namely without any internet connection.
2. Requirements:
   In order to use this tool, one must varify that:
   a. Google's gemma31b moodle is already exists locally in the computer.
   b. Those libraries are installed: transformers, torch, safetensors, huggingface_hub.
3. Usage:
   In order to use this tool via Terminals, one must provide 2 arguments:
   a. A C/CPP file - MUST.
   b. A path to a folder containing gemma31b's files - AN OPTION:
       i.In case the model is already exists, one can enter the actual path to the relevant folder.
       ii. Otherwise, if not providing any path, a default one will be chosen. This option assume there is a folder named "default_gemma31b_model" in with the model in the same folder that Analyzer.py exists.
   c. In order to use the tool, write the following in the terminal:
   >> py (or python)     Analyzer.py     file_name     path_to_model.
4. Project's architecture:
   The project can be seperated to 3 main sections:
   a. First, the code extract safetly (without execution of the file) the file's lines.
   b. Second, it seperate those lines to blocks (of max size) - in order to let the modle handle them correctly.
   c. Lastly, the model get each block and analyst it. Its response is printed for the user.
