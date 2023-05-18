#Lo scopo è recuperare tramite Api Directa i dati finanziari in tempo reale.
#L'utente inizialmente dovrà scegliere quale lista titoli usare.
#La lista titoli dovrà essere modificabile e salvata in un file. La lista titoli scelta dall'utente sarà poi una variabile usata
#e passata al comando di sottoscrizione. In questo link puoi trovare  le istruzioni https://app1.directatrading.com/trading-api-directa/index.html.
#Ora ponendo attenzione al formato ed alla posizione dei dati ricevuti dobbiamo salvarli in modo efficente in un file.
#Solo successivamente ci occuperemo di rappresentare i dati in una tabella in tempo reale
#ed grafico in tempo reale dando la possibilità all'utente di scegliere quali dati per la tabella e quali per il grafico. Quindi procediamo per passi.
#Il software deve essere modulare in modo da poter lavorare sui singoli moduli separatamente.Tenendo in considerazione questi concetti procediamo.

#Crea un codice python che si occupi della gestione lista titoli.
import os.path
class ListaTitoli:
    def __init__(self, file_name='lista_titoli.txt'):
        self.file_name = file_name
        if not os.path.isfile(self.file_name):
            open(self.file_name, 'a').close()  # Crea un file vuoto se non esiste
        with open(self.file_name, 'r') as file:
            self.titoli = [line.strip() for line in file.readlines()]


    def aggiungi_titolo(self, titolo):
        if titolo not in self.titoli:
            self.titoli.append(titolo)

    def rimuovi_titolo(self, titolo):
        if titolo in self.titoli:
            self.titoli.remove(titolo)

    def salva_lista(self, file_name=None):
        # Se non viene fornito un nome di file, usa il nome di file esistente
        if file_name is None:
            file_name = self.file_name
        with open(file_name, 'w') as f:
            for titolo in self.titoli:
                f.write(titolo + '\n')


