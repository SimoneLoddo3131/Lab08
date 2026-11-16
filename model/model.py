from database.distributore_DAO import DistributoreDAO


'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()



        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # FATTO


        lista_tupla_medie=[]
        if self._distributori:
            for distributore in self._distributori:
                nome_distr=distributore.nome
                lista_prezzi_distr=distributore.get_prezzi()
        try:

            lista_prezzi_mese = [p.prezzo_litro for p in lista_prezzi_distr if p.data.month==mese]
            media = sum(lista_prezzi_mese)/len(lista_prezzi_mese)
            lista_tupla_medie.append((nome_distr, media ))
        except ZeroDivisionError:
            print("nessun prezzo trovato, la lista è vuota del mese richiesta è vuota")


        return lista_tupla_medie








    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []

        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 0, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno==7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return # da ricontrollare con il debugger

        for distr_id in prezzi_settimana:
            costo_oggi=prezzi_settimana[distr_id][giorno]*100
            if ultimo_distributore is not None and ultimo_distributore != distr_id:
                costo_oggi+=5
            if (costo_oggi + costo_corrente) >= self.__costo_ottimo and self.__costo_ottimo != -1:
                continue
            sequenza_parziale.append(distr_id)
            self.__ricorsione(sequenza_parziale, giorno+1, distr_id, costo_oggi+costo_corrente, prezzi_settimana)

            sequenza_parziale.pop()















    def __get_prezzi_prima_settimana_mese(self, mese: int):

        diz_chiave_id_valore_lista_prezzi=dict()

        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """

        #FATTO (problema nasce se i dati non sono ordinati)
        """prezzi_ordinati = sorted(
            [p for p in lista_prezzi if p.data.month == mese and 1 <= p.data.day <= 7],
            key=lambda p: p.data
        )"""
        for distr in self._distributori:
            lista_prezzi=distr.get_prezzi()
            lista_prezzi_mese=[p.prezzo_litro for p in lista_prezzi if p.data.month==mese]
            diz_chiave_id_valore_lista_prezzi[distr.id]=lista_prezzi_mese[0:7]
        return diz_chiave_id_valore_lista_prezzi

