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

- **Summarization powered by Google Gemini** (gemini-2.0-flash model).
- **Preset templates** — Quick Summary, Executive Brief, Detailed Report, Key Points for one-click configuration.
- **Adjustable summary options** — Control length (1–10 sentences) and tone (Formal, Casual, Professional, Bullet Points).
- **Chunked summarization** with per-chunk progress feedback for long inputs (character-based chunks with sentence-boundary preference).
- **Quick mode** — Faster, higher-level summaries for speed-sensitive use.
- **Summary statistics** — Display input word count, output word count, reduction percentage, and efficiency ratio.
- **Character counter** — Live word count below the input area.
- **Copy-to-clipboard** button with toast confirmation for easy summary sharing.
- **Welcome screen** — Helpful tips, feature list, and sample text loader when starting.
- **Smooth animations** — CSS transitions and keyframe animations (fade-in, slide-in, button hover effects).
- **Dark and light mode support** — Professional UI theming with glassmorphic design.
- **Comprehensive test suite** — 7 unit tests covering chunking, API mocking, and error handling.

## How it works (workflow)

1. User pastes or uploads text in the main input area.
2. User configures options in the sidebar (summary length, tone, chunking, quick mode).
3. When the user clicks "Summarize Text":
	 - If chunking is enabled and the text is long, the app splits the text into chunks (character-based with sentence-boundary preference).
	 - The app sends each chunk to the Gemini model to get a chunk summary and updates a progress bar.
	 - After all chunks are summarized, the app sends the combined chunk summaries to Gemini to produce a final consolidated summary in the requested tone and length.
4. The final summary is displayed in an expandable section for easy copying.

## Quickstart (local)

**Prerequisites**

- Python 3.8+
- Google Gemini API key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

**Step 1: Clone the repo**

```powershell
git clone https://github.com/ankur0704/AI-Text-Summarizer.git
cd AI-Text-Summarizer
```

**Step 2: Create and activate a virtual environment**

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Add your API key**

Create a `.env` file in the repository root:

```
GOOGLE_API_KEY="AIza...YourSecretGoogleApiKey"
```

**Step 5: Run the app**

```bash
streamlit run app.py
```

