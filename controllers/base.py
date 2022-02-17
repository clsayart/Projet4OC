from models.round import Round
from models.players import Player
from models.tournoi import Tournoi
from views.view_rapports import serialize_player, insert_players, \
    serialize_match, serialize_tournoi, serialize_tournoi_start, \
    insert_tournoi, saving_round, saving_players, remove_tournoi
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
        elif result_menu == "2":
            self.rapports_tournoi.print_rapports()
        else:
            self.continue_tournoi()

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
        tournoi = Tournoi(name, lieu, date_tournoi,
                          controle_temps, description)
        serialized_tournoi = serialize_tournoi_start(tournoi)
        insert_tournoi(serialized_tournoi)
        players = self.get_players()
        print("players", players)
        serialized_players = saving_players(players)
        # print(serialized_players)
        insert_players(serialized_players)
        print('Joueurs bien enregistrés!')
        print("Il est temps de commencer les rounds!")
        result_round = self.generate_rounds()
        matches = self.view_tournoi.generate_pairs_first_round(players)
        serialized_matches_round_1 = serialize_match(matches)
        ranking_of_round_1 = self.view_tournoi.set_ranking(players)
        print("ranking", ranking_of_round_1)
        rounds = []
        serialized_rounds = []
        result_round.list_matchs.append(matches)
        result_round.heure_fin = str(datetime.datetime.now())
        serialized_round_one = saving_round(result_round,
                                            serialized_matches_round_1)
        rounds.append(result_round)
        serialized_rounds.append(serialized_round_one)
        # UPDATE PLAYERS RANKING
        updated_players = self.update_players_ranking(players, ranking_of_round_1)
        serialized_updated_players = saving_players(updated_players)
        # REMOVE ANCIEN TOURNOI
        remove_tournoi(tournoi.nom)
        # INSERT NOUVEAU TOURNOI
        serialized_tournoi = serialize_tournoi(tournoi,
                                               serialized_updated_players,
                                               serialized_rounds)
        insert_tournoi(serialized_tournoi)
        ranking_of_round_2 = self.make_round(ranking_of_round_1, players, tournoi, serialized_rounds)
        print("ranking_of_round_2", ranking_of_round_2)
        print("tournoi", tournoi)
        print("serialized_rounds", serialized_rounds)
        ranking_of_round_3 = self.make_round(ranking_of_round_2, players, tournoi, serialized_rounds)
        print("ranking_of_round_3", ranking_of_round_3)
        ranking_of_round_4 = self.make_round(ranking_of_round_3, players, tournoi, serialized_rounds)
        print("ranking_of_round_3", ranking_of_round_4)
        print("Tournoi terminé et enregistré!")

    def make_round(self, ranking, players, tournoi, serialized_rounds):
        round = self.generate_rounds()
        matches_of_round = self.view_tournoi.generate_pairs_second_round(ranking)
        serialized_matches_of_round = serialize_match(matches_of_round)
        round.heure_fin = str(datetime.datetime.now())
        round.list_matchs.append(matches_of_round)
        serialized_round = saving_round(round, serialized_matches_of_round)
        #rounds.append(round)
        serialized_rounds.append(serialized_round)
        ranking_of_round = self.view_tournoi.set_ranking(players)
        # UPDATE PLAYERS RANKING
        updated_players_indef = self.update_players_ranking(players, ranking)
        serialized_updated_players_indef = saving_players(updated_players_indef)
        # REMOVE ANCIEN TOURNOI
        remove_tournoi(tournoi.nom)
        # INSERT NOUVEAU TOURNOI
        serialized_tournoi_indef = serialize_tournoi(tournoi,
                                                     serialized_updated_players_indef,
                                                     serialized_rounds)
        insert_tournoi(serialized_tournoi_indef)
        return ranking_of_round

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

    def update_players_ranking(self, players, ranking):
        for player in players:
            for rank in ranking:
                # find player, then update rank
                if rank[0].first_name == player.first_name:
                    player.rank = rank[1]
        return players

    def continue_tournoi(self):
        tournoi_to_continue = self.rapports_tournoi.find_tournoi_to_continue()
        print("tournoi_to_continue_len", tournoi_to_continue)
        print("tournoi_to_continue_rounds", tournoi_to_continue.rounds)
        print("tournoi_to_continue_rounds.len", len(tournoi_to_continue.rounds))
        print("tournoi_to_continue_rounds.type", type(len(tournoi_to_continue.rounds)))

        #if players len = 0 generate players? else players = tournoi_to_continue.players

        # 4 rounds - round + 3 make round - if len(tournoi_to_continue.rounds) == 0
        # tournoi = tournoi_to_continue
        # d'abord round1 ??? if len() < 1 puis for i in 3 else for i in len
        # result_round = self.generate_rounds()
        # players = tournoi.players?
        # matches = self.view_tournoi.generate_pairs_first_round(players)
        # serialized_matches_round_1 = serialize_match(matches)
        # ranking_of_round_1 = self.view_tournoi.set_ranking(players)
        # print("ranking", ranking_of_round_1)
        # rounds = []
        # serialized_rounds = []
        # result_round.list_matchs.append(matches)
        # result_round.heure_fin = str(datetime.datetime.now())
        # serialized_round_one = saving_round(result_round,
        #                                     serialized_matches_round_1)
        # rounds.append(result_round)
        # serialized_rounds.append(serialized_round_one)
        # ranking_of_round_2 = self.make_round(ranking_of_round_1, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_2", ranking_of_round_2)
        # print("tournoi", tournoi)
        # print("serialized_rounds", serialized_rounds)
        # ranking_of_round_3 = self.make_round(ranking_of_round_2, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_3)
        # ranking_of_round_4 = self.make_round(ranking_of_round_3, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_4)



        # 3 rounds - 3 make round - if len() == 1
        # players déjà prévu en haut de la fonction
        # tournoi déjà prévu en haut de la fonction
        # serialized_rounds = []
        # ranking_of_round = self.view_tournoi.set_ranking(players) ????? PREVIOUS RANKING????
        # ranking_of_round_2 = self.make_round(ranking_of_round, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_2", ranking_of_round_2)
        # print("tournoi", tournoi)
        # print("serialized_rounds", serialized_rounds)
        # ranking_of_round_3 = self.make_round(ranking_of_round_2, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_3)
        # ranking_of_round_4 = self.make_round(ranking_of_round_3, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_4)


        # 2 rounds - 2 make round - if len() == 2
        # players déjà prévu en haut de la fonction
        # tournoi déjà prévu en haut de la fonction
        # serialized_rounds = []
        # ranking_of_round_2 = self.view_tournoi.set_ranking(players) ?????? PREVIOUS RANKING????
        # ranking_of_round_3 = self.make_round(ranking_of_round_2, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_3)
        # ranking_of_round_4 = self.make_round(ranking_of_round_3, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_4)


        # 1 round - 1 make round - if len() == 3
        # players déjà prévu en haut de la fonction
        # tournoi déjà prévu en haut de la fonction
        # serialized_rounds = []
        # ranking_of_round_3 = self.view_tournoi.set_ranking(players) ?????? PREVIOUS RANKING????
        # ranking_of_round_4 = self.make_round(ranking_of_round_3, players, tournoi_to_continue, serialized_rounds)
        # print("ranking_of_round_3", ranking_of_round_4)

        print("Tournoi terminé et enregistré!")
        print("i am here")

