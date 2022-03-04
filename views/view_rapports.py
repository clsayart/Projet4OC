from tinydb import TinyDB, Query
from models.players import Player
from models.match import Match
from models.round import Round
from models.tournoi import Tournoi

# with open("storage/db.json", "w+") as file:
db = TinyDB('db.json')
players_table = db.table('players')
players = players_table.all()
tournois_table = db.table('tournois')
tournois = tournois_table.all()
Tournoi_query = Query()


def serialize_player(players):
    serialized_players = []
    for player in players:
        serialized_player = {
            'last_name': player.last_name,
            'first_name': player.first_name,
            'date_of_birth': player.date_of_birth,
            'sex': player.sex,
            'rank': player.rank
        }
        serialized_players.append(serialized_player)
    return serialized_players


def serialize_match(matches):
    serialized_matches = []
    for match in matches:
        serialized_match = {
            "player 1": match.player1.first_name,
            "player 2": match.player2.first_name,
            "score player 1": match.score_player1,
            "score player 2": match.score_player2
        }
        serialized_matches.append(serialized_match)
    return serialized_matches


def serialize_match_continued(matches):
    serialized_matches = []
    for match in matches:
        serialized_match = {
            "player 1": match.player1,
            "player 2": match.player2,
            "score player 1": match.score_player1,
            "score player 2": match.score_player2
        }
        serialized_matches.append(serialized_match)
    return serialized_matches


def serialize_round(round, serialized_matches):
    serialized_round = {
        "nom du round": round.nom,
        "date": round.date,
        "heure de debut": round.heure_debut,
        "heure de fin": round.heure_fin,
        "liste des matchs": serialized_matches
    }
    return serialized_round


def serialize_tournoi(tournoi, serialized_players, serialized_rounds):
    serialized_tournoi = {
        'nom': tournoi.nom,
        'lieu': tournoi.lieu,
        'date_tournoi': tournoi.date_tournoi,
        'rounds': serialized_rounds,
        'players': serialized_players,
        'nombre_de_tours': tournoi.nombre_de_tours,
        'controle_temps': tournoi.controle_temps,
        'description': tournoi.description
    }
    return serialized_tournoi


def serialize_tournoi_start(tournoi):
    serialized_tournoi = {
        'nom': tournoi.nom,
        'lieu': tournoi.lieu,
        'date_tournoi': tournoi.date_tournoi,
        'rounds': tournoi.rounds,
        'players': tournoi.players,
        'nombre_de_tours': tournoi.nombre_de_tours,
        'controle_temps': tournoi.controle_temps,
        'description': tournoi.description
    }
    return serialized_tournoi


def insert_players(serialized_players):
    players_table.insert_multiple(serialized_players)


def remove_tournoi(tournoi_name):
    tournois_table.remove(Tournoi_query.nom == tournoi_name)


def insert_tournoi(serialized_tournoi):
    tournois_table.insert(serialized_tournoi)


def saving_round(round, serialized_matches):
    saving = \
        input("Sauvegarder le round et continuer? "
              "Entrez 1 pour sauvegarder, 2 pour arrêter: ")
    while saving not in ['1', '2']:
        saving = input("Please enter 1 or 2! Choice : ")
    if int(saving) == 1:
        serialized_round = serialize_round(round, serialized_matches)
        pass
    else:
        exit()
    return serialized_round


def saving_round_continued(round, serialized_matches):
    serialized_round = serialize_round(round, serialized_matches)
    return serialized_round


def saving_players(players):
    serialized_players = []
    saving = input("Sauvegarder les joueurs? Entrez 1 pour sauvegarder: ")
    while saving not in ['1']:
        saving = input("Entrez 1 pour sauvegarder: ")
    try:
        if int(saving) == 1:
            serialized_players = serialize_player(players)
            pass
        else:
            pass
    except ValueError:
        saving = input("Entrez 1 pour sauvegarder, s'il vous plait: ")
        if int(saving) == 1:
            serialized_players = serialize_player(players)
            pass
        else:
            pass
    return serialized_players


