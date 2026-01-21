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

## Data Format

Each chapter is stored in a JSON file with the following structure:

```json
{
  "version": "WEB",
  "book": "Gn",
  "chapter": 1,
  "verses": [
    {
      "number": 1,
      "text": "In the beginning, God created the heavens and the earth."
    },
    ...
  ]
}
```

## Documentation

- [Legends and Abbreviations](docs/legends.md)

## Quality Assurance

We have a suite of integrity tests to ensure the data is complete and accurate. These tests verify:
- All 66 books of the Bible are present.
- Each book contains the correct number of chapters.
- Each chapter contains the correct number of verses.
- Data consistency across different versions.
- JSON structure validity.

To run the tests, use the following command:

```bash
python3 tests/test_bible_integrity.py
```
