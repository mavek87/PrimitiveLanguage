# Log - UI Module

## 2026-03-27 | refactoring: frase builder click invece drag-drop | impatto: alto
- Sostituito drag-and-drop con click per comporre/frammentare frase
- Ogni click aggiunge/rimuove parola dalla frase
- Cliccando parola già selezionata la rimuove
- 38 test passati

## 2026-03-27 | implementazione: frase builder completo | impatto: alto
- Implementato frase builder con DragTarget/Draggable
- 10 parole con tier (pronouns, verbs, nouns, adjectives)
- DragTarget per drop area
- Bottoni Verifica e Pulisci funzionanti
- 35 test passati

## 2026-03-27 | correzione: fix API Flet 0.83 | impatto: alto
- Corretto ft.colors -> ft.Colors
- Corretto ft.alignment.center -> ft.Alignment.CENTER
- Corretto ft.icons.IMAGE -> "image" (string)
- Corretto ft.ElevatedButton -> ft.Button (deprecato)
- Corretto back_to_menu() reset stato
- Corretto Border() e rimosso scroll Container

## 2026-03-27 | decisione: ui implementation | impatto: alto
- main.py creato con app Flet completa
- Menu principale con 3 pulsanti (Review, Frasi, Statistiche)
- Flashcard Reviewer implementato con:
  - Visualizzazione parola + immagine fallback
  - Rivelazione risposta
  - Rating buttons 1-4
- Statistiche mostrate (carte dovute, totale, intervallo medio)
- Frase Builder base (placeholder)
- Integrazione con SRS controller funzionante