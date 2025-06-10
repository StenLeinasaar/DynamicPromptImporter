# Dynamic Prompt Importer

This repository exposes a `DynamicPromptImporter` class which lets you treat a
GitHub repository full of Markdown prompts as a Python object. Each Markdown
file becomes an attribute that returns the file contents.

## Verifying prompt import

1. **Install dependencies** (only `requests` is required):

   ```bash
   pip install requests
   ```

2. **Instantiate** the importer using your repository and token. Replace the repo
   name and token below with your own values.

   ```python
   from init import DynamicPromptImporter

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

5. **Run the tests** to ensure everything is wired correctly:

   ```bash
   pytest
   ```

   The included unit test uses mocked HTTP responses to simulate GitHub and
   verifies that a prompt can be retrieved successfully.
