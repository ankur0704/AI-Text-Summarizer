from types import SimpleNamespace


class SummarizationError(Exception):
    """Raised when summarization via model fails."""


def chunk_text(text: str, approx_chars: int = 4000):
    """
    Split `text` into chunks of approximately `approx_chars` characters.
    Prefer to split on sentence boundaries (periods) when possible.

    Returns a list of non-empty chunk strings. For empty input returns [].
    Raises TypeError for non-string input.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + approx_chars, length)
        if end < length:
            # try to break on a period within the window
            next_period = text.rfind('.', start, end)
            if next_period > start:
                end = next_period + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def _build_chunk_prompt(chunk: str, tone: str, sentences: int, bullet: bool = False, quick: bool = False) -> str:
    if bullet:
        return f"""
You are an expert summarizer. Summarize the following text into {sentences} concise bullet points that capture the key ideas.
Text:
---
{chunk}
---
"""
    length_desc = "a brief" if quick else "a detailed"
    return f"""
You are an expert summarizer. Provide {length_desc} summary in a {tone} tone.
The summary should be {sentences} sentences long and capture the main points.
Text:
---
{chunk}
---
"""


def summarize_chunk(chunk: str, model, tone: str, sentences: int, bullet: bool = False, quick: bool = False) -> str:
    """Summarize a single chunk by calling `model.generate_content(prompt)`.

    `model` must have a `generate_content(prompt)` method that returns an object
    with a `text` attribute (compatible with the code used in the app).
    Raises `SummarizationError` on underlying errors.
    """
    prompt = _build_chunk_prompt(chunk, tone, sentences, bullet=bullet, quick=quick)
    try:
        resp = model.generate_content(prompt)
        # model.generate_content is expected to return an object with `.text`
        return getattr(resp, "text", str(resp))
    except Exception as e:
        raise SummarizationError(f"summarization failed: {str(e)}") from e


def consolidate_and_summarize(intermediate_summaries: list, model, tone: str, summary_length: int) -> str:
    """Combine intermediate summaries and ask the model for a final consolidated summary."""
    combined_text = "\n\n".join(intermediate_summaries)
    prompt = f"""
You are an expert summarizer. Combine the following chunk summaries into one coherent summary.
The final summary should be in a {tone} tone and be exactly {summary_length} sentences long.
Chunk summaries:
---
{combined_text}
---
"""
    try:
        resp = model.generate_content(prompt)
        return getattr(resp, "text", str(resp))
    except Exception as e:
        raise SummarizationError(f"final consolidation failed: {str(e)}") from e
