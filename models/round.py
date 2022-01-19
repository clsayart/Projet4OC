
class Round:
    def __init__(self, nom, date, heure_debut, heure_fin='', list_matchs=[]):
        self.nom = nom
        self.date = date
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.list_matchs = list_matchs
