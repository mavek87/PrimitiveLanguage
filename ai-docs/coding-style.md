# Coding Style

## Principi

- **Clean Code** — il codice deve parlare da solo. Se devi spiegare cosa fa, riscrivilo meglio.
- **KISS** — la soluzione più semplice che funziona è la migliore.
- **SOLID** — in particolare Single Responsibility e Dependency Inversion.
- **DRY** — se lo stesso codice appare 2+ volte, estrailo in una funzione comune
- **Separation of Concerns** — non mischiare logica di business con I/O, parsing con validazione, ecc.
## Python

- Nomi significativi: variabili, funzioni, classi e file devono dire cosa fanno. Se il nome è chiaro, il codice si legge da solo.
- **Playbook e Verifiche Numeriche:** Se la direttiva richiede analisi dati, algoritmi complessi o conferme visive/numeriche, crea un playbook interattivo con Marimo (installalo via `uv add marimo` solo se strettamente necessario). Salvalo in puro `.py` e usalo come "verità oggettiva": l'output del playbook deve guidare la tua implementazione e fungere da prova concreta durante la fase di VERIFICA.
- **Usa sempre i type hints**. Ogni funzione ha tipi su parametri e return.
- Un file = una responsabilità chiara. Più funzioni o classi nello stesso file vanno bene se collaborano sulla stessa responsabilità. Se non sono correlate, spezza.
- Usa Protocol (non ABC) per definire contratti/interfacce. Solo quando servono davvero (più di un'implementazione), non per un solo caso.
- Docstring sulle funzioni pubbliche: cosa fa, cosa entra, cosa esce. Commenti inline solo per: edge case, workaround, decisioni non ovvie.
- Commenti: spiegano perchè non cosa. Se hai bisogno di un commento per spiegare 'cosa' allora riscrivi direttamente il codice rendendolo più leggibile.
- Funzioni corte — se supera ~20 righe è indizio che forse fa troppo.
- Guard clauses & Fail Fast — gestisci i casi limite all'inizio della funzione e esci subito. Evita annidamenti profondi di if/else. Se qualcosa non va, fallisci subito con errore chiaro.
- Eccezioni specifiche, cerca di evitare `except Exception` generico — nasconde i bug.
- Cerca di evitare variabili globali — passa tutto tramite parametri.
- Immutabilità dove possibile — preferisci tuple, frozenset, `dataclass(frozen=True)`. Meno bug da stato mutabile.
- Usa `dataclass` o `NamedTuple` per strutture dati, non dizionari anonimi.
- Context manager — usa sempre `with` per risorse (file, connessioni, lock). Mai aprire senza chiudere.
- List comprehension per trasformazioni semplici. Se diventa complessa, meglio un loop esplicito. Leggibilità prima.
- Import espliciti, mai `from modulo import *`.
- Dipendenze minime — non aggiungere librerie per cose che Python fa nativamente.
- Evita liste con tipi misti — una lista contiene un solo tipo di dato.
- Usa il modulo `logging` negli script — aiuta a diagnosticare errori a runtime.
- Usa async/await solo se: più operazioni I/O indipendenti e beneficio reale misurabile. Non usarlo per complessità.
- Non usare librerie esterne solo per convenienza implementativa, ma non reinventare neanche la ruota. Se una libreria è necessaria o estremamente conveniente giustifica la scelta brevemente.

## Design Patterns

Usali quando il problema li richiede naturalmente, non forzarli. KISS prevale sempre. I più utili in Python: Strategy (tramite Protocol), Factory, Repository.

## Test

- **TDD**: scrivi il test prima del codice, dal contratto e dall'ipotesi. Mai dal codice.
- Priorità ai test end-to-end: verifica il comportamento reale, non i dettagli di implementazione.
- Evita mock — preferisci fake objects. Mock accettabile solo per I/O esterno non controllabile (API a pagamento, servizi terzi).
- Random/property-based test quando possibile: scoprono edge case che i test manuali non trovano.
- Testa sempre un comportamento, non giocare con i test.

## Refactoring

Dopo ogni refactoring, rilancia tutti i test (unit + end-to-end). Il refactoring non è completo finché tutti i test sono verdi. Se un test si rompe dopo un refactoring, il refactoring è sbagliato — non il test.

## Ambiente di esecuzione

L'agente opera dentro un container Docker isolato. Lavora sulla cartella `/app`.

**Tool stack:**

- **Python**: usa sempre `uv` (es. `uv run`, `uv add`). NON usare `python3` di sistema.
- **Java**: usa sempre `./gradlew` (JDK 25 nel PATH).
- **JS/TS**: usa `bun` per test e pacchetti.
- **Git**: commit puliti. Utente `ubuntu`.

**Limitazioni:**

- Non accedere a cartelle fuori da `/app`
- Non installare pacchetti via `apt` — le modifiche al container sono volatili. Usa i tool di progetto (`uv add`, `bun add`, `build.gradle`)
- Se `gradlew` dà "Permission Denied" → `chmod +x gradlew`