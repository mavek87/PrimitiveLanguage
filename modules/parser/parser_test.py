import pytest
import sqlite3
import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from modules.parser import db_builder


TEST_DB = "test_app.db"


@pytest.fixture
def test_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    original_path = db_builder.DATABASE_PATH
    db_builder.DATABASE_PATH = TEST_DB

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db_builder.DATABASE_PATH = original_path


def test_init_database(test_db):
    conn = db_builder.init_database()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    assert "Concepts" in tables
    assert "Translations" in tables
    assert "UserMemory" in tables

    conn.close()


def test_parse_words_file():
    words_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "google-10000-english.txt",
    )
    words = db_builder.parse_words_file(words_file, limit=10)

    assert len(words) == 10
    assert words[0] == "the"
    assert words[1] == "of"


def test_populate_database(test_db):
    words = ["test", "word", "example"]
    translations = {"test": "prova", "word": "parola"}

    db_builder.populate_database(words, translations)

    conn = db_builder.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Concepts")
    assert cursor.fetchone()[0] == 3

    cursor.execute("SELECT word_english FROM Concepts WHERE word_english = 'test'")
    assert cursor.fetchone()[0] == "test"

    cursor.execute("SELECT COUNT(*) FROM Translations WHERE concept_id = 1")
    assert cursor.fetchone()[0] == 1

    cursor.execute("SELECT translation FROM Translations WHERE concept_id = 1")
    assert cursor.fetchone()[0] == "prova"

    conn.close()


def test_synonyms_handling(test_db):
    words = ["dress"]
    translations = {"dress": "vestito/abito"}

    db_builder.populate_database(words, translations)

    conn = db_builder.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT translation FROM Translations WHERE concept_id = 1 ORDER BY translation"
    )
    results = cursor.fetchall()
    assert len(results) == 2
    assert results[0][0] == "abito"
    assert results[1][0] == "vestito"

    conn.close()


def test_concept_and_translations_relationship(test_db):
    words = ["cat", "dog"]
    translations = {"cat": "gatto", "dog": "cane"}

    db_builder.populate_database(words, translations)

    conn = db_builder.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.word_english, t.translation
        FROM Concepts c
        JOIN Translations t ON c.id = t.concept_id
        ORDER BY c.word_english
    """)
    results = cursor.fetchall()

    assert results[0] == ("cat", "gatto")
    assert results[1] == ("dog", "cane")

    conn.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