class RapportsView:

    def print_rapports(self):
        print("----------Rapports---------\n")
        print("1. Liste de tous les joueurs - Entrez 1")
        print("2. Liste de tous les joueurs d'un tournoi - Entrez 2")
        print("3. Liste de tous les tournois - Entrez 3")
        print("4. Liste de tous les rounds d'un tournoi - Entrez 4")
        print("5. Liste de tous les matchs d'un tournoi - Entrez 5")
        choice_rapports = input("votre choix: ")
        while choice_rapports not in ['1', '2', '3', '4', '5']:
            choice_rapports = input("Please enter 1, 2, 3, 4 or 5! Choice : ")
        if int(choice_rapports) == 1:
            self.all_players()
        elif int(choice_rapports) == 2:
            self.list_players_tournoi()
        elif int(choice_rapports) == 3:
            self.list_tournois()
        elif int(choice_rapports) == 4:
            self.list_rounds_tournois()
        elif int(choice_rapports) == 5:
            self.list_matches_tournois()
        # return choice_rapports

    def all_players(self):
        print('players all players', players)
        print("--- Liste des joueurs ---\n")
        print("1. Par classement\n")
        print("2. Par ordre alphabétique\n")
        choice = input("Votre choix : ")
        while choice not in ['1', '2']:
            choice = input("Please enter 1 or 2! Choice : ")

        if int(choice) == 1:
            sorted_players = sorted(players,
                                    key=lambda k: k['rank'])
            for player in sorted_players:
                print('Prenom : ' + str(player['first_name']) + '\n' +
                      'Nom : ' + str(player['last_name']) + '\n' +
                      'Date de naissance : ' + str(player['date_of_birth']) +
                      '\n' +
                      'Sexe : ' + str(player['sex']) + '\n' +
                      'Classement : ' + str(player['rank']) + '\n')
        elif int(choice) == 2:
            sorted_players = sorted(players,
                                    key=lambda k: k['first_name'])
            for player in sorted_players:
                print('Prenom : ' + str(player['first_name']) + '\n' +
                      'Nom : ' + str(player['last_name']) + '\n' +
                      'Date de naissance : ' + str(player['date_of_birth']) +
                      '\n' +
                      'Sexe : ' + str(player['sex']) + '\n' +
                      'Classement : ' + str(player['rank']) + '\n')

    def list_players_tournoi(self):

        print("--- Liste des joueurs par tournoi ---\n")
        choice = input("Entrez le nom du tournoi : ")
        print("1. Par classement\n")
        print("2. Par ordre alphabétique\n")
        second_choice = input("Votre choix : ")
        while second_choice not in ['1', '2']:
            second_choice = input("Please enter 1 or 2! Choice : ")

        for tournoi in tournois:
            if choice == str(tournoi['nom']):
                if int(second_choice) == 1:
                    sorted_players_here = sorted(tournoi['players'],
                                                 key=lambda key: key['rank'])
                    for player in sorted_players_here:
                        print('Prenom : ' + str(player['first_name']) + '\n' +
                              'Nom de Famille : ' + str(player['last_name']) +
                              '\n' +
                              'Date de naissance : ' +
                              str(player['date_of_birth']) + '\n' +
                              'Sexe : ' + str(player['sex']) + '\n' +
                              'Rank : ' + str(player['rank']) + '\n')
                elif int(second_choice) == 2:
                    sorted_players_here = \
                        sorted(tournoi['players'],
                               key=lambda key: key['first_name'])
                    for player in sorted_players_here:
                        print('Prenom : ' + str(player['first_name']) + '\n' +
                              'Nom de Famille : ' +
                              str(player['last_name']) + '\n' +
                              'Date de naissance : ' +
                              str(player['date']) + '\n' +
                              'Sexe : ' + str(player['sex']) + '\n' +
                              'Rank : ' + str(player['rank']) + '\n')

    def list_tournois(self):
        print("--- Liste de tous les tournois ---\n")
        tournoi_index = 1
        for tournoi in tournois:
            print('Tournoi ' + str(tournoi_index) + '\n' +
                  'Nom : ' + str(tournoi['nom']) + '\n' +
                  'Lieu : ' + str(tournoi['lieu']) + '\n' +
                  'Date : ' + str(tournoi['date_tournoi']) + '\n' +
                  'Description: ' + str(tournoi['description']) + '\n\n' +
                  'Liste des Joueurs :')
            player_index = 1
            for player in tournoi['players']:
                print('Player ' + str(player_index) + '\n' +
                      'Prénom : ' + str(player['first_name']) + '\n' +
                      'Nom : ' + str(player['last_name']) + '\n' +
                      'Date de naissance : ' +
                      str(player['date_of_birth']) + '\n' +
                      'Sexe : ' + str(player['sex']) + '\n' +
                      'Rank : ' + str(player['rank']) + '\n')
                player_index += 1
            print('Liste des rounds :')
            round_index = 1
            for round in tournoi['rounds']:
                print('Nom : ' + str(round['nom du round']) + '\n' +
                      'Début : ' + str(round['heure de debut']) + '\n' +
                      'Fin : ' + str(round['heure de fin']) + '\n' +

                      'Liste des matchs :\n')
                match_index = 1
                for match in round['liste des matchs']:
                    print('Match ' + str(match_index) + '\n' +
                          'Player 1 : ' + str(match['player 1']) + '\n' +
                          'Player 2 : ' + str(match['player 2']) + '\n' +
                          'Score 1 : ' + str(match['score player 1']) + '\n' +
                          'Score 2 : ' + str(match['score player 2']) + '\n')
                    match_index += 1
                round_index += 1
            tournoi_index += 1

    def list_rounds_tournois(self):
        print("--- Liste des tours d'un tournoi ---\n")
        choice = input("Entrez le nom du tournoi : ")

        for tournoi in tournois:
            if choice == str(tournoi['nom']):
                print('Liste des tours :')
                round_index = 1
                for round in tournoi['rounds']:
                    print('Nom : ' + str(round['nom du round']) + '\n' +
                          'Début : ' + str(round['heure de debut']) + '\n' +
                          'Fin : ' + str(round['heure de fin']) + '\n' +
                          'Liste des matchs :\n')
                    round_index += 1
                    match_index = 1
                    for match in round['liste des matchs']:
                        print('Match ' + str(match_index) + '\n' +
                              'Player 1 : ' + str(match['player 1']) + '\n' +
                              'Player 2 : ' + str(match['player 2']) + '\n' +
                              'Score 1 : ' +
                              str(match['score player 1']) + '\n' +
                              'Score 2 : ' +
                              str(match['score player 2']) + '\n')
                        match_index += 1

    def list_matches_tournois(self):
        print("--- Liste des matchs d'un tournoi ---\n")
        choice = input("Entrez le nom du tournoi : ")

        for tournoi in tournois:
            if choice == str(tournoi['nom']):
                round_index = 1
                for round in tournoi['rounds']:
                    print('Tour  ' + str(round_index) + '\n')
                    round_index += 1
                    match_index = 1
                    for match in round['liste des matchs']:
                        print('Match ' + str(match_index) + '\n' +
                              'Player 1 : ' + str(match['player 1']) + '\n' +
                              'Player 2 : ' + str(match['player 2']) + '\n' +
                              'Score 1 : ' +
                              str(match['score player 1']) + '\n' +
                              'Score 2 : ' +
                              str(match['score player 2']) + '\n')
                        match_index += 1

    def find_tournoi_to_continue(self):
        choice = \
            input("Entrez le nom du tournoi à reprendre: ")
        for tournoi in tournois:
            if choice == str(tournoi['nom']):
                nom = tournoi['nom']
                lieu = tournoi['lieu']
                date_tournoi = tournoi['date_tournoi']
                nombre_de_tours = tournoi['nombre_de_tours']
                controle_temps = tournoi['controle_temps']
                description = tournoi['description']
                players_continued = []
                rounds_continued = []
                matches_continued = []
                for player in tournoi['players']:
                    first_name = player['first_name']
                    last_name = player['last_name']
                    date_of_birth = player['date_of_birth']
                    sex = player['sex']
                    rank = player['rank']
                    player = Player(last_name,
                                    first_name,
                                    date_of_birth,
                                    sex, rank)
                    players_continued.append(player)
                for round in tournoi['rounds']:
                    nom_round = round['nom du round']
                    date = round['date']
                    heure_debut = round['heure de debut']
                    heure_fin = round['heure de debut']
                    for match in round['liste des matchs']:
                        player1 = match['player 1']
                        player2 = match['player 2']
                        score_player1 = match['score player 1']
                        score_player2 = match['score player 2']
                        match = Match(player1,
                                      player2,
                                      score_player1,
                                      score_player2)
                        matches_continued.append(match)
                    round_continued = Round(nom_round,
                                            date,
                                            heure_debut,
                                            heure_fin,
                                            matches_continued)
                    rounds_continued.append(round_continued)
                tournoi_object = Tournoi(nom, lieu, date_tournoi,
                                         controle_temps,
                                         description,
                                         rounds_continued,
                                         players_continued,
                                         nombre_de_tours)
                print(tournoi_object)
        return tournoi_object
