# AI Text Summarizer

A Python command-line tool that summarizes any text, webpage, or file using Groq AI (LLaMA 3) — completely free with no credit card needed.

## Features

- Summarize **raw text**, **any URL**, or a **.txt file**
- Three output lengths: `short`, `medium`, `detailed`
- `--save` flag to store summaries in timestamped files
- Secure API key handling with `.env`
- Fully tested with mocked API calls

## Demo

```
$ python summarizer.py --url https://en.wikipedia.org/wiki/Artificial_intelligence --length short

Fetching: https://en.wikipedia.org/wiki/Artificial_intelligence
Summarizing (short)...

==================================================
Artificial intelligence is the simulation of human intelligence by machines.
It encompasses tasks like learning, reasoning, and problem-solving. Modern AI
powers applications ranging from voice assistants to self-driving cars.
==================================================
```

## Installation

```bash
# Clone the repo
git clone https://github.com/Aniket-Jaiswal2002/ai-summarizer.git
cd ai-summarizer

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Open .env and paste your Groq API key
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

## Usage

```bash
# Summarize a webpage
python summarizer.py --url https://example.com

# Summarize direct text
python summarizer.py --text "Your long text goes here..."

# Summarize a text file
python summarizer.py --file article.txt

# Choose summary length
python summarizer.py --url https://example.com --length detailed

# Save the summary to a file
python summarizer.py --url https://example.com --save
```

## Running tests

```bash
pytest test_summarizer.py -v
```

## Tech stack

- Python 3.10+
- [Groq API](https://console.groq.com) with LLaMA 3 model
- `requests` + `beautifulsoup4` for URL fetching
- `python-dotenv` for secure API key handling
- `pytest` + `unittest.mock` for testing
