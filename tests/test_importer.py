import base64
import types
import sys
from unittest.mock import patch, MagicMock
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

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
                {"path": "folder/example.md", "type": "blob", "sha": "sha-blob"}
            ]
        }
    elif url.endswith("/git/blobs/sha-blob"):
        content = base64.b64encode(b"Test prompt").decode()
        response.json.return_value = {"encoding": "base64", "content": content}
    else:
        raise AssertionError(f"Unexpected URL: {url}")
    return response

# Register the stubbed requests module
sys.modules['requests'] = types.SimpleNamespace(Session=DummySession)

from init import DynamicPromptImporter


def test_prompt_fetching():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.folder.example
    assert text == "Test prompt"


def test_get_file_content():
    importer = DynamicPromptImporter("owner/repo", preload=True)
    text = importer.get_file_content("folder/example")
    assert text == "Test prompt"
