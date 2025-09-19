
# AI Text Summarizer (Gemini + Streamlit)

A simple, user-friendly web app that uses Google Gemini to summarize long text. Built with Python and Streamlit, this project focuses on easy setup and a smooth user experience for summarizing articles, notes, and documents.

---

## Table of contents

- Overview
- Features
- How it works (workflow)
- Quickstart (local)
- Configuration
- Usage guide
- Troubleshooting & tips
- Development & contribution
- License

---

## Overview

This project provides a small web UI where users paste or upload text and ask Gemini to summarize it. For very long inputs the app supports chunked summarization: the text is split into smaller pieces and each piece is summarized, then those intermediate summaries are combined into a final concise summary. This improves reliability and responsiveness for large documents.

## Features

- Summarization powered by Google Gemini.
- Adjustable summary length (in sentences) and tone (Formal, Casual, Professional, Bullet Points).
- Chunked summarization with per-chunk progress feedback for long inputs.
- Quick mode (faster, higher-level summaries) for speed-sensitive use.
- Clean Streamlit UI with collapsible summary output.

## How it works (workflow)

1. User pastes or uploads text in the main input area.
2. User configures options in the sidebar (summary length, tone, chunking, quick mode).
3. When the user clicks "Summarize Text":
	 - If chunking is enabled and the text is long, the app splits the text into chunks (character-based with sentence-boundary preference).
	 - The app sends each chunk to the Gemini model to get a chunk summary and updates a progress bar.
	 - After all chunks are summarized, the app sends the combined chunk summaries to Gemini to produce a final consolidated summary in the requested tone and length.
4. The final summary is displayed in an expandable section for easy copying.

## Quickstart (local)

Prerequisites

- Python 3.8+
- Google Gemini API key (AI Studio / Google Generative Models)

1) Clone the repo

git clone https://github.com/YOUR_USERNAME/AI-Text-Summarizer.git
cd AI-Text-Summarizer

2) Create and activate a virtual environment

Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate
```

macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

3) Install dependencies

```bash
pip install -r requirements.txt
```

4) Add your API key

Create a `.env` file in the repository root with:

```
GOOGLE_API_KEY="AIza...YourSecretGoogleApiKey"
```

5) Run the app

```powershell
streamlit run app.py
```

Open the URL Streamlit prints in your browser (usually http://localhost:8501).

## Configuration

- Sidebar options
	- Summary Length: number of sentences (1–10).
	- Summary Tone: Formal, Casual, Professional, Bullet Points.
	- Enable chunked summarization: recommended for long inputs.
	- Approx. characters per chunk: controls chunk size (default 4000).
	- Quick mode: faster, less detailed summaries.

## Usage guide

- Paste or type text into the main input area.
- Optionally tweak sidebar settings.
- Click "Summarize Text" and wait for the progress bar and status messages.
- Expand "View Your Summary" to read or copy the output.

## Troubleshooting & tips

- API key errors: confirm your `GOOGLE_API_KEY` is set in `.env` and valid. Streamlit shows an error if the app cannot connect.
- Long documents: enable chunking (default) and increase chunk size carefully — larger chunks may cause longer per-call latency or API limits.
- Quick mode: use when you just want a fast gist instead of a detailed summary.
- If you see rate limits or timeouts from Gemini, reduce chunk size or summarize in multiple passes.

## Development notes

- Main files
	- `app.py` — Streamlit app and summarization flow.
	- `style.css` — UI styling.
	- `requirements.txt` — Python dependencies.

- Tests: None included by default. To add tests, mock `model.generate_content` and assert chunking + consolidation behavior.

## Contributing

Contributions are welcome. A simple workflow:

1. Fork the repo and create a branch for your change.
2. Make your changes and add tests where appropriate.
3. Open a pull request describing your change.

## License

This project is provided as-is. Add your preferred license file if you plan to publish it publicly.

---

If you want, I can also:
- Add a compact `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
- Generate a short `docs/` page or GitHub Pages site with screenshots.
- Create a small example long-text file to demo chunking behavior locally.

---

Happy summarizing! ✍️


## Performance tips for long documents

- The app supports chunked summarization: long inputs are split into smaller pieces which are summarized individually and then combined. This reduces the chance of timeouts and gives faster visible progress when working with very large texts.
- Enable "Quick mode" in the sidebar for a faster, higher-level summary when you only need the gist. Quick mode trades some detail for speed.
- If the text is extremely long (many MBs), consider pasting a shorter excerpt or running multiple smaller summarizations.
