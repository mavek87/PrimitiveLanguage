import sqlite3
import os

DATABASE_PATH = "app.db"

MANUAL_TRANSLATIONS = {
    "the": "il/lo/la",
    "of": "di",
    "and": "e",
    "to": "a/verso",
    "a": "un/uno/una",
    "in": "in",
    "for": "per",
    "is": "essere",
    "on": "su",
    "that": "che/quello",
    "by": "per/da",
    "this": "questo/questa",
    "with": "con",
    "i": "io",
    "you": "tu/lei",
    "it": "esso/essa",
    "not": "non",
    "or": "o",
    "be": "essere",
    "are": "essere",
    "was": "essere (passato)",
    "were": "essere (passato)",
    "been": "essere (participio)",
    "have": "avere",
    "has": "avere",
    "had": "avere (passato)",
    "do": "fare",
    "does": "fare (terza persona)",
    "did": "fare (passato)",
    "will": "volere/futuro",
    "would": "condizionale",
    "can": "potere",
    "could": "potere (passato)",
    "should": "dovere",
    "may": "potere",
    "might": "potere (passato)",
    "must": "dovere",
    "only": "solo",
    "other": "altro",
    "than": "di/che",
    "then": "allora/poi",
    "also": "anche",
    "into": "in/dentro",
    "its": "suo/sua",
    "make": "fare",
    "just": "solo/giusto",
    "over": "su/oltre",
    "such": "tale",
    "take": "prendere",
    "come": "venire",
    "these": "questi/queste",
    "know": "sapere",
    "see": "vedere",
    "use": "usare",
    "get": "ottenere",
    "go": "andare",
    "goes": "andare (terza)",
    "going": "andare (gerundio)",
    "went": "andare (passato)",
    "gone": "andare (participio)",
    "come": "venire",
    "came": "venire (passato)",
    "back": "indietro",
    "after": "dopo",
    "first": "primo",
    "two": "due",
    "new": "nuovo",
    "year": "anno",
    "most": "più",
    "people": "persona/gente",
    "way": "via/modo",
    "well": "bene",
    "even": "anche",
    "day": "giorno",
    "now": "ora",
    "find": "trovare",
    "give": "dare",
    "tell": "dire",
    "try": "provare",
    "call": "chiamare",
    "need": "bisogno",
    "feel": "sentire",
    "become": "diventare",
    "leave": "lasciare",
    "put": "mettere",
    "keep": "mantenere",
    "let": "lasciare",
    "begin": "iniziare",
    "seem": "sembrare",
    "help": "aiutare",
    "show": "mostrare",
    "hear": "sentire",
    "play": "giocare",
    "run": "correre",
    "move": "muovere",
    "live": "vivere",
    "believe": "credere",
    "bring": "portare",
    "happen": "accadere",
    "write": "scrivere",
    "provide": "fornire",
    "sit": "sedersi",
    "stand": "stare in piedi",
    "lose": "perdere",
    "pay": "pagare",
    "meet": "incontrare",
    "include": "includere",
    "continue": "continuare",
    "set": "impostare",
    "learn": "imparare",
    "change": "cambiare",
    "lead": "guidare",
    "understand": "capire",
    "watch": "guardare",
    "follow": "seguire",
    "stop": "fermare",
    "create": "creare",
    "speak": "parlare",
    "read": "leggere",
    "allow": "permettere",
    "add": "aggiungere",
    "spend": "spendere",
    "grow": "crescere",
    "open": "aprire",
    "walk": "camminare",
    "win": "vincere",
    "offer": "offrire",
    "remember": "ricordare",
    "love": "amare",
    "consider": "considerare",
    "appear": "apparire",
    "buy": "comprare",
    "wait": "aspettare",
    "serve": "servire",
    "die": "morire",
    "send": "inviare",
    "expect": "aspettarsi",
    "build": "costruire",
    "stay": "stare",
    "fall": "cadere",
    "cut": "tagliare",
    "reach": "raggiungere",
    "kill": "uccidere",
    "remain": "rimanere",
    "suggest": "suggerire",
    "raise": "alzare",
    "pass": "passare",
    "sell": "vendere",
    "require": "richiedere",
    "report": "riferire",
    "decide": "decidere",
    "pull": "tirare",
}


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_english TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            image_url TEXT,
            tier INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id INTEGER NOT NULL,
            lang_code TEXT NOT NULL,
            translation TEXT NOT NULL,
            FOREIGN KEY (concept_id) REFERENCES Concepts(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserMemory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id INTEGER NOT NULL,
            easiness REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            repetitions INTEGER DEFAULT 0,
            due_date TEXT,
            last_review TEXT,
            FOREIGN KEY (concept_id) REFERENCES Concepts(id)
        )
    """)

    conn.commit()
    return conn


def parse_words_file(filepath, limit=100):
    words = []
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            word = line.strip().lower()
            if word:
                words.append(word)
    return words


def populate_database(words, translations_dict):
    conn = init_database()
    cursor = conn.cursor()

    for word in words:
        cursor.execute(
            "INSERT INTO Concepts (word_english, tier) VALUES (?, 1)", (word,)
        )
        concept_id = cursor.lastrowid

        italian = translations_dict.get(word, "")
        if italian:
            for trans in italian.split("/"):
                cursor.execute(
                    "INSERT INTO Translations (concept_id, lang_code, translation) VALUES (?, 'it', ?)",
                    (concept_id, trans.strip()),
                )

        cursor.execute(
            "INSERT INTO UserMemory (concept_id, due_date) VALUES (?, datetime('now'))",
            (concept_id,),
        )

    conn.commit()
    conn.close()
    print(f"Database popolato con {len(words)} parole")


if __name__ == "__main__":
    words_file = "data/google-10000-english.txt"
    if os.path.exists(words_file):
        words = parse_words_file(words_file, limit=100)
        populate_database(words, MANUAL_TRANSLATIONS)
    else:
        print(f"File {words_file} non trovato")
