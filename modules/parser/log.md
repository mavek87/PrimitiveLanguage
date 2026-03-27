# Log - Parser Module

## 2026-03-27 | decisione: setup | impatto: alto
- Configurato pyproject.toml con dipendenze: flet, fsrs, requests
- Scaricato google-10000-english.txt (prime 1000 parole disponibili)
- Creati README.md e TODO.md
- Aggiornato todo con task iniziali

## 2026-03-27 | decisione: struttura moduli | impatto: alto
- Create directory modules/parser, modules/srs_engine, modules/ui
- Creati checklist.md e state.md per parser module
- Approccio ibrido: vocaboli da file inglese + traduzioni manuali progressive

## 2026-03-27 | decisione: test | impatto: alto
- Creato parser_test.py con 5 test
- test_init_database: verifica creazione tabelle
- test_parse_words_file: verifica parsing file vocaboli
- test_populate_database: verifica inserimento dati
- test_synonyms_handling: verifica gestione sinonimie (split /)
- test_concept_and_translations_relationship: verifica relazioni DB
- 5 test passati