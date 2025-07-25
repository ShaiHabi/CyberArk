Work Summary Report – Shay Habi

This document provides a detailed report of the development stages, the reasoning behind my decisions, and my implementation choices throughout the project.In the git you may find the PDF of this document as well.

Initial Setup and Exploration:

While reviewing the instruction document, I encountered two language models I wasn’t previously familiar with: Microsoft’s PHI4 and Google’s gemma3b. Therefore, my first step was to research these models, understand their characteristics, capabilities, and usage methods. I did so by reading relevant documentation, watching YouTube tutorials, and consulting other language models.

In my next step, and in accordance with the guidelines that initially referenced PHI4, I began working with this model, including installation and code integration.



Pseudocode – Design-Level Guidelines:

At a high level, I defined three main principles to guide the tool’s implementation:

Modularity:

One of the guiding principles in this project was to maintain a modular codebase. This was reflected early on in the way input validation was handled, allowing the user to provide either a relative or absolute path to the gemma3b model directory.

To improve readability and avoid code duplication, I implemented methods such as failure\_message and writing\_prompt, which handled recurring logic and helped keep the code organized and maintainable.

Security:

Assuming that input files, including those supplied as part of the exercise, could be malicious, I took steps to ensure that the model would not run any code unintentionally. Therefore, the tool first opens the provided file in read-only mode, and each line was stored with its corresponding line number for traceability during later vulnerability reporting.

Output Quality Optimization:

To improve the accuracy and clarity of the model’s output, and to help the model generate the most accurate results possible, I designed three complementary strategies: overlapping between code blocks, maintaining a running log of previously identified issues, and generating a final summary based on the complete list of findings. These approaches - and the decisions made regarding their use - are discussed in more detail later in the report.





Pseudocode – Design-Level Guidelines:

To build the required tool, I implemented several key methods as outlined below

Main:

In addition to being the entry point of the program, this method handles all user input validation. First, it checks whether a file was provided for analysis and ensures that the file has a .c or .cpp extension, as required. Next, it verifies whether the user specified a path to the directory containing the gemma3b model files. If not, the method attempts to locate the default directory as described in the instructions (README.md). If both validations pass, the method proceeds to call extract\_content\_safely followed by using\_model.



extract\_content\_safely:

Although the file is received as a string and cannot be executed (which ensures that if it contains malicious code, neither the computer nor the user would be affected), the tool, through this method, reads the file in read-only mode. As part of this process, each line is read and assigned a line number, which is appended to the line from that point onward.



using\_model:

This method implements the core functionality of the tool. In the submitted version, all prompts are processed using Google’s gemma3b model. The method first calls join\_for\_model to divide the file’s separated lines of code into blocks. Each block is then passed to the model using a tailored prompt, generated via the writing\_prompt method. The model’s response is printed directly to the user.



Originally, this method was designed to support an additional mechanism: tracking previously detected problematic lines. Given the model’s limitations (lack of memory across prompts and a strict token limit for prompt+response), I aimed to give the model a sense of “memory” by including, in each new prompt, a list of findings from earlier blocks. The idea was that by passing this context forward, the model could build on prior insights and produce more comprehensive results.



This idea was meant to work in parallel with block overlapping (explained later). However, due to prompt size constraints and unsatisfactory test results, I ultimately decided to abandon this approach.



Still, not wanting to discard the idea of “findings tracking” altogether, I implemented a separate mechanism for post-analysis summarization. In this version, the model analyzes each block individually while storing its conclusions in a dedicated array (rather than printing them immediately). Once all blocks are processed, the tool calls join\_for\_model and writing\_prompt again - this time to prompt the model to generate a final summary based on its earlier findings.

Unfortunately, testing revealed that this method was also ineffective: the model often expected user input, generated overly verbose responses, or failed to focus on more critical issues. As a result, I decided to drop this approach as well.



join\_for\_model:

Both models, Google’s gemma3b and Microsoft’s PHI4, have a combined limit on the prompt and response length. If this limit is exceeded, the model may either throw an error or stop generating a response before completing it. At the same time, I wanted to avoid passing each line of code to the model individually - as this would strip the context and likely result in inaccurate analysis.

My solution to both challenges was as follows: I took the separated, numbered lines of code (produced by the extract\_content\_safely method) and grouped them into blocks that fit within a predefined character limit. Each block was then sent to the model for analysis. The block size was adjusted across different versions of the tool. Initially, I used a limit of around 6000 characters, which I understood to be the typical capacity supported by the PHI4 model. However, once I transitioned to the lighter gemma3 model, I gradually reduced the block size to 750 characters. This wasn’t a one-time change - it came after extensive experimentation with different prompt structures and model responses, during which I found that smaller blocks consistently yielded better and more manageable output.

Indeed, in practice, this approach yielded noticeably better results compared to sending individual lines to the model. When working with full blocks, the model was able to skip irrelevant lines and, in some cases, even identify logical connections between related lines within the same block when detecting security issues.

I also considered the possibility that a malicious actor could craft an extremely long line of code to disrupt the model’s behavior. To address this, I added logic during the block-building process to detect and handle such cases. If an unusually long line was found, it was split into smaller, valid sub-blocks. While this is a rare edge case in my view, I preferred to err on the side of caution.

Finally, I should note that the method was originally intended to support slight overlap between adjacent blocks - to help preserve context between them, such as cases where a function is split across blocks. The initial design included an overlap of about 1000 characters, which I later reduced to just the last 3 lines of the previous block. However, due to the switch to gemma3 and the need to minimize prompt size, I ultimately dropped this feature.



writing\_prompt:

As its name suggests, this method generates the prompt that is sent to the model for analysis, together with the relevant block of code described earlier. Originally, this function was designed for use with the PHI4 model, which required separating the prompt into system and user components. However, even after switching to the gemma3 model, I chose to keep the original implementation, as it was well-structured and produced good results with gemma3 as well.

Additionally, the method was initially designed to support two modes: file and summarize. The first mode was used to send each block of original code lines for analysis. The second mode was intended to generate a prompt for summarizing findings collected during the earlier stage, as part of an idea that was later dropped.



Challenges Encountered During Development:

As noted in Section 3, most of the challenges I faced during implementation stemmed from working with local language models:

Initially, my focus was on interacting with the PHI4 model. Although I found several creative ways to work around its input length limitations, the model failed to respond, even after extended execution times. After a long period of running time with no response, I concluded that the model was too heavy for my computer and that I needed to switch to the lighter gemma3 model.

The main challenge with gemma3 was prompt formulation. In many cases, the model’s responses did not align with what I was asking. After many hours of trial and error, I discovered that moving the block content to the beginning of the prompt - before the instruction text - led to a dramatic improvement in the model’s output.

This simple change made a significant difference and became the foundation for the final version of the tool. While the output is still not perfect and some model limitations remain, the results were far better than earlier attempts and aligned much more closely with the assignment’s requirements.

Due to time constraints and personal circumstances, I could not continue refining the prompts further. I chose to submit a working version that met the core requirements, rather than risk submitting an incomplete or less reliable solution.



