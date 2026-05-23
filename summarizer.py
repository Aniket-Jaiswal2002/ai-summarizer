import os
import argparse
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY not found. "
        "Create a .env file with: GROQ_API_KEY=your_key_here"
    )

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

LENGTH_INSTRUCTIONS = {
    "short":    "in 3-4 sentences",
    "medium":   "in one concise paragraph",
    "detailed": "in 3-5 bullet points covering the key ideas",
}


def fetch_url(url: str) -> str:
    """Fetch and extract readable text from a URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:8000]
    except requests.RequestException as e:
        raise SystemExit(f"Error fetching URL: {e}")


def summarize(text: str, length: str = "medium") -> str:
    """Send text to Groq and return a summary."""
    instruction = LENGTH_INSTRUCTIONS.get(length, LENGTH_INSTRUCTIONS["medium"])
    prompt = (
        f"Summarize the following text {instruction}. "
        f"Be clear and concise. Do not add commentary.\n\n"
        f"TEXT:\n{text}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()


def save_output(summary: str, source: str) -> Path:
    """Save the summary to a timestamped text file."""
    output_dir = Path("summaries")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"summary_{timestamp}.txt"
    filename.write_text(
        f"Source: {source}\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'=' * 50}\n\n"
        f"{summary}\n",
        encoding="utf-8",
    )
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Summarize any text or webpage using Groq AI (LLaMA 3).",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--url",  help="URL of a webpage to summarize")
    source_group.add_argument("--text", help="Text to summarize (wrap in quotes)")
    source_group.add_argument("--file", help="Path to a .txt file to summarize")

    parser.add_argument(
        "--length",
        choices=["short", "medium", "detailed"],
        default="medium",
        help=(
            "Summary length:\n"
            "  short    = 3-4 sentences\n"
            "  medium   = one paragraph (default)\n"
            "  detailed = 3-5 bullet points"
        ),
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the summary to a file in the summaries/ folder",
    )

    args = parser.parse_args()

    if args.url:
        print(f"Fetching: {args.url}")
        text = fetch_url(args.url)
        source = args.url
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise SystemExit(f"File not found: {args.file}")
        text = file_path.read_text(encoding="utf-8")
        source = args.file
    else:
        text = args.text
        source = "direct input"

    print(f"Summarizing ({args.length})...\n")
    summary = summarize(text, length=args.length)

    print("=" * 50)
    print(summary)
    print("=" * 50)

    if args.save:
        saved_path = save_output(summary, source)
        print(f"\nSaved to: {saved_path}")


if __name__ == "__main__":
    main()
