import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        try:
            durataMin= int(self._view.txt_durata.value) #devo avere un intero e non stringa
        except ValueError:
            self._view.show_alert("Inserisci un valore non nullo")

        self._model.buildGrafo(durataMin)# il grafo sempre costruito dal model

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"grafo creato: {len(self._model._grafo.nodes)} album , {len(self._model._grafo.edges)} archi"))

        self._view.dd_album.disabled = False
        self._view.pulsante_analisi_comp.disabled = False
        self._view.txt_durata_totale.disabled = False
        self._view.pulsante_set_album.disabled = False

        self.popoladd() #creo una funzione per popolare la dd

        self._view.update()

    def popoladd(self):
        for album in self._model._listaAlbum:
            self._view.dd_album.options.append(ft.dropdown.Option(text=album.title, key=album.id))

        self._view.update()


    def get_selected_album(self, e):
        album_selected = e.control.value #prendo il valore della scelta
        if album_selected is None:
            self._view.show_alert("Non hai selezionato l'album")
        else:
            album =int(album_selected)
            self._model._albumScelto= self._model._dictalbum.get(album)# richiamo l'oggetto dal dizionario



        print(f"Album Scelto: {self._model._albumScelto}")





    def handle_analisi_comp(self, e):
        album= self._model._albumScelto
        durataTot = 0

        compconnessa=self._model.getconnessa(album) #comp connessa nel model
        for album in compconnessa:
            durataTot += album.durata

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione compontente:{len(compconnessa)}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Durata Totale:{durataTot}"))
        self._view.update()


    def handle_get_set_album(self, e):
        album= self._model._albumScelto #prendo l'album scelto
        durataTot = 0
        if not album:
            self._view.show_alert("Non hai selezionato l'album")
        try:
            maxDurata =float(self._view.txt_durata_totale.value)
        except ValueError:
            self._view.show_alert("Inserisci un valore non  nullo")

        migliorSet =self._model.getSet(album, maxDurata) # risolve il model e ritorna il milgior path

        for album in migliorSet: #calcolo durata tot del milgior path
            durataTot += album.durata

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato:{len(migliorSet)} album , {durataTot} minuti"))
        for album in migliorSet:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{album}  ({album.durata} minuti)"))
        self._view.update()

