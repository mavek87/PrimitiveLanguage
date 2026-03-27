# TODO - Progetto Lingua Primitiva

## Setup Infrastruttura
- [x] Creare README.md con scopo progetto e architettura
- [x] Installare dipendenze: flet, fsrs, requests
- [x] Scaricare google-10000-english.txt (prime 1000 parole)

## Parser / Data Layer (modules/parser/)
- [x] Creare cartella modules/parser/
- [x] Creare db_builder.py per parsare vocaboli
- [x] Definire schema SQLite (Concepts, Translations, UserMemory)
- [x] Gestione sinonimie multiple (split /)
- [x] Testare parser con dati mock
- [x] Popolare database con prime 100 parole

## SRS Engine (modules/srs_engine/)
- [x] Creare cartella modules/srs_engine/
- [x] Implementare wrapper per fsrs.Scheduler
- [x] Creare API assess_recall(concept_id, rating)
- [x] Implementare espansione i+1 (sblocco Tier 2/3)
- [x] Testare algoritmo con dati fittizi

## UI Flet (modules/ui/)
- [x] Creare cartella modules/ui/
- [x] Implementare Flashcard Reviewer (Dual-Coding)
- [x] Implementare Frase Builder (click per comporre/frammentare)
- [x] Fix drag-drop non funzionante -> click toggle
- [x] Integrare con SRS engine
- [x] Testare UI end-to-end (35 test)

## Verbale
- [x] Aggiornare state.md in ogni modulo
- [x] Aggiornare log.md dopo ogni task significativa

## VERIFICA FINALE
- [x] Test: 35/35 passati
- [x] Build: OK
- [x] Fix API Flet 0.83: Colors, Alignment, Icon, Button, Border
- [x] Simulazione utente completa funzionante
- [x] Frase Builder drag-and-drop implementato

## COMPLETATO ✓