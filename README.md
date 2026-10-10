# AI Text Summarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/powered_by-Claude-orange.svg)](https://www.anthropic.com)

A lightweight open-source CLI that summarizes long text in seconds using the
Claude API. Point it at a file or pipe text in — get clean bullet points, a
brief paragraph, or a structured report back.

## ✨ Features

- 📄 **Summarize files** — `.txt`, `.md`, transcripts, articles, notes
- ⌨️ **Pipe-friendly** — works with stdin in any shell pipeline
- 🎨 **4 styles** — `bullets`, `brief`, `detailed`, `tldr`
- 📏 **Length control** — optional `--max-words` cap
- 💾 **Save output** — write summaries straight to a file with `--output`

## 🚀 Quickstart

```bash
# 1. Clone
git clone https://github.com/coding-programming473/ai-text-summarizer.git
cd ai-text-summarizer

# 2. Install
pip install -r requirements.txt

# 3. Add your Claude API key (get one at https://console.anthropic.com)
export ANTHROPIC_API_KEY="sk-ant-..."        # Linux / macOS
# setx ANTHROPIC_API_KEY "sk-ant-..."        # Windows

# 4. Summarize something
python summarizer.py file examples/sample.txt --bullets
```

## 📖 Usage

```bash
# Bullet-point summary (default)
python summarizer.py file report.txt --bullets

# One short paragraph
python summarizer.py file report.txt --style brief

# Structured report: Overview / Key Points / Takeaways
python summarizer.py file report.txt --style detailed

# TL;DR + key points, capped at ~100 words, saved to a file
python summarizer.py file report.txt --style tldr --max-words 100 --output summary.md

# Pipe text from anywhere
cat notes.txt | python summarizer.py stdin
echo "Long pasted text..." | python summarizer.py stdin

# Use a different Claude model
python summarizer.py file report.txt --model claude-haiku-4-5
```

### All options

| Flag | Description | Default |
|---|---|---|
| `--style` | `bullets` \| `brief` \| `detailed` \| `tldr` | `bullets` |
| `--max-words` | Rough word cap for the summary | none |
| `--model` | Claude model to use | `claude-sonnet-4-5` |
| `--max-tokens` | Max output tokens | `1024` |
| `--output` | Write summary to file instead of stdout | none |

## 🧠 How it works

```
 input.txt ──▶ summarizer.py ──▶ Claude API ──▶ clean summary
                    │
                    └── style prompt + word cap
```

1. The CLI reads your text and wraps it in a style-specific prompt.
2. It calls the Claude Messages API (`client.messages.create`).
3. The summary prints to your terminal (or to `--output` file).

No frameworks, no servers — one file, one dependency (`anthropic` SDK).

## 🛠 Requirements

- Python 3.9+
- A Claude API key ([console.anthropic.com](https://console.anthropic.com))

## 🗺 Roadmap

- [ ] URL input (`summarizer.py url https://...`)
- [ ] PDF support
- [ ] Batch mode for whole folders
- [ ] Config file for default style/model

PRs welcome — see [CONTRIBUTING](#-contributing) below.

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/my-idea`)
3. Commit, push, open a Pull Request

Bug reports and feature ideas → open an **Issue**.

## 📜 License

MIT — see [LICENSE](LICENSE). Use it anywhere, just keep the notice.
