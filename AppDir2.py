import socket
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os
from tkinter import messagebox, filedialog


# Funzione per printare il messaggio di errore
def errore(messaggio):
   print(messaggio)
   exit(0)

# Funzione per la connessione e la ricezione del feed
def datafeed(selected_list):
   sfeed = ""
   porta = 10005
   buffersize = 256
   # Unisci i titoli in una stringa separata da virgole
   titoli = ",".join(selected_list)
   comando = f"SUBPRZALL {titoli}\n"
   host = "127.0.0.1"
   df = pd.DataFrame(columns=['Bid', 'Ask'])  # DataFrame per conservare i dati

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

   # Ricezione dei dati
   bidask_data = []
   if os.path.isfile('dati.parquet'):
        df = pd.read_parquet('dati.parquet')
   else:
        df = pd.DataFrame(columns=["Ticker", "Time", "QuantBid","p1", "Bid", "QuantAsk", "p2", "Ask"])

   while True:
        dati = s.recv(buffersize) # Ricezione dei dati
        decoded_data = dati.decode() # Decodifica dei dati
        print(decoded_data) # Decodifica dei dati
        # Filtra solo i messaggi di tipo "BIDASK"
        if decoded_data.startswith("BIDASK"):
            bidask_data.append(decoded_data.split(";")[1:])
            print(bidask_data) 
            
        # Converti i dati di tipo "BIDASK" in un dataframe
        new_df = pd.DataFrame(bidask_data, columns=["Ticker", "Time", "QuantBid","p1", "Bid", "QuantAsk", "p2", "Ask"])
        df = pd.concat([df, new_df])
        df.to_parquet("dati.parquet", index=False)


        
        # Chiusura del socket
        #s.close()
        #exit()
   



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
        self.selected_file.set(self.list_files[0]) # imposta l'opzione predefinita  
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
        self.root.destroy() # Chiudi la finestra 

        # Leggi il file selezionato e estrai i titoli
        with open(selected_file, 'r') as file:
            selected_list = file.read().splitlines()

        # Passa la lista di titoli alla funzione datafeed
        datafeed(selected_list)
        



AppDir(tk.Tk()).root.mainloop()
