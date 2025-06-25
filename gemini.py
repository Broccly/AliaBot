import shutil
import subprocess
import os
import time
import google.generativeai as genai
from rich.console import Console
from rich.spinner import Spinner
from rich.panel import Panel
from threading import Thread
import pyfiglet

console = Console()
genai.configure(api_key="AIzaSyCV4-bOUYdG3qulbCfsJ5SbSv_DPsmj10E")
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

ALIA_BOT_BANNER = pyfiglet.figlet_format("AliaBot", font="slant")
ALIA_BOT_BANNER = f"[bold italic]\n{ALIA_BOT_BANNER}[/bold italic]"

MAX_WIDTH = 90  # Wider box

def get_terminal_width():
    return shutil.get_terminal_size().columns

def print_centered_panel(content, title="", style=""):
    panel = Panel(content, title=title, width=MAX_WIDTH, border_style=style)
    console.print(panel, justify="center")

def print_input_box(prompt_text):
    # Prepare content for input box - just prompt text in panel
    content = f"[bold yellow]{prompt_text}[/bold yellow]"
    print_centered_panel(content, title="You", style="yellow")

def get_padded_prompt(prompt_text):
    term_width = get_terminal_width()
    # panel has borders so input area width = MAX_WIDTH - 4 (2 chars left + 2 chars right border)
    input_area_width = MAX_WIDTH - 4
    # Calculate padding so user input starts right after prompt_text inside panel left border
    padding = (term_width - MAX_WIDTH) // 2 + len(prompt_text) + 2  # 2 for left border + space
    return " " * padding

class SpinnerDisplay:
    def __init__(self, text="AliaBot is thinking..."):
        self.text = text
        self.running = False
        self.thread = Thread(target=self._run)

    def _run(self):
        with console.status(self.text, spinner="dots", spinner_style="green"):
            while self.running:
                time.sleep(0.1)

    def start(self):
        self.running = True
        console.clear()
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()


def run_terminal_command(command):
    try:
        if command.startswith("cd "):
            path = command[3:].strip()
            os.chdir(path)
            return f"📁 Changed directory to `{os.getcwd()}`"
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"❌ Error: {e}"

def interpret_and_act(user_input):
    prompt = f"""
You are a smart assistant that decides what to do with user input.

If it's a shell instruction (e.g., 'list files', 'show python version'), convert it into a Linux command:
Return: COMMAND: <command>

If it's a question or general message, respond in natural language:
Return: REPLY: <reply>

User: {user_input}
"""

    spinner = SpinnerDisplay()
    spinner.start()
    decision = model.generate_content(prompt).text.strip()
    spinner.stop()

    if decision.startswith("COMMAND:"):
        command = decision[len("COMMAND:"):].strip()
        output = run_terminal_command(command)
        print_centered_panel(output, title="🤖 AliaBot (terminal output)", style="green")
    elif decision.startswith("REPLY:"):
        reply = decision[len("REPLY:"):].strip()
        print_centered_panel(reply, title="🤖 AliaBot", style="cyan")
    else:
        print_centered_panel("❓ I didn't understand that.", title="🤖 AliaBot", style="red")

if __name__ == "__main__":
    console.print(ALIA_BOT_BANNER, justify="center")
    print_centered_panel("[bold magenta]🧠 AliaBot Terminal Assistant\n(type 'exit' to quit)[/bold magenta]", style="magenta")

while True:
    # Print input prompt box
    print_input_box("You >")

    # Calculate where user should type based on padding
    padded_prompt = get_padded_prompt("You > ")

    # Collect user input
    user_input = input(padded_prompt).strip()

    if user_input.lower() == "exit":
        print_centered_panel("[bold magenta]👋 Goodbye![/bold magenta]", style="magenta")
        break

    # Now show the user's input as a styled box
    print_centered_panel(f"[bold yellow]{user_input}[/bold yellow]", title="You", style="yellow")

    # Process input
    interpret_and_act(user_input)

