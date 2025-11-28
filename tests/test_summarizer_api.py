import pytest
from types import SimpleNamespace

from summarizer import summarize_chunk, consolidate_and_summarize, SummarizationError


class DummyModel:
    def __init__(self, response_text="ok", raise_exc=False):
        self.response_text = response_text
        self.raise_exc = raise_exc

    def generate_content(self, prompt: str):
        if self.raise_exc:
            raise RuntimeError("api error")
        return SimpleNamespace(text=self.response_text)


def test_summarize_chunk_calls_model():
    model = DummyModel(response_text="chunk summary")
    out = summarize_chunk("some text", model, tone="Formal", sentences=2)
    assert out == "chunk summary"


def test_summarize_chunk_handles_error():
    model = DummyModel(raise_exc=True)
    with pytest.raises(SummarizationError):
        summarize_chunk("some text", model, tone="Formal", sentences=2)


def test_consolidate_and_summarize_success():
    model = DummyModel(response_text="final summary")
    out = consolidate_and_summarize(["a", "b"], model, tone="Casual", summary_length=3)
    assert out == "final summary"


def test_consolidate_and_summarize_error():
    model = DummyModel(raise_exc=True)
    with pytest.raises(SummarizationError):
        consolidate_and_summarize(["a"], model, tone="Casual", summary_length=1)
