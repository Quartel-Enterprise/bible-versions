import os
import json
import unittest
try:
    from tests.bible_metadata import STANDARD_VERSE_COUNTS
except ImportError:
    from bible_metadata import STANDARD_VERSE_COUNTS

# Expected chapter counts for a standard Protestant Bible (66 books)
EXPECTED_CHAPTERS = {
    "Gn": 50, "Ex": 40, "Lv": 27, "Nm": 36, "Dt": 34, "Js": 24, "Jz": 21, "Rt": 4,
    "1Sm": 31, "2Sm": 24, "1Rs": 22, "2Rs": 25, "1Cr": 29, "2Cr": 36, "Ed": 10,
    "Ne": 13, "Et": 10, "Jo": 42, "Sl": 150, "Pv": 31, "Ec": 12, "Ct": 8,
    "Is": 66, "Jr": 52, "Lm": 5, "Ez": 48, "Dn": 12, "Os": 14, "Jl": 3, "Am": 9,
    "Ob": 1, "Jn": 4, "Mq": 7, "Na": 3, "Hc": 3, "Sf": 3, "Ag": 2, "Zc": 14, "Ml": 4,
    "Mt": 28, "Mc": 16, "Lc": 24, "Jh": 21, "At": 28, "Rm": 16, "1Co": 16, "2Co": 13,
    "Gl": 6, "Ef": 6, "Fp": 4, "Cl": 4, "1Ts": 5, "2Ts": 3, "1Tm": 6, "2Tm": 4,
    "Tt": 3, "Fm": 1, "Hb": 13, "Tg": 5, "1Pe": 5, "2Pe": 3, "1Jo": 5, "2Jo": 1,
    "3Jo": 1, "Jd": 1, "Ap": 22
}

BOOK_NAMES = {
    "Gn": "Genesis", "Ex": "Exodus", "Lv": "Leviticus", "Nm": "Numbers",
    "Dt": "Deuteronomy", "Js": "Joshua", "Jz": "Judges", "Rt": "Ruth",
    "1Sm": "1 Samuel", "2Sm": "2 Samuel", "1Rs": "1 Kings", "2Rs": "2 Kings",
    "1Cr": "1 Chronicles", "2Cr": "2 Chronicles", "Ed": "Ezra", "Ne": "Nehemiah",
    "Et": "Esther", "Jo": "Job", "Sl": "Psalms", "Pv": "Proverbs",
    "Ec": "Ecclesiastes", "Ct": "Song of Solomon", "Is": "Isaiah", "Jr": "Jeremiah",
    "Lm": "Lamentations", "Ez": "Ezekiel", "Dn": "Daniel", "Os": "Hosea",
    "Jl": "Joel", "Am": "Amos", "Ob": "Obadiah", "Jn": "Jonah",
    "Mq": "Micah", "Na": "Nahum", "Hc": "Habakkuk", "Sf": "Zephaniah",
    "Ag": "Haggai", "Zc": "Zechariah", "Ml": "Malachi", "Mt": "Matthew",
    "Mc": "Mark", "Lc": "Luke", "Jh": "John", "At": "Acts",
    "Rm": "Romans", "1Co": "1 Corinthians", "2Co": "2 Corinthians", "Gl": "Galatians",
    "Ef": "Ephesians", "Fp": "Philippians", "Cl": "Colossians", "1Ts": "1 Thessalonians",
    "2Ts": "2 Thessalonians", "1Tm": "1 Timothy", "2Tm": "2 Timothy", "Tt": "Titus",
    "Fm": "Philemon", "Hb": "Hebrews", "Tg": "James", "1Pe": "1 Peter",
    "2Pe": "2 Peter", "1Jo": "1 John", "2Jo": "2 John", "3Jo": "3 John",
    "Jd": "Jude", "Ap": "Revelation"
}

# Reference Verse Counts Sample
REFERENCE_VERSES = {
    "Gn": {1: 31, 50: 26},
    "Ex": {1: 22, 40: 38},
    "Sl": {1: 6, 119: 176, 150: 6},
    "Mt": {1: 25, 28: 20},
    "Ap": {1: 20, 22: 21}
}

BIBLE_ROOT = os.path.join(os.getcwd(), "bible")


def get_versions():
    if not os.path.exists(BIBLE_ROOT):
        return []
    return [v for v in os.listdir(BIBLE_ROOT) if os.path.isdir(os.path.join(BIBLE_ROOT, v))]


