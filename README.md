# Lingua Primitiva - Progetto di Apprendimento Linguistico

## Scopo del Progetto
Decostruire il normale processo di apprendimento linguistico ("Pidginization") per acquisire in tempi record una "comunicazione di sopravvivenza" basica. L'obiettivo non è la fluency grammaticale ortodossa ma esprimersi in maniera primordiale (es. "io essere uomo, io volere cibo, tu brutto, casa buona").

Lo spunto storico è la **"Lingua Franca" (Sabir)** usata dai mercanti medievali del Mediterraneo.

## Stack Tecnologico
- **Backend**: Python + SQLite
- **UI**: Flet (cross-platform, offline-ready)
- **SRS**: FSRS (algoritmo ML, 20-30% più efficiente)
- **Immagini**: Pixabay API

## Struttura dei Moduli

| Modulo | Descrizione | File |
|--------|-------------|------|
| `modules/parser/` | Parsing vocaboli e gestione database SQLite | `db_builder.py` |
| `modules/srs_engine/` | Motore di spaced repetition FSRS | `srs_controller.py` |
| `modules/ui/` | Applicazione Flet (Flashcard + Frase Builder) | `ui.py` |

## Setup
```bash
pip install flet fsrs requests
```

## Indice Moduli
- [Parser](./modules/parser/state.md)
- [SRS Engine](./modules/srs_engine/state.md)
- [UI](./modules/ui/state.md)