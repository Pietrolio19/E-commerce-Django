<h1>E-commerce Django</h1>

Il sito presenta un catalogo da in cui è possibile vedere i prodotti in vendita. All'interno del catalogo è possibile filtrare per categoria oppure cercare direttamente un prodotto, i filtri si trovano nella barra in alto insieme a le icone per accedere al carrello e alla zona utente. Dopo aver selezionato di prodotti nella finestra del carrello è possibile eliminare eventuali articoli e procedere al checkout. Nel checkout è necessario selezionare un metodo di pagamento e un indirizzo, confermare e premere "Paga" per completare l'ordine. Nella zona utente sono visibili i dati dell'utente e i suoi ordini. <br>
Il lato manager è accessibile solo dagli "store_manager" che presentano nel modello il campo "is_store_manager==TRUE" dal pulsante "accedi al pannello da manager" nel catalogo. Da qui è possibile cancellare o modificare: ordini, cateogrie e prodotti; le categorie e i prodotti si possono anche creare.

<h3>In caso si voglia testare il lato user è possibile fare una sign up inventando un account oppure usare l'utente fittizio: (Username: Posto, Password: Posto25+), per il lato manager si può usare l'utente fittizio: (Username: store_manager1, Password: storemanager1).</h3>

Per popolare il DB è possibile usare uno dei due metodi:
1. Usare il fixture presente e i seguenti comandi:

2. Usare lo script "populate_db.py" in management/commands tramite i comandi:
