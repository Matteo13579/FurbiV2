# FurbiOC V2

API Sviluppata per facilitare il controllo degli utenti su OpinionCity
Controlli attuali:
- Telefono casa
- Telefono mobile
- Telefono ufficio

Gli utenti verranno divisi in utenti confermati, in famiglia o in bannati. 
Queste sono categorie interne al sistema, su opinioncity non avranno "peso"

## API
Le funzioni implementate al momento sono per la gestione di:
1. ### Intervistati
   #### Utenti con parco informazioni completo 
   _Funzioni_:
   - Selezione intervistato per id
   - Selezione di tutti gli intervistati
   - Creazione di un intervistato
   - Modifica di un intervistato

2. ### Contatti
    #### Utenti con solamente id e numero di telefono
    _Funzioni_:
    - Selezione contatto per id
    - Selezione di tutti i contatti
    - Creazione di un contatto

3. ### Utenti 
   ### Utenti confermati
    _Funzioni_:
    - Selezione Utente per id
    - Selezione di tutti gli utenti
    - Creazione di un utente

4. ### Ban
   #### Utenti bannati
    _Funzioni_:
    - Selezione bannato per id
    - Selezione di tutti i bannati
    - Creazione di un bannato

5. ### Famiglie 
   #### Utenti etichettati come una famiglia
    _Funzioni_:
    - Selezione famiglia per id della famiglia
    - Selezione famiglia per id dell'intervistato
    - Selezione di tutte le famiglie
    - Creazione di una famiglia
    - Modifica di una famiglia in bannati

6. ### Furbi
   #### Funzioni di controllo per i furbi, tramite conteggio di ricorrenze ed estrapolazione da DB
   _Funzioni_:
   - Selezione dei furbi totali
   - Selezione dei furbi non ancora controllati

7. ### Sito 
   #### Funzioni in test o per test
   
## TO DO
 - [ ] Salvataggio utenti per indirizzo
 - [ ] Aggiornamento utenti per indirizzo
 - [ ] Controllo furbi per indirizzo
 - [ ] Creazione del file JSON contenente i furbi per indirizzo.