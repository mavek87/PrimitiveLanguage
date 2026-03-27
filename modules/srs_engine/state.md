# State - SRS Engine Module

## Situazione Attuale
- Database creato con 100 concetti e 58 traduzioni
- Parser completato
- SRS Controller implementato con:
  - get_due_cards()
  - assess_recall(concept_id, rating)
  - check_expansion()
- 5 carte dovute rilevate correttamente

## Prossimo Step
- Implementare UI Flet (Flashcard Reviewer + Frase Builder)
- Testare integrazione UI con SRS engine

## Note
- Libreria fsrs installata (non pyfsrs)
- Rating: 1=Again, 2=Hard, 3=Good, 4=Easy
- Warning LSP non bloccanti