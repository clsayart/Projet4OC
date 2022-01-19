class Tournoi:
    def __init__(self, nom, lieu, date_tournoi, controle_temps, description,
                 rounds=[], players=[], nombre_de_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date_tournoi = date_tournoi
        self.nombre_de_tours = nombre_de_tours
        self.rounds = rounds
        self.players = players
        self.controle_temps = controle_temps
        self.description = description
