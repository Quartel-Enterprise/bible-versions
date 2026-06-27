import os


def count_chapters(version_path):
    """Counts the total number of chapter files in a version directory.

    A chapter is any ``[Chapter].json`` file inside a book directory. The
    version's ``metadata.json`` lives at the version root (not inside a book
    directory), so it is naturally excluded from the count.
    """
    total = 0
    for book in os.listdir(version_path):
        book_path = os.path.join(version_path, book)
        if not os.path.isdir(book_path):
            continue
        total += sum(
            1
            for entry in os.listdir(book_path)
            if entry.endswith(".json") and os.path.isfile(os.path.join(book_path, entry))
        )
    return total


if __name__ == "__main__":
    bible_root = os.path.join(os.getcwd(), "bible")
    versions = sorted(
        v for v in os.listdir(bible_root) if os.path.isdir(os.path.join(bible_root, v))
    )
    for version in versions:
        print(f"{version}: {count_chapters(os.path.join(bible_root, version))}")