class TestBibleIntegrity(unittest.TestCase):

    def test_all_versions_structure(self):
        versions = get_versions()
        self.assertGreater(len(versions), 0, "No Bible versions found in bible/ directory")
        
        for version in versions:
            with self.subTest(version=version):
                version_path = os.path.join(BIBLE_ROOT, version)
                existing_books = [b for b in os.listdir(version_path) if os.path.isdir(os.path.join(version_path, b))]
                
                # Check 66 books
                with self.subTest(check="missing_books"):
                    missing = [b for b in EXPECTED_CHAPTERS if b not in existing_books]
                    if missing:
                        missing_with_names = [f"{b} ({BOOK_NAMES.get(b, 'Unknown')})" for b in missing]
                        # We don't assert 66 here yet to allow checking other books
                        print(f"[{version}] Missing books: {missing_with_names}")

                # Check chapter counts
                for book, expected_count in EXPECTED_CHAPTERS.items():
                    with self.subTest(check="chapter_count", book=book):
                        book_path = os.path.join(version_path, book)
                        missing_chapters = []
                        for i in range(1, expected_count + 1):
                            if not os.path.exists(os.path.join(book_path, f"{i}.json")):
                                missing_chapters.append(i)
                        
                        book_name = BOOK_NAMES.get(book, "Unknown")
                        self.assertEqual(len(missing_chapters), 0, 
                                         f"{version} - {book} ({book_name}): missing chapters: {missing_chapters}")

                # Check verse counts sample
                v_errors = []
                for book, chapters in REFERENCE_VERSES.items():
                    if book not in existing_books: continue
                    for chapter, expected_verses in chapters.items():
                        file_path = os.path.join(version_path, book, f"{chapter}.json")
                        if not os.path.exists(file_path): continue
                        
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            actual_verses = len(data.get("verses", []))
                            if actual_verses != expected_verses:
                                book_name = BOOK_NAMES.get(book, "Unknown")
                                v_errors.append(f"{book} ({book_name}) {chapter}: expected {expected_verses}, found {actual_verses}")
                if v_errors:
                    self.fail(f"Version {version} verse count mismatches:\n" + "\n".join(v_errors))

    def test_cross_version_consistency(self):
        versions = get_versions()
        if len(versions) < 2:
            return
            
        v1 = versions[0]
        v1_path = os.path.join(BIBLE_ROOT, v1)
        errors = []
        
        for book in EXPECTED_CHAPTERS:
            b1_path = os.path.join(v1_path, book)
            if not os.path.exists(b1_path): continue
            
            for ch_file in sorted(os.listdir(b1_path)):
                if not ch_file.endswith(".json"): continue
                
                # Get v1 count
                try:
                    with open(os.path.join(b1_path, ch_file), "r") as f:
                        v1_data = json.load(f)
                        v1_cnt = len(v1_data.get("verses", []))
                except: continue
                
                for vn in versions[1:]:
                    vn_file = os.path.join(BIBLE_ROOT, vn, book, ch_file)
                    if os.path.exists(vn_file):
                        try:
                            with open(vn_file, "r") as f:
                                vn_data = json.load(f)
                                vn_cnt = len(vn_data.get("verses", []))
                                if v1_cnt != vn_cnt:
                                    book_name = BOOK_NAMES.get(book, "Unknown")
                                    errors.append(f"{book} ({book_name}) Chapter file {ch_file}: {v1} ({v1_cnt}) != {vn} ({vn_cnt})")
                        except: continue
                        
        if errors:
            self.fail(f"Verse count inconsistencies between versions:\n" + "\n".join(errors[:20]))

    def test_json_integrity(self):
        versions = get_versions()
        for v in versions:
            v_path = os.path.join(BIBLE_ROOT, v)
            for root, _, files in os.walk(v_path):
                for file in files:
                    if file.endswith(".json"):
                        path = os.path.join(root, file)
                        with self.subTest(file=path):
                            with open(path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                self.assertIn("verses", data)
                                self.assertIsInstance(data["verses"], list)
                                self.assertGreater(len(data["verses"]), 0)

    def test_all_chapters_verse_counts(self):
        """Verifies for every chapter if the verses amount is correct, according to standard baseline."""
        versions = get_versions()
        for version in versions:
            version_path = os.path.join(BIBLE_ROOT, version)
            errors = []
            
            for book, expected_list in STANDARD_VERSE_COUNTS.items():
                book_path = os.path.join(version_path, book)
                book_name = BOOK_NAMES.get(book, book)
                
                if not os.path.exists(book_path):
                    continue
                
                for i, expected_verses in enumerate(expected_list):
                    chapter = i + 1
                    file_path = os.path.join(book_path, f"{chapter}.json")
                    
                    if not os.path.exists(file_path):
                        # Missing chapters are handled in test_all_versions_structure
                        continue
                        
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            actual_verses = len(data.get("verses", []))
                            if actual_verses != expected_verses:
                                errors.append(f"{book} ({book_name}) {chapter}: expected {expected_verses}, found {actual_verses}")
                    except Exception as e:
                        errors.append(f"{book} ({book_name}) {chapter}: error reading file - {str(e)}")
            
            if errors:
                # Limit output to first 50 errors for readability
                msg = f"Version {version} has {len(errors)} verse count deviations:\n" + "\n".join(errors[:50])
                if len(errors) > 50:
                    msg += f"\n... and {len(errors) - 50} more."
                self.fail(msg)

if __name__ == "__main__":
    unittest.main()
