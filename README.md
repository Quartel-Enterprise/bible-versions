# Bible Versions

A collection of Bible versions in JSON format, organized by version, book, and chapter.

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
