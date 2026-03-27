import sqlite3
import json
from datetime import datetime, timedelta, timezone
from fsrs import Scheduler, Card, Rating, State

DATABASE_PATH = "app.db"

scheduler = Scheduler()


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def get_card_data(concept_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT um.*, c.word_english
        FROM UserMemory um
        JOIN Concepts c ON um.concept_id = c.id
        WHERE um.concept_id = ?
    """,
        (concept_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "concept_id": row["concept_id"],
        "word_english": row["word_english"],
        "easiness": row["easiness"],
        "interval": row["interval"],
        "repetitions": row["repetitions"],
        "due_date": row["due_date"],
        "last_review": row["last_review"],
    }


def create_fsrs_card(card_data):
    card = Card()

    if (
        card_data
        and card_data.get("interval", 0) > 0
        and card_data.get("repetitions", 0) > 0
    ):
        card.difficulty = card_data.get("easiness", 2.5)
        card.stability = float(card_data.get("interval", 1))
        card.state = State(2)
        card.due = datetime.fromisoformat(
            card_data.get("due_date", datetime.now(timezone.utc).isoformat()).replace(
                "Z", "+00:00"
            )
        )
        card.last_review = datetime.fromisoformat(
            card_data.get(
                "last_review", datetime.now(timezone.utc).isoformat()
            ).replace("Z", "+00:00")
        )

    return card


def assess_recall(concept_id, rating_value):
    card_data = get_card_data(concept_id)
    card = create_fsrs_card(card_data)

    rating_map = {1: Rating.Again, 2: Rating.Hard, 3: Rating.Good, 4: Rating.Easy}
    rating = rating_map.get(rating_value, Rating.Good)

    card, review_log = scheduler.review_card(card, rating)

    conn = get_connection()
    cursor = conn.cursor()

    new_difficulty = card.difficulty
    new_stability = card.stability
    new_due = str(card.due)
    now_str = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        "SELECT repetitions FROM UserMemory WHERE concept_id = ?", (concept_id,)
    )
    current_reps = cursor.fetchone()[0] or 0
    new_reps = current_reps + 1

    cursor.execute(
        """
        UPDATE UserMemory
        SET easiness = ?,
            interval = ?,
            repetitions = ?,
            due_date = ?,
            last_review = ?
        WHERE concept_id = ?
    """,
        (
            new_difficulty,
            int(new_stability),
            new_reps,
            new_due,
            now_str,
            concept_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "next_review": new_due,
        "interval": int(new_stability),
        "difficulty": new_difficulty,
    }


def get_due_cards(limit=20):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.id, c.word_english, c.image_url, t.translation
        FROM Concepts c
        JOIN UserMemory um ON c.id = um.concept_id
        JOIN Translations t ON c.id = t.concept_id AND t.lang_code = 'it'
        WHERE um.due_date <= datetime('now')
        ORDER BY um.due_date ASC
        LIMIT ?
    """,
        (limit,),
    )

    results = cursor.fetchall()
    conn.close()

    return [
        {
            "concept_id": row["id"],
            "word": row["word_english"],
            "translation": row["translation"],
            "image_url": row["image_url"],
        }
        for row in results
    ]


def check_expansion():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(interval) as avg_interval
        FROM UserMemory
        WHERE repetitions > 2
    """)

    result = cursor.fetchone()
    avg_interval = result[0] if result and result[0] else 0

    if avg_interval > 21:
        cursor.execute("""
            UPDATE Concepts
            SET tier = 2
            WHERE tier = 1 AND id NOT IN (
                SELECT concept_id FROM UserMemory WHERE repetitions < 3
            )
        """)
        conn.commit()
        return True

    conn.close()
    return False


if __name__ == "__main__":
    due = get_due_cards(5)
    print(f"Carte dovute: {len(due)}")
    for card in due:
        print(f"  - {card['word']} ({card['translation']})")
