import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._grafo= nx.Graph()
        self._listaAlbum = []
        self._listaconnessioni=[]
        self._dictalbum = {}
        self._albumScelto = None  # inizializzo la scelta della dd
        self._migliorsoluzione =[]


    def buildGrafo(self, durata):
        self._grafo.clear()

        #prendo gli albume tramite il dao
        self._listaAlbum = DAO.getAlbumByDurata(durata)

        #mappo gli album per id
        for album in self._listaAlbum:
            self._dictalbum[album.id] = album

        self._grafo.add_nodes_from(self._listaAlbum) #aggiungo i nodi

        self._listaconnessioni = DAO.connessioni(self._dictalbum) #trovo le connessioni dal DAO (gia pronte come se possero due album)
        self._grafo.add_edges_from(self._listaconnessioni)#ggiungo gli archi

    def getconnessa(self, album):
        if album not in self._grafo:
            return []

        return nx.node_connected_component(self._grafo, album) #ritorno la componente connessa

    def getSet(self , album, maxdurata):
        componente=self.getconnessa(album) #calcolo la comp connesa
        self._migliorsoluzione =[]
        parziale =[album] #imposto l'album scleto come inizio



        self.ricorsione(parziale,maxdurata,componente,album.durata) #ricorsione

        return self._migliorsoluzione

    def ricorsione(self, parziale, maxdurata, componente,durataIniziale):
        if len(parziale)>len(self._migliorsoluzione):#massimizzo gli album possibili
            self._migliorsoluzione = parziale

        for album in componente:
            if album in parziale: #se l'album è gia in parziale salta al prossimo senza eseguire sotto
                continue
            durata =album.durata + durataIniziale #calcolo la durata
            if durata <= maxdurata:
                parziale.append(album)# se la durata è minore , appendo e riccrro ancora
                self.ricorsione(parziale, maxdurata, componente,durata)








