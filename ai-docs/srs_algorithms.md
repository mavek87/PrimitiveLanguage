---
fonte: Ricerca Web (Comparazione Algoritmi Spaced Repetition)
data: 2026-03-27
moduli_rilevanti: modules/srs
perche_e_qui: Fornire le basi teoriche e comparative per l'implementazione del motore SRS dell'app.
changelog:
  - 2026-03-27: Creazione del documento.
---

# Algoritmi Spaced Repetition (SRS): SuperMemo-2 vs FSRS

Nella costruzione di un sistema di apprendimento basato su SRS, la scelta dell'algoritmo di scheduling è fondamentale per ottimizzare il tempo di studio e la ritenzione. I due candidati principali sono SM-2 e FSRS.

## 1. SuperMemo-2 (SM-2)
Creato da Piotr Wozniak nel 1987, è il gold standard storico (usato a lungo come default da Anki).
- **Meccanica:** Si basa su uno *spacing effect* rudimentale ma molto efficace. Usa "Easiness Factor (EF)" (moltiplicatore della difficoltà), "Quality of Response (0-5)" e "Repetition Number".
- **Vantaggi:** Semplice, formula matematica facilmente implementabile (non richiede machine learning), altamente testato nel tempo.
- **Svantaggi:** Regole fisse, non si adatta al 100% alla reale curva di memoria individuale dell'utente e gestisce male i giorni di "ritardo" (se l'utente non apre l'app per giorni).

## 2. FSRS (Free Spaced Repetition Scheduler)
Algoritmo moderno basato su Machine Learning (ora disponibile come variante avanzata in Anki).
- **Meccanica:** Si basa sul "Three Component Model of Memory" tracciando *Retrievability (R)* (probabilità di ricordo immediato), *Stability (S)* (tempo necessario per scendere dal 100% al 90% di ritenzione) e *Difficulty (D)*.
- **Vantaggi:** Altamente personalizzato in base allo storico dell'utente (impara come impara l'utente). Richiede storicamente il 20-30% di review **in meno** per ottenere la stessa ritenzione, salvando molto tempo. Gestuale brillantemente i ritardi nello studio. Target retention è parametrizzabile dall'utente.
- **Svantaggi:** Logica soggiacente complessa, richiede un modello di machine learning o un porting matematico complesso e uno storico di review continuo per fittare i pesi ottimali.

## Conclusione Tecnica per il Progetto
Per il modulo `modules/srs/` della "Lingua Primitiva", iniziare con l'algoritmo **SM-2** è la scelta più rapida per un MVP a causa della sua facilità d'implementazione. Tuttavia, se l'obiettivo è il massimo risparmio di tempo per l'utente, studiare l'implementazione in Python di **FSRS** (esistono librerie open-source come `fsrs-rs`/`pyfsrs`) potrebbe essere il differenziatore tecnico chiave dell'applicazione per permettere l'apprendimento ultra-rapido.
