import pytest
import os
import sys
import sqlite3

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from modules.parser import db_builder
from modules.srs_engine import srs_controller


TEST_DB = "test_ui.db"


@pytest.fixture
def test_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    original_path = db_builder.DATABASE_PATH
    db_builder.DATABASE_PATH = TEST_DB

    words = ["cat", "dog", "house", "food", "water"]
    translations = {
        "cat": "gatto",
        "dog": "cane",
        "house": "casa",
        "food": "cibo",
        "water": "acqua",
    }
    db_builder.populate_database(words, translations)

    srs_controller.DATABASE_PATH = TEST_DB

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db_builder.DATABASE_PATH = original_path
    srs_controller.DATABASE_PATH = original_path


def test_main_module_import():
    from modules.ui import ui

    assert ui is not None


def test_get_due_cards_returns_list(test_db):
    cards = srs_controller.get_due_cards(10)

    assert isinstance(cards, list)
    assert len(cards) > 0
    assert all("concept_id" in c for c in cards)
    assert all("word" in c for c in cards)
    assert all("translation" in c for c in cards)


def test_rate_card_updates_db(test_db):
    cards = srs_controller.get_due_cards(1)
    concept_id = cards[0]["concept_id"]

    conn = srs_controller.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT repetitions FROM UserMemory WHERE concept_id = ?", (concept_id,)
    )
    reps_before = cursor.fetchone()[0]
    conn.close()

    result = srs_controller.assess_recall(concept_id, 3)

    conn = srs_controller.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT repetitions, interval FROM UserMemory WHERE concept_id = ?",
        (concept_id,),
    )
    row = cursor.fetchone()
    conn.close()

    assert row[0] > reps_before
    assert row[1] > 0


def test_empty_due_cards_after_review(test_db):
    cards = srs_controller.get_due_cards(100)

    for card in cards:
        srs_controller.assess_recall(card["concept_id"], 3)

    remaining = srs_controller.get_due_cards(10)

    for card in cards:
        found = any(c["concept_id"] == card["concept_id"] for c in remaining)
        if found:
            conn = srs_controller.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT due_date FROM UserMemory WHERE concept_id = ?",
                (card["concept_id"],),
            )
            due = cursor.fetchone()[0]
            conn.close()
            assert due is not None


def test_review_complete_message_shown():
    pass


def test_stats_show_correct_counts(test_db):
    due = srs_controller.get_due_cards(100)
    due_count = len(due)

    conn = srs_controller.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Concepts")
    total = cursor.fetchone()[0]
    conn.close()

    assert due_count <= total
    assert total == 5


def test_image_fallback_when_missing(test_db):
    cards = srs_controller.get_due_cards(1)

    for card in cards:
        assert card.get("image_url") is None or card.get("image_url") == ""


def test_translation_always_available(test_db):
    cards = srs_controller.get_due_cards(100)

    for card in cards:
        assert "translation" in card
        assert card["translation"] is not None


def test_ui_initialization():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    assert app.page == page
    assert app.current_card_index == 0
    assert app.show_answer == False
    assert len(app.due_cards) == 0


def test_start_review_loads_due_cards():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp
    from modules.srs_engine import srs_controller

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_review(None)

    assert len(app.due_cards) > 0
    assert app.current_card_index == 0
    assert app.show_answer == False


def test_start_review_empty_due_cards(test_db):
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    cards = srs_controller.get_due_cards(100)
    for card in cards:
        srs_controller.assess_recall(card["concept_id"], 3)

    app.start_review(None)

    assert len(app.due_cards) == 0


def test_reveal_answer_sets_flag():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp
    from modules.srs_engine import srs_controller

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.due_cards = srs_controller.get_due_cards(1)
    app.current_card_index = 0
    app.show_answer = False

    app.reveal_answer(None)

    assert app.show_answer == True


def test_rate_card_advances_index():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp
    from modules.srs_engine import srs_controller

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    cards = srs_controller.get_due_cards(3)
    app.due_cards = cards
    app.current_card_index = 0
    app.show_answer = True

    app.rate_card(3)

    assert app.current_card_index == 1
    assert app.show_answer == False


def test_back_to_menu_resets_state():
    import flet as ft
    from unittest.mock import MagicMock, call
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.due_cards = [{"word": "test"}]
    app.current_card_index = 5
    app.show_answer = True

    app.back_to_menu(None)

    assert len(app.due_cards) == 0
    assert app.current_card_index == 0
    assert app.show_answer == False


def test_full_user_simulation():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp
    from modules.srs_engine import srs_controller
    from modules.parser import db_builder

    original_path = db_builder.DATABASE_PATH
    db_builder.DATABASE_PATH = "test_simulation.db"
    srs_controller.DATABASE_PATH = "test_simulation.db"

    words = ["hello", "world", "test"]
    translations = {"hello": "ciao", "world": "mondo", "test": "prova"}
    db_builder.populate_database(words, translations)

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_review(None)
    assert len(app.due_cards) == 3

    card = app.due_cards[app.current_card_index]
    app.reveal_answer(None)
    assert app.show_answer == True

    app.rate_card(3)
    assert app.current_card_index == 1

    app.reveal_answer(None)
    app.rate_card(4)
    assert app.current_card_index == 2

    app.reveal_answer(None)
    app.rate_card(2)
    assert app.current_card_index == 3

    if os.path.exists("test_simulation.db"):
        os.remove("test_simulation.db")

    db_builder.DATABASE_PATH = original_path
    srs_controller.DATABASE_PATH = original_path


def test_phrase_builder_initialization():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)

    assert hasattr(app, "phrase_blocks")
    assert hasattr(app, "selected_words")
    assert len(app.phrase_blocks) > 0
    assert len(app.selected_words) == 0


def test_phrase_builder_word_blocks():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)

    tier1_words = [b["word"] for b in app.phrase_blocks if b["tier"] == 1]
    tier2_words = [b["word"] for b in app.phrase_blocks if b["tier"] == 2]
    tier3_words = [b["word"] for b in app.phrase_blocks if b["tier"] == 3]

    assert len(tier1_words) > 0
    assert len(tier2_words) > 0
    assert len(tier3_words) > 0
    assert "io" in tier1_words
    assert "andare" in tier2_words


def test_phrase_builder_clear():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)
    app.selected_words = ["io", "andare"]

    app.clear_phrase(None)

    assert len(app.selected_words) == 0


def test_phrase_builder_check_empty():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)
    app.selected_words = []

    app.check_phrase(None)

    assert app.result_text.value == "Costruisci una frase prima!"


def test_phrase_builder_check_with_words():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)
    app.selected_words = ["io", "andare", "casa"]

    app.check_phrase(None)

    assert "io andare casa" in app.result_text.value


def test_phrase_builder_click_adds_word():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)
    assert app.selected_words == []

    app._on_word_click("andare")

    assert "andare" in app.selected_words
    assert page.update.called


def test_phrase_builder_click_removes_word():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)
    app.selected_words = ["io", "andare"]

    app._on_word_click("andare")

    assert "andare" not in app.selected_words
    assert "io" in app.selected_words


def test_phrase_builder_tier_colors():
    import flet as ft
    from unittest.mock import MagicMock
    from modules.ui.ui import LinguaPrimitivaApp

    page = MagicMock(spec=ft.Page)
    app = LinguaPrimitivaApp(page)

    app.start_frase_builder(None)

    assert app._get_tier_color(1) == ft.Colors.BLUE_700
    assert app._get_tier_color(2) == ft.Colors.ORANGE_700
    assert app._get_tier_color(3) == ft.Colors.PURPLE_700


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
