# Dynamic Prompt Importer

This repository exposes a `DynamicPromptImporter` class which lets you treat a
GitHub repository full of Markdown prompts as a Python object. Each Markdown
file becomes an attribute that returns the file contents.

## Installation

Install the package from PyPI:

```bash
pip install dynamic-prompt-importer
```

Or install the current repository for development:

```bash
pip install -e .
```

## Usage example

1. **Install the package** (and dependencies):

   ```bash
   pip install dynamic-prompt-importer
   ```

2. **Instantiate** the importer using your repository and token. Replace the repo
   name and token below with your own values.

   ```python
   from dynamic_prompt_importer import DynamicPromptImporter

   importer = DynamicPromptImporter(
       "owner/repo-with-prompts",
       token="ghp_yourGitHubToken",
       preload=True,
   )
   ```

3. **Access a prompt** by navigating through attributes that mirror the folder
   structure of the repository. For example, if the repo contains a file
   `greetings/welcome.md`, you can print it with:

   ```python
   print(importer.greetings.welcome)
   ```

   You should see the Markdown contents of `greetings/welcome.md` printed to the
   console.

4. **Fetch a file by path** using the ``get_file_content`` helper when you
   prefer to specify a file path directly:

   ```python
   text = importer.get_file_content("greetings/welcome")
   ```

## API overview

- `DynamicPromptImporter(repo, token=None, branch="main", preload=False)`
  creates an importer for the given GitHub repository.
- Attribute access mirrors the repository structure. For instance
  `importer.docs.setup` returns the contents of `docs/setup.md`.
- `get_file_content(path)` fetches a Markdown file by path when attribute access
  is inconvenient.
- `reload()` clears caches and fetches a fresh copy of the repository.


5. **Run the tests** to ensure everything is wired correctly:

   ```bash
   pytest
   ```

   The included unit test uses mocked HTTP responses to simulate GitHub and
   verifies that a prompt can be retrieved successfully.
