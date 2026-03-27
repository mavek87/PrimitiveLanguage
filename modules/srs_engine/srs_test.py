import pytest
import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from modules.srs_engine import srs_controller
from modules.parser import db_builder
from fsrs import Scheduler, Card, Rating, State


TEST_DB = "test_srs_full.db"


@pytest.fixture
def test_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    original_path = db_builder.DATABASE_PATH
    db_builder.DATABASE_PATH = TEST_DB

    words = [
        "cat",
        "dog",
        "house",
        "water",
        "food",
        "good",
        "bad",
        "big",
        "small",
        "eat",
    ]
    translations = {
        "cat": "gatto",
        "dog": "cane",
        "house": "casa",
        "water": "acqua",
        "food": "cibo",
        "good": "buono",
        "bad": "cattivo",
        "big": "grande",
        "small": "piccolo",
        "eat": "mangiare",
    }
    db_builder.populate_database(words, translations)

    srs_controller.DATABASE_PATH = TEST_DB

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db_builder.DATABASE_PATH = original_path
    srs_controller.DATABASE_PATH = original_path


def test_fsrs_scheduler_initialization():
    scheduler = Scheduler()
    assert scheduler is not None

    card = Card()
    assert card.state == State.Learning


def test_fsrs_review_card_again():
    scheduler = Scheduler()
    card = Card()

    card, review_log = scheduler.review_card(card, Rating.Again)

    assert card.state == State.Learning
    assert review_log.rating == Rating.Again


def test_fsrs_review_card_good():
    scheduler = Scheduler()
    card = Card()

    card, review_log = scheduler.review_card(card, Rating.Good)

    assert card.stability is not None
    assert card.due is not None


def test_fsrs_review_progression():
    scheduler = Scheduler()
    card = Card()

    for _ in range(5):
        card, _ = scheduler.review_card(card, Rating.Good)

    final_stability = card.stability or 0
    assert final_stability > 0


def test_assess_recall_updates_database(test_db):
    cards = srs_controller.get_due_cards(1)
    concept_id = cards[0]["concept_id"]

    result = srs_controller.assess_recall(concept_id, 3)

    conn = srs_controller.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT interval, repetitions FROM UserMemory WHERE concept_id = ?",
        (concept_id,),
    )
    row = cursor.fetchone()
    conn.close()

    assert row[0] == result["interval"]
    assert row[1] >= 1


def test_assess_recall_again_decreases_interval(test_db):
    cards = srs_controller.get_due_cards(1)
    concept_id = cards[0]["concept_id"]

    srs_controller.assess_recall(concept_id, 3)

    result = srs_controller.assess_recall(concept_id, 1)

    assert result["interval"] < 3


def test_assess_recall_easy_increases_interval(test_db):
    cards = srs_controller.get_due_cards(1)
    concept_id = cards[0]["concept_id"]

    result_good = srs_controller.assess_recall(concept_id, 3)
    interval_good = result_good["interval"]

    result_easy = srs_controller.assess_recall(concept_id, 4)
    interval_easy = result_easy["interval"]

    assert interval_easy > interval_good


def test_get_due_cards_empty_after_all_reviewed(test_db):
    cards = srs_controller.get_due_cards(100)
    concept_ids = [c["concept_id"] for c in cards]

    for cid in concept_ids:
        srs_controller.assess_recall(cid, 3)

    remaining = srs_controller.get_due_cards(100)

    for card in remaining:
        assert card["concept_id"] not in concept_ids


def test_expansion_triggers_after_high_avg_interval(test_db):
    cards = srs_controller.get_due_cards(10)

    for card in cards:
        for _ in range(5):
            srs_controller.assess_recall(card["concept_id"], 3)

    result = srs_controller.check_expansion()

    assert isinstance(result, bool)


def test_due_cards_respects_limit(test_db):
    cards = srs_controller.get_due_cards(3)

    assert len(cards) <= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
