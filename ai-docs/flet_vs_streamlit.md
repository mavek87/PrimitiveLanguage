---
fonte: Ricerca Web (Flet vs Streamlit per Flashcard App offline)
data: 2026-03-27
moduli_rilevanti: modules/ui
perche_e_qui: Determinare il miglior framework Python per un'interfaccia interattiva da studio.
changelog:
  - 2026-03-27: Creazione del documento.
---

# UI Framework: Flet vs Streamlit

Mentre per i prototipi sui dati Streamlit è impareggiabile, per un'applicazione "Language Learning" orientata all'utente finale (una flashcard app) la ricerca dimostra che **Flet** è nettamente superiore.

## 1. Modello di Esecuzione
- **Streamlit** re-esegue l'intero script Python dall'alto verso il basso a ogni interazione (es. quando schiacci un bottone). Per girare centinaia di flashcard, questo causa rallentamenti, refresh sgradevoli e rende ostica la gestione dello stato interattivo complesso (come trascinare blocchi in un esercizio di completamento).
- **Flet** è basato su Flutter (di Google) e usa un modello "Event-Driven" tradizionale. L'interfaccia non si ricarica mai. Il tocco su uno schermo gira la card fluidamente.

## 2. Piattaforme e Offline
- **Streamlit** è pensato per girare su un server e mostrato su browser. Non può essere compilato facilmente in un'App offline per cellulare (che è dove gli utenti studiano di solito le flashcard).
- **Flet** nativamente permette, a partire dallo stesso codice Python, di pacchettizzare un'App Desktop (Windows/Mac), un'App Web, e soprattutto un'App Mobile (.apk / iOS) stand-alone che funziona totalmente **offline**.

## Conclusione
Per il modulo `modules/ui` abbandoniamo l'ipotesi Streamlit e procediamo con **Flet**. Garantirà transizioni fluide tra le immagini e le parole, essenziali per la *Dual-Coding Theory*, e permetterà un domani di portare l'app facilmente sullo smartphone dell'utente.
