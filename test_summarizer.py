import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from summarizer import fetch_url, summarize, save_output


def test_fetch_url_returns_text():
    fake_html = "<html><body><p>Hello world.</p></body></html>"
    mock_response = MagicMock()
    mock_response.text = fake_html
    mock_response.raise_for_status = MagicMock()
    with patch("summarizer.requests.get", return_value=mock_response):
        result = fetch_url("https://example.com")
    assert "Hello world" in result


def test_fetch_url_removes_script_tags():
    fake_html = "<html><body><script>bad code</script><p>Good text.</p></body></html>"
    mock_response = MagicMock()
    mock_response.text = fake_html
    mock_response.raise_for_status = MagicMock()
    with patch("summarizer.requests.get", return_value=mock_response):
        result = fetch_url("https://example.com")
    assert "bad code" not in result
    assert "Good text" in result


def test_summarize_returns_string():
    mock_choice = MagicMock()
    mock_choice.message.content = "This is a summary."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    with patch("summarizer.client.chat.completions.create", return_value=mock_response):
        result = summarize("Some long text here.", length="short")
    assert isinstance(result, str)
    assert len(result) > 0


def test_summarize_uses_correct_length():
    mock_choice = MagicMock()
    mock_choice.message.content = "Summary."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    with patch("summarizer.client.chat.completions.create", return_value=mock_response) as mock_call:
        summarize("Some text.", length="detailed")
        prompt = mock_call.call_args[1]["messages"][0]["content"]
        assert "bullet points" in prompt


def test_summarize_defaults_to_medium():
    mock_choice = MagicMock()
    mock_choice.message.content = "Medium summary."
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    with patch("summarizer.client.chat.completions.create", return_value=mock_response) as mock_call:
        summarize("Some text.")
        prompt = mock_call.call_args[1]["messages"][0]["content"]
        assert "paragraph" in prompt


def test_save_output_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    saved = save_output("Great summary.", source="test input")
    assert saved.exists()
    content = saved.read_text(encoding="utf-8")
    assert "Great summary." in content
    assert "test input" in content


def test_save_output_creates_summaries_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_output("A summary.", source="test")
    assert (tmp_path / "summaries").is_dir()
