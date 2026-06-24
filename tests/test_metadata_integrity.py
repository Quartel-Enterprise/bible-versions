import os
import re
import json
import unittest

BIBLE_ROOT = os.path.join(os.getcwd(), "bible")

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

def get_versions():
    if not os.path.exists(BIBLE_ROOT):
        return []
    return [v for v in os.listdir(BIBLE_ROOT) if os.path.isdir(os.path.join(BIBLE_ROOT, v))]

EXPECTED_METADATA = {
    "ACF": {
        "name": "Almeida Corrigida Fiel",
        "id": "ACF",
        "version": "1.0.0",
        "language": "pt",
        "country": "br",
        "year": {"begin": 1994, "end": 2011}
    },
    "WEB": {
        "name": "World English Bible",
        "id": "WEB",
        "version": "1.0.0",
        "language": "en",
        "country": "-",
        "year": {"begin": 1997, "end": 2020}
    }
}

class TestMetadataIntegrity(unittest.TestCase):
    def test_metadata_files_exist(self):
        """Verifies that each version has a metadata.json file."""
        versions = get_versions()
        for version in versions:
            with self.subTest(version=version):
                metadata_path = os.path.join(BIBLE_ROOT, version, "metadata.json")
                self.assertTrue(os.path.exists(metadata_path), f"metadata.json missing in {version}")

    def test_metadata_structure_and_content(self):
        """Verifies the structure and content of each metadata.json file."""
        versions = get_versions()
        for version in versions:
            metadata_path = os.path.join(BIBLE_ROOT, version, "metadata.json")
            if not os.path.exists(metadata_path):
                continue

            with self.subTest(version=version):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        self.fail(f"Invalid JSON in {metadata_path}")

                    # Check required fields
                    self.assertIn("name", data, f"Missing 'name' in {metadata_path}")
                    self.assertEqual(data.get("id"), version, f"Metadata ID mismatch in {version}")
                    self.assertIn("version", data, f"Missing 'version' in {metadata_path}")
                    self.assertIsInstance(data["version"], str, f"'version' must be a string in {metadata_path}")
                    self.assertRegex(
                        data["version"],
                        SEMVER_PATTERN,
                        f"'version' must follow SemVer (major.minor.patch) in {metadata_path}",
                    )
                    self.assertIn("language", data, f"Missing 'language' in {metadata_path}")
                    self.assertIn("country", data, f"Missing 'country' in {metadata_path}")
                    self.assertIn("year", data, f"Missing 'year' in {metadata_path}")
                    
                    year = data.get("year", {})
                    self.assertIsInstance(year, dict, f"'year' must be an object in {metadata_path}")
                    self.assertIn("begin", year, f"Missing 'year.begin' in {metadata_path}")
                    self.assertIn("end", year, f"Missing 'year.end' in {metadata_path}")
                    self.assertIsInstance(year["begin"], int, f"'year.begin' must be an integer in {metadata_path}")
                    self.assertIsInstance(year["end"], int, f"'year.end' must be an integer in {metadata_path}")

    def test_known_metadata_values(self):
        """Verifies specific field values for known Bible versions."""
        for version, expected in EXPECTED_METADATA.items():
            metadata_path = os.path.join(BIBLE_ROOT, version, "metadata.json")
            if not os.path.exists(metadata_path):
                continue

            with self.subTest(version=version):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    actual = json.load(f)
                    self.assertEqual(actual, expected, f"Metadata content mismatch for {version}")

if __name__ == "__main__":
    unittest.main()
