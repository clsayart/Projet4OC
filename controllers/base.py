from models.round import Round
from models.players import Player
from models.tournoi import Tournoi
from views.view_rapports import serialize_player, insert_players, \
    serialize_match, serialize_tournoi, \
    insert_tournoi, saving_round, saving_players
from time import gmtime, strftime
import datetime


class Controller:
    def __init__(self, view_tournoi, rapports_tournoi, tournoi=None):
        self.tournoi = tournoi
        self.view_tournoi = view_tournoi
        self.rapports_tournoi = rapports_tournoi

    def get_players(self):
        players = []
        while len(players) < 8:
            last_name, first_name, date_of_birth, \
                sex = self.view_tournoi.prompt_for_player()
            if not (last_name, first_name, date_of_birth, sex):
                return "stop"
            player = Player(last_name, first_name, date_of_birth, sex, rank=0)
            players.append(player)
        return players

    def run(self):
        result_menu = self.view_tournoi.menu()
        if result_menu == "1":
            self.start_tournoi()
        else:
            self.rapports_tournoi.print_rapports()

    def generate_rounds(self):
        result_round = self.view_tournoi.prompt_for_round()
        nom = result_round
        date = str(datetime.datetime.now())
        heure_debut = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        round = Round(nom, date, heure_debut, heure_fin='', list_matchs=[])
        return round

    def start_tournoi(self):
        name, lieu, date_tournoi, controle_temps, \
            description = self.view_tournoi.prompt_for_tournoi()
        players = self.get_players()
        serialized_players = saving_players(players)
        print(serialized_players)
        insert_players(serialized_players)
        print('Joueurs bien enregistrés!')
        print("Il est temps de commencer les rounds!")
        result_round = self.generate_rounds()
        matches = self.view_tournoi.generate_pairs_first_round(players)
        serialized_matches_round_1 = serialize_match(matches)
        ranking = self.view_tournoi.set_ranking(players)
        rounds = []
        serialized_rounds = []
        result_round.list_matchs.append(matches)
        result_round.heure_fin = str(datetime.datetime.now())
        serialized_round_one = saving_round(result_round,
                                            serialized_matches_round_1)
        rounds.append(result_round)
        serialized_rounds.append(serialized_round_one)
        round_2 = self.generate_rounds()
        matches_second_round = \
            self.view_tournoi.generate_pairs_second_round(ranking)
        serialized_matches_round_2 = serialize_match(matches_second_round)
        round_2.heure_fin = str(datetime.datetime.now())
        round_2.list_matchs.append(matches)
        serialized_round_two = saving_round(round_2,
                                            serialized_matches_round_2)
        rounds.append(round_2)
        serialized_rounds.append(serialized_round_two)
        ranking_round_2 = self.view_tournoi.set_ranking(players)
        round_3 = self.generate_rounds()
        matches_third_round = \
            self.view_tournoi.generate_pairs_second_round(ranking_round_2)
        serialized_matches_round_3 = serialize_match(matches_third_round)
        round_3.heure_fin = str(datetime.datetime.now())
        round_3.list_matchs.append(matches_third_round)
        serialized_round_three = saving_round(round_3,
                                              serialized_matches_round_3)
        rounds.append(round_3)
        serialized_rounds.append(serialized_round_three)
        ranking_round_3 = self.view_tournoi.set_ranking(players)
        round_4 = self.generate_rounds()
        matches_fourth_round = \
            self.view_tournoi.generate_pairs(ranking_round_3, ranking_round_2)
        serialized_matches_round_4 = serialize_match(matches_fourth_round)
        round_4.heure_fin = str(datetime.datetime.now())
        round_4.list_matchs.append(matches_fourth_round)
        serialized_round_four = saving_round(round_4,
                                             serialized_matches_round_4)
        rounds.append(round_4)
        serialized_rounds.append(serialized_round_four)
        players = self.view_tournoi.final_players_ranking(players)
        tournoi = Tournoi(name, lieu, date_tournoi,
                          controle_temps, description, rounds, players)
        self.view_tournoi.end_tournoi(tournoi, players)
        serialized_players_tournoi = serialize_player(players)
        serialized_tournoi = serialize_tournoi(tournoi,
                                               serialized_players_tournoi,
                                               serialized_rounds)
        insert_tournoi(serialized_tournoi)
        print("end!")

    def players_ranking_updated(self, players, ranking):
        sorted_players = sorted(players,
                                key=lambda k: k['first_name'])
        print('sorted players début', sorted_players)
        sorted_ranking = sorted(ranking,
                                key=lambda k: k[0].first_name)
        print('sorted ranking début', sorted_ranking)
        print(len(sorted_players))
        i = 0
        while i < len(sorted_players) - 1:
            sorted_players.rank = sorted_ranking[1]
        print('sorted players fin', sorted_players)
        return sorted_players
