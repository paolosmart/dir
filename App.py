import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from lista_titoli import ListaTitoli  # Assicurarsi che lista_titoli.py sia nello stesso directory

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestione Lista Titoli')

        # Configura la finestra
        self.root.geometry('800x600+400+300')  # Finestra di dimensione 800x600, centrata
        self.root.configure(bg='black')  # Colore di sfondo nero

        # Ottieni un elenco dei file nella directory corrente
        self.files = os.listdir('.')
    
        # Filtra l'elenco per includere solo i file che terminano con '.txt'
        self.list_files = [file for file in self.files if file.endswith('.txt')]

        # Se non ci sono file di lista, inizia con una lista vuota
        if not self.list_files:
            self.lista = ListaTitoli()
        else:
            # Altrimenti, inizia con il primo file di lista
            self.lista = ListaTitoli(self.list_files[0])
        
        

        # Crea il menu a tendina
        self.selected_file = tk.StringVar(self.root)
        self.selected_file.set(self.lista.file_name)  # imposta l'opzione predefinita
        self.dropdown = tk.OptionMenu(self.root, self.selected_file, *self.list_files, command=self.seleziona_lista)
        self.dropdown.configure(bg='black', fg='white')  # Configura il colore di sfondo e del testo
        self.dropdown.pack()

        # Crea la Listbox per visualizzare i titoli
        self.listbox = tk.Listbox(self.root, bg='black', fg='white')
        self.listbox.pack(fill=tk.BOTH, expand=1)

        # Creazione dei bottoni
        self.aggiungi_bottone = tk.Button(root, text="Aggiungi Titolo", command=self.aggiungi_titolo, bg='black', fg='white')
        self.salva_bottone = tk.Button(root, text="Salva Lista", command=self.salva_lista, bg='black', fg='white')
        self.rimuovi_bottone = tk.Button(root, text="Rimuovi Titolo", command=self.rimuovi_titolo, bg='black', fg='white')
        # Crea il bottone per creare una nuova lista
        self.nuova_lista_button = tk.Button(root, text="Crea nuova lista", command=self.crea_nuova_lista) 
        self.nuova_lista_button.pack() 

        # Posizionamento dei bottoni
        self.aggiungi_bottone.pack(fill=tk.BOTH)
        self.salva_bottone.pack(fill=tk.BOTH)
        self.rimuovi_bottone.pack(fill=tk.BOTH)
        self.nuova_lista_button.pack(fill=tk.BOTH)

    def seleziona_lista(self, file_name):
        self.lista = ListaTitoli(file_name)
        self.aggiorna_elenco()
        messagebox.showinfo("Successo", f"Lista '{file_name}' selezionata con successo!")
    
    def crea_nuova_lista(self):  # crea una nuova lista vuota
        self.lista = ListaTitoli()  # create a new empty list
        self.aggiorna_elenco()  # update the list display
        self.aggiorna_menu()  # update the dropdown menu


    def aggiungi_titolo(self):
        titolo = simpledialog.askstring("Aggiungi Titolo", "Inserisci il titolo da aggiungere:")
        if titolo:
            self.lista.aggiungi_titolo(titolo)
            self.aggiorna_elenco()
            messagebox.showinfo("Successo", f"Titolo '{titolo}' aggiunto con successo!")

    def salva_lista(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text file", "*.txt"),("All Files", "*.*") ))
        if file_path:
            self.lista.salva_lista(file_path)
            self.aggiorna_menu(file_path)
            messagebox.showinfo("Successo", f"Lista salvata come '{file_path}'!")

    def rimuovi_titolo(self):
        titolo = simpledialog.askstring("Rimuovi Titolo", "Inserisci il titolo da rimuovere:")
        if titolo:
            self.lista.rimuovi_titolo(titolo)
            self.aggiorna_elenco()
            messagebox.showinfo("Successo", f"Titolo '{titolo}' rimosso con successo!")

    def aggiorna_elenco(self):
        self.listbox.delete(0, tk.END)  # Rimuove tutti gli elementi esistenti
        for titolo in self.lista.titoli:
            self.listbox.insert(tk.END, titolo)  # Aggiunge ogni titolo alla Listbox

    def aggiorna_menu(self, file_path=None):
        if file_path is not None:
         #    Aggiungi il nuovo file all'elenco dei file
            self.list_files.append(os.path.basename(file_path))
            # Ricrea il menu a tendina con l'elenco dei file aggiornato
            self.dropdown['menu'].delete(0, 'end')
            for file_name in self.list_files:
                self.dropdown['menu'].add_command(label=file_name, command=tk._setit(self.selected_file, file_name, self.seleziona_lista))
    
    def update_option_menu(self):
        menu = self.om["menu"]
        menu.delete(0, "end")
        for string in self.options:
            menu.add_command(label=string, 
                            command=lambda value=string: self.om_variable.set(value))
    


root = tk.Tk()
app = App(root)
root.mainloop()
