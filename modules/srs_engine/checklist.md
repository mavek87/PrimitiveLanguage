# SRS Engine Module - Checklist

## Obiettivo
Motore di spaced repetition basato su FSRS.

## Task
- [x] Implementare wrapper per fsrs.Scheduler
- [x] Creare API assess_recall(concept_id, rating)
- [x] Implementare espansione i+1 (sblocco Tier 2/3)
- [x] Testare algoritmo con dati fittizi

## Criteri di Verifica
- [x] Scheduler FSRS correttamente inizializzato
- [x] Rating 1-4 correttamente aggiornati nel database
- [x] Espansione i+1 attivata quando stability media > 85%