# Data Format

This document specifies how the Bible data in this repository is structured and
how each version is versioned.

## Directory Layout

```
bible/
└── [Version]/            # A specific Bible version (e.g. ACF, WEB)
    ├── metadata.json     # Metadata about the version
    └── [Book]/           # A specific book, using its abbreviation
        └── [Chapter].json  # The verses for that chapter
```

See the [Legends Documentation](legends.md) for the list of versions and the
book abbreviations used in directory names.

## Chapter Files

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
    }
  ]
}
```

| Field     | Type   | Description                                            |
|:----------|:-------|:------------------------------------------------------|
| `version` | string | The version `id` this chapter belongs to.             |
| `book`    | string | The book abbreviation (see the Legends Documentation). |
| `chapter` | number | The chapter number.                                   |
| `verses`  | array  | The list of verses in the chapter.                    |

Each entry in `verses` has:

| Field    | Type   | Description          |
|:---------|:-------|:---------------------|
| `number` | number | The verse number.    |
| `text`   | string | The verse text.      |

## Version Metadata

Each version directory contains a `metadata.json` file with general information
about the version:

```json
{
  "id": "ACF",
  "name": "Almeida Corrigida Fiel",
  "version": "1.1.0",
  "language": "pt",
  "country": "br",
  "chapters": 1189,
  "year": {
    "begin": 1994,
    "end": 2011
  }
}
```

| Field      | Type   | Description                                                        |
|:-----------|:-------|:------------------------------------------------------------------|
| `id`       | string | The version identifier. Matches the version directory name.       |
| `name`     | string | The full, human-readable name of the version.                     |
| `version`  | string | The data version of this translation (see [Versioning](#versioning)). |
| `language` | string | ISO 639-1 language code (e.g. `pt`, `en`).                         |
| `country`  | string | ISO 3166-1 alpha-2 country code, or `-` when not country-specific. |
| `chapters` | number | The total number of chapters across all books in this version.    |
| `year`     | object | The publication range of the underlying translation.              |

The `year` object has:

| Field   | Type   | Description                          |
|:--------|:-------|:-------------------------------------|
| `begin` | number | The year the translation began.      |
| `end`   | number | The year the translation was completed. |

## Versioning

Each version is independently versioned through the `version` field of its
`metadata.json`, following [Semantic Versioning](https://semver.org/)
(`MAJOR.MINOR.PATCH`). The number describes **the data in this repository for
that translation**, not the publication history of the translation itself (that
is what `year` is for).

Consumers can compare the stored `version` against the latest one to decide
whether a cached copy of a translation is still up to date.

| Part      | Increment when…                                                                                   | Examples                                                          |
|:----------|:--------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|
| **MAJOR** | A change breaks consumers: the JSON schema changes, a version `id` changes, or a book/chapter is removed. | Renaming the `text` field; removing a book.                       |
| **MINOR** | Content is added without breaking consumers: a missing book, chapter, or verse is added, or a new metadata field is introduced. | Adding a missing verse; adding a chapter.                         |
| **PATCH** | An existing verse's text is corrected without changing the structure.                             | Fixing a typo, accent, or punctuation.                            |

### Rules

- Every translation starts at `1.0.0`.
- **Any** change to the content of a translation must bump its `version`. A
  silent content change would leave consumers serving stale, cached data.
- The version is scoped **per translation**: changing `ACF` does not affect the
  `version` of `WEB`.

### Consumer guidance

- Different **MAJOR** ⇒ the data may not be readable by the current code; do not
  auto-update, require a client update.
- Different **MINOR** or **PATCH** ⇒ revalidate and refresh the cached
  translation.
