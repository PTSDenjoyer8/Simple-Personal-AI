Athena AI Assistant

Overview

Athena is a local AI assistant powered by Mistral-7B, designed to interact with users, remember past conversations, and execute system commands such as opening and closing applications. It integrates natural language processing (NLP), database memory storage, and system automation for an interactive user experience.

Features

Conversational AI: Uses Mistral-7B via Ollama to generate intelligent responses.

Memory Retention: Stores user interactions in a SQLite database to maintain context.

Application Control: Can open and close applications via system commands.

Automated Task Execution: Recognizes user commands and executes actions accordingly.

Requirements

Make sure you have the following installed:

Python 3.x

Ollama

Required Python libraries:

pip install ollama pyautogui psutil

Setup & Usage

Clone the repository or download the script.

Run the script:

python athena.py

Interact with Athena using text input.

Use commands like:

Open an application: open chrome

Close an application: close notepad

Ask questions or chat naturally.

Stop Athena: Type opreste te.

How It Works

User inputs are processed and checked for commands (open, close).

If it's a general query, the AI generates a response using Mistral-7B.

The conversation is stored in a SQLite database to maintain context.

If the user is inactive, Athena can initiate conversations.

Future Improvements

Voice recognition and response integration.

Extended command set for more system interactions.

Customizable AI behavior and user preferences.

License

This project is open-source and free to use. Modify and improve as needed!
