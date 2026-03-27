# Parser Module - Checklist

## Obiettivo
Parser per vocaboli e gestione database SQLite.

## Task
- [ ] Creare db_builder.py per parsing vocaboli
- [ ] Definire schema SQLite (Concepts, Translations, UserMemory)
- [ ] Gestione sinonimie multiple (split /)
- [ ] Testare parser con dati mock
- [ ] Popolare database con prime 100 parole

## Criteri di Verifica
- Database SQLite creato con schema corretto
- Parser gestisce correttamente file google-10000-english.txt
- Sinonimie multiple salvate come righe separate
- Test automatici passano