# OpenAI assistent.
# Usage: python3 assistent.py [web]
# For web run using  `streamlit run assistent.py web`

"""
REPL loop with an OpenAI model running commands in a shell and I giving instructions to the model.
Several commands to run from one answer from the model.
I tried this loop to enhance the program itself. Meaning it issued commands to read its code and propose modifications to it. It only proposed some minor enhancements.
Streaming API: it outputs result token by token.
Web app partially. I asked it to generate a web app based on StreamLit. But it generated REPL inside it which was not functional. 

"""
import subprocess
from openai import OpenAI
import re
import streamlit as st


system_prompt = """You are being run in a scaffold in a bash shell on an Archlinux system. When you want to run a shell command, write it in a <bash> XML tag (example: "<bash> some command </bash>"), other things you say will be sent to the user. You will be shown the result of the command and be able to run more commands. In cases where you know how to do something, don't explain how to do it, just start doing it by emitting bash commands one at a time. You can't interact with stdin directly, so if you do things over ssh you need to run commands that will finish and return control to you rather than blocking on stdin. Don't wait for the user to say OK before suggesting a bash command to run, just say the command. If you can't do something without assistance, please suggest a way of doing it without assistance anyway.

Example:

Q: List all files in ~/ directory.

A: <bash>ls ~</bash>
"""


def main():
    client = OpenAI()
    print(f"SYSTEM: {system_prompt}")
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    while True:
        # Get command from user:
        command = input("> ")
        pattern = re.compile(r"<bash>(.*)</bash>")
        if command == "exit":
            break
        else:
            messages.append({"role": "user", "content": command})
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, stream=True
            )

            completion_text = ""
            # iterate through the stream of events
            for event in completion:
                event_text = event.choices[0].delta.content  # extract the text
                if event_text:
                    completion_text += event_text  # append the text
                    print(event_text, end="")
            print()

            # Find all matches of <bash> tags using regex and loop through them:
            for bash_command in re.findall(pattern, completion_text):
                # Ask user if to execute command:
                confirm = input(f"Run command? (Y/n): {bash_command} ")
                if confirm == "n":
                    continue
                try:
                    cprocess = subprocess.run(
                        bash_command, shell=True, capture_output=True
                    )
                    print(cprocess.stdout.decode("utf-8"))
                    messages.append(
                        {
                            "role": "user",
                            "content": "Output of the last command was: "
                            + cprocess.stdout.decode("utf-8"),
                        }
                    )
                except subprocess.CalledProcessError as error:
                    print(error.output.decode("utf-8"))
                    messages.append(
                        {
                            "role": "user",
                            "content": "Error executing command: "
                            + error.output.decode("utf-8"),
                        }
                    )


"""
def web():
    # Initialize Streamlit app
    st.title("Assistant")

    # Initialize OpenAI client and state
    client = OpenAI()
    messages = []

    # Display system prompt
    st.write(f"SYSTEM: {system_prompt}")
    messages.append({"role": "system", "content": system_prompt})

    counter = 0
    while True:
        # Get command input from user
        command = st.text_input("Enter your command:", key=f"command{counter}")
        counter += 1

        # Create button to execute command
        if st.button("Run Command"):
            pattern = re.compile(r"<bash>(.*)</bash>")

            if command == "exit":
                st.stop()  # Stop the Streamlit app
            else:
                messages.append({"role": "user", "content": command})
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo", messages=messages, stream=True
                )

                completion_text = ""
                for event in completion:
                    event_text = event.choices[0].delta.content
                    stempty = st.empty()
                    if event_text:
                        completion_text += event_text
                        stempty.write(event_text)

                for bash_command in re.findall(pattern, completion_text):
                    # Button to confirm command:
                    if st.button("Run Subommand"):
                        try:
                            cprocess = subprocess.run(
                                bash_command, shell=True, capture_output=True
                            )
                            st.write(
                                cprocess.stdout.decode("utf-8")
                            )  # Display output in the app
                            messages.append(
                                {
                                    "role": "user",
                                    "content": "Output of the last command was: "
                                    + cprocess.stdout.decode("utf-8"),
                                }
                            )
                        except subprocess.CalledProcessError as error:
                            st.write(error.output.decode("utf-8"))  # Display output in the app
                            st.session_state.messages.append(
                                {
                                    "role": "user",
                                    "content": "Error executing command: "
                                    + error.output.decode("utf-8"),
                                }
                            )
"""

# Run either web or main based on 'web' flag:
if __name__ == "__main__":
    import sys

    #if len(sys.argv) > 1 and sys.argv[1] == "web":
    #    web()
    #else:
    main()
