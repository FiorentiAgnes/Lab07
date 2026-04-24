import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese = self._view.dd_mese.value
        #Controllo se non viene selezionato un mese
        if mese is None or mese == "":
            self._view.lst_result.controls.append(ft.Text("Seleziona un mese!"))
            self._view.update_page()
            return
        citta_umidita_media = self._model.GetUmiditaMedia(mese)
        self._view.lst_result.controls.clear()
        for c in citta_umidita_media:
            self._view.lst_result.controls.append(
                ft.Text(
                    f" {c['Localita']}:  {c['Umidita']};"))
        self._view.update_page()



    def handle_sequenza(self, e):
        mese = self._view.dd_mese.value
        if mese is None or mese == "":
            self._view.lst_result.controls.append(ft.Text("Seleziona un mese prima di calcolare la sequenza!"))
            self._view.update_page()
            return

        # Chiamata al metodo di ottimizzazione ricorsiva
        sequenza_ottima, costo_totale = self._model.calcola_sequenza(mese)

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo_totale} ed è:"))

        # Iteriamo sulla sequenza (che contiene i nomi delle città)
        # e mostriamo i dettagli giorno per giorno
        for i, citta in enumerate(sequenza_ottima):
            giorno = i + 1
            # Formattiamo la data come richiesto: [Città 2013-MM-DD]
            # Usiamo zfill(2) per avere sempre due cifre (es. 01, 02...)
            mese_str = str(mese).zfill(2)
            giorno_str = str(giorno).zfill(2)

            # Recuperiamo l'umidità specifica per quel giorno dal model o dai dati salvati
            # (Assumendo che tu voglia mostrare l'umidità nel testo come nell'esempio)
            testo_riga = f"[{citta} 2013-{mese_str}-{giorno_str}]"
            self._view.lst_result.controls.append(ft.Text(testo_riga))

        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

