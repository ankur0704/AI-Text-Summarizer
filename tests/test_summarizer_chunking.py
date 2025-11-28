import pytest
from summarizer import chunk_text


def test_chunk_text_basic():
    text = "This is sentence one. This is sentence two. This is sentence three."
    chunks = chunk_text(text, approx_chars=25)
    # Expect multiple chunks because approx_chars small
    assert len(chunks) >= 2
    # each chunk should end with a period when possible
    for c in chunks[:-1]:
        assert c.endswith('.')


def test_chunk_text_empty():
    assert chunk_text("   ", approx_chars=1000) == []


def test_chunk_text_nonstring():
    with pytest.raises(TypeError):
        chunk_text(123, approx_chars=1000)
