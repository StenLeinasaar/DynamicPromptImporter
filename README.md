# Dynamic Prompt Importer

Dynamic Prompt Importer turns a GitHub repository full of Markdown files into a Python object.  Each prompt can be accessed as an attribute which lazily downloads the file on first use.  The package was born out of laziness—I wanted a quick way to pull prompts from my private prompt repo without manually copying files around.

## Installation

Install from PyPI:

```bash
pip install dynamic-prompt-importer
```

For development install the repo directly:

```bash
pip install -e .
```

## Usage

```python
from dynamic_prompt_importer import DynamicPromptImporter

importer = DynamicPromptImporter(
    "owner/my-prompt-repo",  # GitHub "owner/repo" spec
    token="ghp_yourGitHubToken",  # needed for private repos
    preload=True,  # fetch the repo tree immediately
)

print(importer.folder.welcome)  # prints contents of folder/welcome.md
```

You may also fetch a file explicitly using `get_file_content()`:

```python
text = importer.get_file_content("folder/welcome")
```

## API

* `DynamicPromptImporter(repo, token=None, branch="main", preload=False)` - create an importer for a GitHub repo.
* Attribute access mirrors the repository structure: `importer.docs.setup` returns the text of `docs/setup.md`.
* `get_file_content(path)` - retrieve a file via an explicit path.
* `reload()` - clear caches and re-fetch the repository tree.

## Why?

Maintaining prompts in a separate repository keeps them version controlled and editable without redeploying application code.  This utility lets you pull those prompts into Python on demand so that your code always uses the latest version.

## Running Tests

```bash
pytest -vv -s
```

The tests use mocked HTTP responses so no network access is required. A JSON
summary will be written to `test_report.json` after the run.  See
`tests/README.md` for more details on what each test covers.
