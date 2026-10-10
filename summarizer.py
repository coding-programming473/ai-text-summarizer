#!/usr/bin/env python3
"""
summarizer.py — AI Text Summarizer CLI

Summarize text files, URLs (via pasted text) or stdin using the Claude API.

Usage:
    python summarizer.py file report.txt --bullets
    python summarizer.py file notes.txt --style brief --max-words 100
    echo "long text..." | python summarizer.py stdin
    python summarizer.py file doc.txt --model claude-sonnet-4-5 --output summary.md

Requires: ANTHROPIC_API_KEY environment variable.
"""

import argparse
import os
import sys

try:
    import anthropic
except ImportError:
    print("Missing dependency: run `pip install -r requirements.txt` first.",
          file=sys.stderr)
    sys.exit(1)

DEFAULT_MODEL = "claude-sonnet-4-5"

STYLES = {
    "bullets": "Summarize the text as a concise bullet-point list. "
               "Keep each bullet to one line.",
    "brief": "Summarize the text in one short paragraph (3-5 sentences).",
    "detailed": "Write a structured summary with headings: Overview, "
                "Key Points, and Takeaways.",
    "tldr": "Give a one-line TL;DR, then up to 5 key points.",
}


def build_prompt(text: str, style: str, max_words: int | None) -> str:
    instruction = STYLES.get(style, STYLES["bullets"])
    limit = f" Keep the whole summary under {max_words} words." if max_words else ""
    return f"{instruction}{limit}\n\n--- TEXT TO SUMMARIZE ---\n{text}"


def summarize(text: str, style: str, max_words: int | None,
              model: str, max_tokens: int) -> str:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user",
                   "content": build_prompt(text, style, max_words)}],
    )
    return "\n".join(
        block.text for block in message.content
        if getattr(block, "type", "") == "text"
    )


def read_input(args) -> str:
    if args.command == "file":
        with open(args.path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    # stdin
    if sys.stdin.isatty():
        print("Paste/pipe text via stdin, or use the `file` subcommand.",
              file=sys.stderr)
        sys.exit(2)
    return sys.stdin.read()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize text using the Claude API.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_file = sub.add_parser("file", help="Summarize a text file.")
    p_file.add_argument("path", help="Path to the .txt/.md file.")

    sub.add_parser("stdin", help="Read text from stdin.")

    for p in (p_file,):
        p.add_argument("--style", default="bullets",
                       choices=list(STYLES),
                       help="Summary style (default: bullets).")
        p.add_argument("--max-words", type=int, default=None,
                       help="Rough max word count for the summary.")
        p.add_argument("--model", default=DEFAULT_MODEL,
                       help=f"Claude model (default: {DEFAULT_MODEL}).")
        p.add_argument("--max-tokens", type=int, default=1024)
        p.add_argument("--output", default=None,
                       help="Write summary to this file instead of stdout.")

    # stdin parser also gets the shared flags
    args = parser.parse_args(argv)
    if not hasattr(args, "style"):
        # stdin path: add defaults manually
        args.style = "bullets"
        args.max_words = None
        args.model = DEFAULT_MODEL
        args.max_tokens = 1024
        args.output = None

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: set the ANTHROPIC_API_KEY environment variable first.",
              file=sys.stderr)
        return 1

    text = read_input(args).strip()
    if not text:
        print("Error: no input text provided.", file=sys.stderr)
        return 1

    try:
        result = summarize(text, args.style, args.max_words,
                           args.model, args.max_tokens)
    except anthropic.AuthenticationError:
        print("Error: invalid API key. Check ANTHROPIC_API_KEY.",
              file=sys.stderr)
        return 1
    except anthropic.APIError as exc:
        print(f"API error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result + "\n")
        print(f"Summary written to {args.output}")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
