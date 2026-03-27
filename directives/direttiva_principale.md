# Direttiva Principale: Progetto "Lingua Primitiva"

## 1. Scopo Essenziale del Progetto
Il progetto mira a decostruire e "hackerare" il normale processo di apprendimento linguistico ("Pidginization"), aggirando completamente il muro cognitivo della grammatica. Lo scopo non è raggiungere la *fluency* grammaticale ortodossa, ma acquisire in tempi record una "comunicazione di sopravvivenza" di base, permettendo all'utente di esprimersi, per lo meno, in maniera primordiale (es. **io essere uomo, io volere cibo, tu brutto, casa buona**).

Lo spunto storico e filosofico del progetto risiede nella celebre **"Lingua Franca" (il Sabir)**, usata nel Medioevo dai mercanti del Mar Mediterraneo: pur non possedendo una grammatica complessa, permetteva loro di instaurare agevolmente conversazioni minime e cruciali tra parlanti di lingue totalmente slegate. 

L'applicazione replica questa immediatezza sfruttando brutalmente il **Principio di Pareto (80/20)**: instillare a livello mnemonico un ristretto nucleo di 1000 parole ad altissima frequenza copre l'80% delle micro-interazioni umane base. I verbi non vengono declinati, azzerando la curva d'apprendimento sintattica per favorire la comunicazione bruta.

## 2. Metodologie Cognitive e Considerazioni Tecniche
Le scelte architetturali si fondano su tre pilastri scientifici esplorati nell'analisi:

1. **Dual-Coding Theory (Associazione Visiva):** Anziché studiare per mezzo della traduzione verbale (es. l'italiano *Cane* -> l'inglese *Dog*), l'utente apprende tramite un'app che associa direttamente il vocabolo target a un'immagine universale. Questo scollega la lingua madre (italiano) dall'equazione, riduce il carico cognitivo da traduzione mentale e aumenta la ritenzione a lungo termine del ~65%.
2. **Spaced Repetition System (Motore SRS Avanzato):** L'utilizzo di algoritmi di Scheduling di memorizzazione. Nello specifico, si integrerà il modello basato su machine learning **FSRS** (accessibile in Python tramite la libreria `pyfsrs`), il quale valuta la stabilità mnemonica di ogni singola parola tagliando del 20-30% sul tempo di ripasso totale rispetto ai vecchi algoritmi standard.
3. **Ipotesi i+1 di Krashen (Espansione Fluida):** Il sistema non abbandona l'utente ai primi 1000 vocaboli primitivi della *Tranche 1-3*. Terminato l'assorbimento di base (la regola 80/20), l'algoritmo introduce un meccanismo di espansione. Sblocca silenziosamente pacchetti di parole superiori (Tier 2, Tier 3) presentandole fluidamente all'interno di un contesto dove l'utente domina il resto della frase (i+1), impedendo la pura stagnazione "Tarzan" e muovendo verso un arricchimento naturale.

---

## 3. Piano Ultra-Dettagliato di Implementazione

Per rispettare l'architettura a moduli isolati prescritta nelle regole d'ingaggio (`AGENTS.md`), il lavoro seguirà rigidamente le seguenti 4 Fasi basate sullo stack **Python + SQLite + pyfsrs + Flet**.

### Fase 1: Setup dell'Infrastruttura
1. Creare i file radice di progetto:
   - `README.md`: Con lo scopo base, la mappa dell'architettura e l'indice di tutti i moduli.
   - `TODO.md`: Con le macro-tasks e la lista prioritaria dello sviluppo concordato.
2. Inizializzare le dipendenze Python:
   - Libreria sqlite nativa per la persistenza agnostica dei dati e dei progressi SRS.
   - Framework `Flet` (basato su Flutter per un'UI fluida e cross-platform, non bloccante per app visuali).
   - `fsrs` (il motore logico spaziale).

### Fase 2: Modulo Parse e Data Layer (Il Database Agnostico)
La priorità è blindare la lista delle 1000 parole target in una forma strutturata.
1. Creazione della cartella `modules/parser/` con i suoi documenti base (`state.md`, `log.md`, `checklist.md`).
2. Sviluppo autonono dello script `db_builder.py` con Regular Expressions per parsare l'elenco testuale/Markdown `obbiettivo.md`.
3. **Architettura Database SQLite**:
   - Tabella `Concepts`: `[id_concetto, categoria, url_immagine_fallback]`. La riga cattura l'idea astratta.
   - Tabella `Translations`: `[id_concetto, lang_code, word]`. In questo modo l'App è del tutto **Agnostica**. I placeholder italiani usati in documentazione avranno code 'it', l'inglese 'en'; ma si potrà scalare su N lingue.
4. **Gestione Sinonimie Multiple**: Se il testo contiene varianti via splitters (es. `dress/clothes`), lo script inserirà due righe `Translations` valide associate allo stesso concetto ID. Approvando uno dei due termini l'utente avrà ragione. (Proprio come la logica degli Alias multi-link in Obsidian).
5. Scrittura di mock testuale o test automatico limitato per assicurare che simboli Markdown (titoli "Tranche", linee separatrici, numeri lista) non rompano il parser.

### Fase 3: Modulo Spaced Repetition System (The Brain)
Tutta la logica di ripetizione è rigorosamente isolata dalla GUI.
1. Creazione cartella `modules/srs_engine/` con i corrispettivi doc di logging.
2. Classe controller per fare astrazione sull'oggetto `Scheduler` locale di `pyfsrs`.
3. Aggiunta Tabella `UserMemory` in DB:
   - Traccia `[userId, id_concetto, retrievability, stability, difficulty, next_review_date, tier_lock_status]`.
4. Creazione API in Python locale `assess_recall(concept_id, rating_utente[1-4])`.
5. **Sub-modulo Espansione (i+1)**: Un routine asincrona (es. all'apertura dell'app o post ripasso) che computa la Media della *Stability* globale del "Tier Core" (Prime 1000). Superata una soglia prestabilita (es. 85%), scansiona M parole "Tier Expansion" impostandole su `Unlocked/Learning`.

### Fase 4: Modulo User Interface (L'App Flet)
L'UI è la mera esecutrice visuale degli eventi del Backend.
1. Creazione cartella `modules/ui/` con ciclo asincrono Flet.
2. **Flashcard Reviewer (Dual-Coding)**:
   - Sull'UI a tutto schermo l'utente è testato tramite un'Immagine gigantesca centrale.
   - In basso un campo di text-input o pulsante audio per fornire l'input nella lingua target.
   - Fallback: in totale assenza dell'Immagine nel Database, lo step mostrerà il termine italiano a tutto campo, garantendo lo scorrere dell'app anche se sprovvista di asset grafici iniziali.
   - Input validato dal DB (Sinonimi) e bottoni per il rating [1-4] re-immessi nello schedulatore.
3. **Esercitatore di Assemblaggio "Lingua Franca"**:
   - Un'UI specializzata ad incastro, dove l'app propone l'astrazione italiana (*Io vado a casa*)
   - Schermo diviso in blocchi semantici isolati ("Io + Andare + Casa") disordinati o trascinabili. L'utente compone frasi brutali senza badare a costruzioni e punteggiature grammaticali, cementificando l'abitudine alla comunicazione di frontiera.
