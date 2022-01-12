from tinydb import TinyDB, Query

db = TinyDB('db.json')
players_table = db.table('players')
tournois_table = db.table('tournois')
rounds_table = db.table('rounds')
matches_table = db.table('matches')
Q_Player = Query()


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
    print("players tiny db", serialized_players)
    return serialized_players


def serialize_match(matches):
    serialized_matches = []
    for match in matches:
        print("match.player1 first name", match.player1.first_name)
        serialized_match = {
            "player 1": match.player1.first_name,
            "player 2": match.player2.first_name,
            "score player 1": match.score_player1,
            "score player 2": match.score_player2
        }
        serialized_matches.append(serialized_match)
    return serialized_matches


# def serialize_round(rounds):
#     serialized_rounds = []
#     for round in rounds:
#         serialized_round = {
#             "nom du round": round.nom,
#             "date": round.date,
#             "heure de début": round.heure_debut,
#             "heure de fin": round.heure_fin,
#             "liste des matchs": round.list_matchs
#         }
#         serialized_rounds.append(serialized_round)
#     return serialized_rounds

def serialize_round(round, serialized_matches):
    serialized_round = {
            "nom du round": round.nom,
            "date": round.date,
            "heure de début": round.heure_debut,
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


def insert_players(serialized_players):
    # players_table = db.table('players')
    players_table.truncate()  # clear the table first
    players_table.insert_multiple(serialized_players)


def insert_rounds(serialized_round):
    rounds_table.insert(serialized_round)


def insert_tournoi(serialized_tournoi):
    # tournois_table.truncate()  # ?
    tournois_table.insert(serialized_tournoi)


def insert_matches(serialized_matches):
    # tournois_table.truncate()  # ?
    matches_table.insert_multiple(serialized_matches)


# def update():
#retour de la dernière fonction?
#     players_table.update({'rank':26}, Q.Player.first_name == 'x')

