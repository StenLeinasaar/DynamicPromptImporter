# Tests for Dynamic Prompt Importer

This suite exercises the behaviour of `DynamicPromptImporter` using mocked
HTTP responses. No real network access is required.

## Running the tests

Run the tests with increased verbosity so that each step is shown and print
statements are displayed:

```bash
pytest -vv -s
```

After the run a JSON summary of the results is written to `test_report.json`
within the repository root.

## What each test covers

- **`test_prompt_fetching`** – verifies that prompts can be fetched via
  attribute access.
- **`test_get_file_content`** – checks explicit retrieval with
  `get_file_content`.
- **`test_attribute_sanitization`** – ensures file names are converted into
  valid Python identifiers.
- **`test_dir_listing_and_reload`** – tests directory introspection with `dir()`
  and cache clearing via `reload()`.
- **`test_missing_attribute`** – confirms that accessing a missing attribute
  raises `AttributeError`.
- **`test_get_file_content_missing`** – verifies that requesting a non-existent
  file raises `FileNotFoundError`.
- **`test_bad_blob_encoding`** – ensures an error is raised when a blob has an
  unexpected encoding.
