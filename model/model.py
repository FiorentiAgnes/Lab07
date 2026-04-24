import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._migliore = []
        self._costo_minimo = float('inf')
        self._situazioni_mese = []

    def GetAllSituazioni(self):
        return MeteoDao.get_all_situazioni()

    def GetUmiditaMedia(self, mese):
        return MeteoDao.get_umidita_media(mese)

    def calcola_sequenza(self, mese):
        # Inizializzazione
        self._situazioni_mese = MeteoDao.get_calcola_sequenza(mese)
        self._migliore = []
        self._costo_minimo = float('inf')

        # Avvio ricorsione
        self._ricorsione([], 0)
        return self._migliore, self._costo_minimo

    def _ricorsione(self, parziale, livello):
        # A: Condizione Terminale (Giorno 15 raggiunto) 
        if livello == 15:
            costo = self._calcola_costo(parziale)
            if costo < self._costo_minimo:
                self._costo_minimo = costo
                self._migliore =copy.deepcopy(parziale)
            return

        # B: Loop sulle 3 città 
        for citta in ["Genova", "Milano", "Torino"]:
            if self._is_valida(parziale, citta):  # C: Filtro 
                parziale.append(citta)
                self._ricorsione(parziale, livello + 1)  # D: Ricorsione 
                parziale.pop()  # E: Backtracking 

    def _is_valida(self, parziale, prossima_citta):
        # Vincolo 1: Massimo 6 giorni totali per città
        giorni_totali = sum(1 for c in parziale if c == prossima_citta)
        if giorni_totali >= 6:
            return False

        # Se è il primo giorno, ogni città è valida
        if len(parziale) == 0:
            return True

        # Vincolo 2: Minimo 3 giorni consecutivi
        ultima_citta = parziale[-1]

        if prossima_citta != ultima_citta:
            # Se voglio cambiare città, devo aver passato almeno 3 giorni nell'ultima
            # Controllo se la lunghezza della sequenza dell'ultima città è < 3
            contatore_ultime = 0
            for i in range(len(parziale) - 1, -1, -1):
                if parziale[i] == ultima_citta:
                    contatore_ultime += 1
                else:
                    break
            if contatore_ultime < 3:
                return False
        else:
            # Se voglio restare nella stessa città, non ci sono vincoli minimi (solo i 6 max)
            pass

        return True

    def _calcola_costo(self, sequenza):
        costo = 0
        for i in range(len(sequenza)):
            # 1. Costo variabile: Umidità della città i-esima nel giorno i
            # Cerchiamo nel buffer dei dati DB la situazione corretta
            citta_corrente = sequenza[i]
            umidita = 0
            for s in self._situazioni_mese:
                # s.Data.day == i+1 perché i parte da 0 (giorno 1)
                if s.localita == citta_corrente and s.data.day == (i + 1):
                    umidita = s.umidita
                    break
            costo += umidita

            # 2. Costo fisso: +100 se cambio città
            if i > 0 and sequenza[i] != sequenza[i - 1]:
                costo += 100
        return costo