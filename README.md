# AliaBot

A terminal-based AI chatbot powered by Google's Gemini AI. AliaBot acts as an intelligent terminal assistant that understands natural language and can either execute shell commands or provide conversational responses.

## Features

- 🤖 **Smart Command Interpretation**: Converts natural language to terminal commands
- 💬 **Conversational AI**: Ask questions and get intelligent responses
- 🎨 **Rich Terminal UI**: Beautiful panels, colors, and ASCII art
- ⚡ **Fast**: Powered by Google Gemini 1.5 Flash

## Setup

### Prerequisites
- Python 3.7+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AliaBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
```bash
cp .env.example .env
```
Then edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Usage

Run AliaBot:
```bash
python gemini.py
```

### Examples

- **Execute commands**: "list files", "show python version", "create a directory called test"
- **Ask questions**: "What is Python?", "How do I use git?"
- **Exit**: Type `exit` to quit

## Security

⚠️ **Important**: Never commit your `.env` file or expose your API key. The `.gitignore` file is configured to exclude `.env` from version control.
