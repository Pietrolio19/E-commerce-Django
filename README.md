<h1>E-commerce Django</h1>

Il sito presenta un catalogo da in cui è possibile vedere i prodotti in vendita. All'interno del catalogo è possibile filtrare per categoria oppure cercare direttamente un prodotto, i filtri si trovano nella barra in alto insieme a le icone per accedere al carrello e alla zona utente. Dopo aver selezionato di prodotti nella finestra del carrello è possibile eliminare eventuali articoli e procedere al checkout. Nel checkout è necessario selezionare un metodo di pagamento e un indirizzo, confermare e premere "Paga" per completare l'ordine. Nella zona utente sono visibili i dati dell'utente e i suoi ordini. <br>
Il lato manager è accessibile solo dagli "store_manager" che presentano nel modello il campo "is_store_manager==TRUE" dal pulsante "accedi al pannello da manager" nel catalogo. Da qui è possibile cancellare o modificare: ordini, cateogrie e prodotti; le categorie e i prodotti si possono anche creare.

In caso si voglia testare il lato user è possibile fare una sign up inventando un account per l'utente base e per il manager (il campo is_store_manager è modificabile dal form).

<h3>In caso di uso locale eseguire la pull del progetto dal branch local</h3>
Creare un ambiente conda tramite Anaconda Prompt: <br>
conda create -n e-commerce-django python=3.11 <br>
conda activate e-commerce-django <br>
Spostarsi nella cartella del progetto <br>
pip install -r requirements.txt <br>

Prima di eseguire i comandi di seguito risulta necessario generare una SECRET_KEY casuale tramite:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Mettere la SECRET_KEY nel file .env-example

Per popolare il DB usare lo script "populate_db.py" in management/commands tramite i comandi: <br>
    python manage.py migrate <br>
    python manage.py populate.db <br>

python manage.py runserver