Open the URL in your browser (usually http://localhost:8501).

## Configuration

- **Preset templates** (quick-select in sidebar)
	- Quick Summary: 2 sentences, Casual tone
	- Executive Brief: 3 sentences, Formal tone
	- Detailed Report: 5 sentences, Professional tone
	- Key Points: Bullet-point format
- **Sidebar options**
	- Summary Length: number of sentences (1–10).
	- Summary Tone: Formal, Casual, Professional, Bullet Points.
	- Enable chunked summarization: recommended for long inputs.
	- Approx. characters per chunk: controls chunk size (default 4000).
	- Quick mode: faster, less detailed summaries.
- **Input area features**
	- Character counter displays live word count.
	- Clear button resets input instantly.
	- Sample text loader in welcome screen for testing.

## Testing

A comprehensive test suite is included to validate text-processing logic, API mocking, input validation, and error handling.

**Quick start:**
```bash
pytest -q
```

Expected output: `7 passed in 0.02s`

**For detailed testing instructions:** See [`TESTING.md`](TESTING.md)

The test suite includes:
- Unit tests for `chunk_text()` (chunking edge cases, invalid inputs)
- API mocking tests for `summarize_chunk()` and `consolidate_and_summarize()`
- Error-handling tests that verify proper exception wrapping and logging

## Usage guide

1. **Open the app** — Run `streamlit run app.py` and open the browser link.
2. **Load sample text** (optional) — Click "Load Sample Text" in the welcome screen to test.
3. **Paste or type text** — Paste your article, notes, or document in the input area.
4. **Choose a preset** (optional) — Select a preset template (Quick Summary, Executive Brief, etc.) to auto-configure settings.
5. **Customize settings** (optional) — Adjust summary length, tone, chunk size in the sidebar.
6. **Click "Summarize Text"** — The app processes the text with a progress bar.
7. **View results** — Expand "View Your Summary" to read the output.
8. **Copy summary** — Click "Copy to Clipboard" for easy sharing.
9. **View statistics** — See summary statistics (input/output words, reduction %, efficiency) below the summary.

## Troubleshooting & tips

| Issue | Solution |
|-------|----------|
| **API key errors** | Confirm your `GOOGLE_API_KEY` is set in `.env` and valid. Restart Streamlit if you just added it. |
| **"Summarization failed" error** | Check your API key has access to Gemini API. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to verify. |
| **Long documents timeout** | Enable chunking (default) and try reducing chunk size. For very large texts (>100KB), test with a smaller excerpt first. |
| **Slow performance** | Enable "Quick mode" in the sidebar for faster, less detailed summaries. Larger chunk sizes also speed up processing. |
| **Rate limit errors** | Reduce chunk size to send fewer/shorter API requests. Wait a few seconds and retry. Consider batching requests. |
| **Copy button not working** | Ensure JavaScript is enabled in your browser. Try refreshing the page. |

**Performance tips for long documents**

- The app supports **chunked summarization** by default: long inputs are split into smaller pieces, summarized individually, then combined. This prevents timeouts and gives visible progress.
- Enable **"Quick mode"** in the sidebar for faster, higher-level summaries when you only need the gist.
- Use **preset templates** to quickly apply optimized settings for your use case (Executive Brief for business, Detailed Report for research, etc.).
- For extremely long texts (>5MB), consider pasting shorter excerpts or running multiple summarizations sequentially.

## Development notes

- **Main files**
	- `app.py` — Streamlit web interface with UI components and chunked summarization flow.
	- `summarizer.py` — Testable business logic module (chunking, summarization, error handling).
	- `style.css` — Modern UI styling with animations, light/dark mode support, glassmorphic design.
	- `requirements.txt` — Python dependencies.

- **Tests**
	- `tests/test_summarizer_chunking.py` — 3 tests validating text chunking behavior (edge cases, invalid inputs).
	- `tests/test_summarizer_api.py` — 4 tests for API mocking, error handling, and consolidation.
	- `tests/conftest.py` — pytest configuration for proper module imports.
	- `TESTING.md` — Comprehensive testing guide with setup, running tests, and extension instructions.

- **Architecture**
	- Modular design: business logic in `summarizer.py`, UI in `app.py` for clean separation of concerns.
	- Mock-based testing: uses `DummyModel` to simulate Gemini API without external calls (fast, reliable, cost-effective).
	- Error handling: custom `SummarizationError` exception with detailed error messages for debugging.

## Contributing

Contributions are welcome. A simple workflow:

1. Fork the repo and create a branch for your change.
2. Make your changes and add tests where appropriate (see [`TESTING.md`](TESTING.md)).
3. Run `pytest -q` to ensure tests pass.
4. Open a pull request describing your change.

## Future enhancements

Potential improvements for future releases:

1. **Token-based chunking** — Replace character-based chunks with token counts using a tokenizer (e.g., tiktoken). Provides accurate control over model input sizes.
2. **Parallel chunk processing** — Summarize multiple chunks concurrently with rate-limit backoff to reduce wall-clock time.
3. **Save / resume sessions** — Allow users to save intermediate summaries and resume long workflows.
4. **Estimated time-to-completion (ETA)** — Display predicted finish time based on chunk count and average processing speed.
5. **File upload support** — Accept PDF, DOCX, TXT files in addition to text input.
6. **Export options** — Download summaries as PDF, Markdown, or plain text.
7. **Multi-language support** — Detect and summarize text in languages other than English.
8. **User analytics** — Track summarization metrics (avg. compression ratio, processing time, etc.) for portfolio projects.

## License

This project is provided as-is. Add your preferred license file if you plan to publish it publicly.

---

**Happy summarizing!** ✍️ If you have questions or suggestions, feel free to open an issue or discussion on GitHub.
