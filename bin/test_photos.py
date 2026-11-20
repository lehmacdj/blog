import sqlite3
import unittest

from photos import _keywords_query, normalize_caption


class KeywordsQueryTests(unittest.TestCase):
    def test_finds_numbered_join_table(self):
        db = sqlite3.connect(":memory:")
        db.executescript("""
            CREATE TABLE ZASSET (Z_PK INTEGER PRIMARY KEY, ZUUID TEXT);
            CREATE TABLE ZADDITIONALASSETATTRIBUTES (
                Z_PK INTEGER PRIMARY KEY, ZASSET INTEGER);
            CREATE TABLE ZKEYWORD (Z_PK INTEGER PRIMARY KEY, ZTITLE TEXT);
            CREATE TABLE Z_1KEYWORDS (
                Z_1ASSETATTRIBUTES INTEGER, Z_53KEYWORDS INTEGER);
            INSERT INTO ZASSET VALUES (1, 'U1'), (2, 'U2');
            INSERT INTO ZADDITIONALASSETATTRIBUTES VALUES (10, 1), (20, 2);
            INSERT INTO ZKEYWORD VALUES (5, 'travel'), (6, 'balloons');
            INSERT INTO Z_1KEYWORDS VALUES (10, 5), (10, 6);
        """)
        self.assertEqual(
            db.execute(_keywords_query(db)).fetchall(),
            [("U1", "balloons"), ("U1", "travel")],
        )

    def test_missing_join_table_is_an_error(self):
        db = sqlite3.connect(":memory:")
        with self.assertRaises(sqlite3.OperationalError):
            _keywords_query(db)


class NormalizeCaptionTests(unittest.TestCase):
    def test_line_separators_become_newlines(self):
        self.assertEqual(
            normalize_caption(" One.\u2028\u2028Two.\r\nThree.\n"),
            "One.\n\nTwo.\nThree.",
        )


if __name__ == "__main__":
    unittest.main()
