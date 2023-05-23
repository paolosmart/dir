import socket
import pandas as pd
import tkinter as tk
import os
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading
import time
import queue

# Funzione per il print del messaggio di errore
def errore(messaggio):
    print(messaggio)
    exit(0)

# Funzione per la connessione e la ricezione del feed
def datafeed(selected_list, data_queue):
    sfeed = ""
    porta = 10005
    buffersize = 256
    # Unisci i titoli in una stringa separata da virgole
    titoli = ",".join(selected_list)
    comando = f"SUBPRZALL {titoli}\n"
    host = "127.0.0.1"

    # Creo il socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Errore nella creazione del socket: %s" % err)
        exit()
    # Connessione al server
    try:
        print(titoli)
        s.connect((host, porta))
    except socket.error as err:
        print("Errore nella connessione al server: %s" % err)
        exit()
    # Invio del comando
    comando = comando.encode()
    s.send(comando)

    while True:
        dati = s.recv(buffersize)  # Ricezione dei dati
        decoded_data = dati.decode()  # Decodifica dei dati
        #print(decoded_data)  # Decodifica dei dati
        # Filtra solo i messaggi di tipo "BIDASK"
        if decoded_data.startswith("BIDASK"):
           _, ticker, time, _, _,bid, _, _, ask, *_ = decoded_data.split(";")
           row = {'Ticker': ticker, 'Bid': bid, 'Ask': ask, 'Time': time}
           data_queue.put(row)  # Add the row to the queue


    # Chiusura del socket
    s.close()


class RealTimeTable(tk.Frame):
    def __init__(self, parent, columns, data_queue):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.columns = columns
        self.data_queue = data_queue  # Store data_queue as an instance variable
        self.ticker_item_ids = {}  # Dictionary to map tickers to item IDs

        # Creazione della tabella
        self.table = ttk.Treeview(self, columns=self.columns, show='headings')
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Creazione degli header della tabella
        for col in self.columns:
            self.table.heading(col, text=col)

        # Avvio del thread per l'aggiornamento dei dati
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_data(self):
        while True:
            # Get all rows from the queue and update the table
            while not self.data_queue.empty():
                row = self.data_queue.get()
                ticker = row['Ticker']
                if ticker in self.ticker_item_ids:
                    # Update the existing row with the new data
                    self.table.item(self.ticker_item_ids[ticker], values=list(row.values()))
                else:
                    # Insert a new row and store the item ID in the dictionary
                    item_id = self.table.insert('', tk.END, values=list(row.values()))
                    self.ticker_item_ids[ticker] = item_id

            # Aggiornamento della tabella ogni secondo
            time.sleep(0.01)



class AppDir:
    def __init__(self, root):
        self.root = root
        self.root.title('Seleziona Lista Titoli')

        # Ottieni un elenco dei file nella directory corrente
        self.files = os.listdir('.')

        # Filtra l'elenco per includere solo i file che terminano con '.txt'
        self.list_files = [file for file in self.files if file.endswith('.txt')]

        # Se non ci sono file di lista, mostra un messaggio di errore
        if not self.list_files:
            messagebox.showinfo("Errore", "Non ci sono file di lista disponibili.")
            return

        # Crea il menu a tendina
        self.selected_file = tk.StringVar(self.root)
        self.selected_file.set(self.list_files[0])  # imposta l'opzione predefinita
        self.dropdown = tk.OptionMenu(self.root, self.selected_file, *self.list_files, command=self.seleziona_lista)
        self.dropdown.pack()

        # Crea il bottone per confermare la selezione
        self.conferma_button = tk.Button(root, text="Conferma", command=self.conferma_selezione)
        self.conferma_button.pack()

    def seleziona_lista(self, file_name):
        self.selected_file.set(file_name)

    def conferma_selezione(self):
        selected_file = self.selected_file.get()
        messagebox.showinfo("Successo", f"File '{selected_file}' selezionato con successo!")
        self.root.destroy()  # Chiudi la finestra

        # Leggi il file selezionato e estrai i titoli
        with open(selected_file, 'r') as file:
            selected_list = file.read().splitlines()

        # Passa la lista di titoli alla funzione datafeed
        data_queue = queue.Queue()
        data_thread = threading.Thread(target=datafeed, args=(selected_list, data_queue))
        data_thread.start()


        # Creazione della finestra principale dell'applicazione
        main_window = tk.Tk()
        main_window.title('Real-Time Data')

        # Creazione della tabella in tempo reale
        table = RealTimeTable(main_window, ['Ticker', 'Bid', 'Ask', 'Time'], data_queue)  # Pass data_queue instead of df and data_lock
        table.pack()  # Pack the table into the main_window

        # Avvio dell'interfaccia grafica principale
        main_window.mainloop()



AppDir(tk.Tk()).root.mainloop()
