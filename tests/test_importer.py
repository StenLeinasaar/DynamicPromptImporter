import base64
import types
import sys
from unittest.mock import MagicMock

import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create a minimal stub for the requests module since the real package may not
# be installed in the test environment.
class DummySession:
    def __init__(self):
        self.headers = {}
    def get(self, url, timeout=None):
        return fake_get(url)

def fake_get(url, *args, **kwargs):
    response = MagicMock()
    response.raise_for_status = lambda: None
    if url.endswith("/branches/main"):
        response.json.return_value = {"commit": {"sha": "sha-main"}}
    elif url.endswith("/git/trees/sha-main?recursive=1"):
        response.json.return_value = {
            "tree": [
                {"path": "folder/example.md", "type": "blob", "sha": "sha-blob"},
                {"path": "another-file.md", "type": "blob", "sha": "sha-blob2"},
                {"path": "bad-encoding.md", "type": "blob", "sha": "sha-bad"},
            ]
        }
    elif url.endswith("/git/blobs/sha-blob"):
        content = base64.b64encode(b"Test prompt").decode()
        response.json.return_value = {"encoding": "base64", "content": content}
    elif url.endswith("/git/blobs/sha-blob2"):
        content = base64.b64encode(b"Another prompt").decode()
        response.json.return_value = {"encoding": "base64", "content": content}
    elif url.endswith("/git/blobs/sha-bad"):
        response.json.return_value = {"encoding": "utf-8", "content": "oops"}
    else:
        raise AssertionError(f"Unexpected URL: {url}")
    return response

# Register the stubbed requests module
sys.modules['requests'] = types.SimpleNamespace(Session=DummySession)

from dynamic_prompt_importer import DynamicPromptImporter


def test_prompt_fetching():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.folder.example
    assert text == "Test prompt"


def test_get_file_content():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.get_file_content("folder/example")
    assert text == "Test prompt"


def test_attribute_sanitization():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.another_file
    assert text == "Another prompt"


def test_dir_listing_and_reload():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    _ = importer.folder.example  # prime cache
    assert "folder" in dir(importer)
    assert "example" in dir(importer.folder)
    assert importer._file_cache
    importer.reload()
    assert not importer._file_cache


def test_missing_attribute():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(AttributeError):
        _ = importer.no_such_file


def test_get_file_content_missing():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(FileNotFoundError):
        importer.get_file_content("folder/not_there")


def test_bad_blob_encoding():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    with pytest.raises(RuntimeError):
        importer.get_file_content("bad-encoding")
