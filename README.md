# Bible Versions

A collection of Bible versions in JSON format, organized by version, book, and chapter.

This data is used in production for [Bible Planner](https://www.bibleplanner.app/).

## Supported Versions and Books

This repository contains various translations of the Bible. For a complete list of supported versions, their descriptions, and the abbreviations used for each book, please refer to the [Legends Documentation](docs/legends.md).

## Project Structure

- `bible/`: Contains the Bible data organized by version.
  - `[Version]/`: Directory for a specific Bible version (e.g., `ACF`, `WEB`).
    - `[Book]/`: Directory for a specific book (using abbreviations).
      - `[Chapter].json`: JSON file containing the verses for that chapter.
    - `metadata.json`: JSON file containing metadata about the version.

## Data Format

Each chapter is stored as a JSON file and each version carries a `metadata.json`
describing it, including a Semantic Version for the data. For the full
specification of the chapter and metadata structures and the versioning rules,
see the [Data Format Documentation](docs/data_format.md).

## Documentation

- [Data Format](docs/data_format.md)
- [Legends and Abbreviations](docs/legends.md)

## Quality Assurance

We have a suite of integrity tests to ensure the data is complete and accurate. These tests verify:
- All 66 books of the Bible are present.
- Each book contains the correct number of chapters.
- Each chapter contains the correct number of verses.
- Data consistency across different versions.
- JSON structure validity.
- Presence and validity of version metadata.

### Running Tests

We use a suite of integrity tests to ensure the data is complete and accurate. You can run all tests using the following command:

```bash
python3 -m unittest discover tests
```

Or run specific test files:

```bash
# Bible data integrity (structure, chapters, verses)
python3 tests/test_bible_integrity.py

# Version metadata validation
python3 tests/test_metadata_integrity.py
```
