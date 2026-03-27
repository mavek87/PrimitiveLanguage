---
fonte: Ricerca Web (Principio di Pareto ed Espansione Vocabolario i+1)
data: 2026-03-27
moduli_rilevanti: modules/srs, modules/content_manager
perche_e_qui: Definire teoricamente l'end-game dell'applicazione: come scalare dopo le 1000 parole usando la regola 80/20 e l'ipotesi di Krashen.
changelog:
  - 2026-03-27: Creazione del documento.
---

# L'Espansione del Vocabolario: Dal Principio di Pareto all'Ipotesi "i+1"

## 1. Il Principio di Pareto (80/20) nelle Lingue
Il Principio di Pareto stabilisce che l'80% dei risultati deriva dal 20% delle cause. Nella linguistica, questo si traduce nel fatto che padroneggiare il 20% dei vocaboli (in genere individuato nelle prime 1000-2000 parole dei *Frequency Lists*) garantisce la comprensione di un massiccio 80% delle conversazioni quotidiane. 
- **La Fase "Primitiva":** Le tue 1000 parole di partenza costituiscono esattamente questo vitale 20%. Assicurare quelle significa fornire la "struttura portante" della sopravvivenza (la *Communication Fluency*).

## 2. Il Problema della Transizione: Oltre il Tarzan
Se ci si ferma a 1000 parole base, non c'è crescita reale verso la naturalezza linguistica. L'app non può restare un cantiere "primitivo" in eterno, ma deve fungere da rampa di lancio fluida verso parole più complesse.

## 3. La Soluzione: Ipotesi "i+1" (Comprehensible Input)
Stephen Krashen teorizzò che l'acquisizione della lingua avviene solo quando il discente riceve input linguistico (i) leggermente superiore al suo livello corrente (+1).
Le IA e i sistemi adattivi moderni usano questo principio per l'**espansione fluida del vocabolario**:
- **Introduzione Contestuale:** Una volta padroneggiate le 1000 parole, il sistema introduce nuovi vocaboli (dal vocabolario esteso di 3000-5000 parole) mostrandoli all'interno di frasi composte *esclusivamente* dalle 1000 parole già conosciute dall'utente.
- **Tasso di Novità (5-10%):** Per evitare frustrazione, l'esposizione ideale dovrebbe contenere solo il 5-10% di parole sconosciute.

## Come Implementare l'Espansione nell'App
1. **Tranches Dinamiche:** Il Database non si fermerà a 1000. Supporterà N parole, ordinate per *Global Frequency Index*.
2. **Sistema di Unlock:** L'app utilizzerà lo stato SRS. Quando il mazzo "Primitive Core" (1000 words) raggiunge un livello di maturità globale dell'80% nel cervello dell'utente, l'app "sblocca" silenziosamente pacchetti giornalieri di 5/10 parole nuove, introducendole fluidamente nella rotazione dei ripassi in modo non traumatico.
