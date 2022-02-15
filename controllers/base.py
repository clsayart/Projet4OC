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
        # DE QUOI J'AI BESOIN DANS RETURN?? tournoi, serialized_rounds?????
        print("tournoi", tournoi)
        print("serialized_rounds", serialized_rounds)
        ranking_of_round_3 = self.make_round(ranking_of_round_2, players, tournoi, serialized_rounds)
        print("ranking_of_round_3", ranking_of_round_3)



        print("end!")

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
        #d'abord round1 ???
        # result_round = self.generate_rounds()

        # players = tournoi.players

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
        for i in range(1 - tournoi_to_continue[0]):
            print(i)
            print("tournoi object", tournoi_to_continue[1])
            print("tournoi rounds matches", tournoi_to_continue.round[i].matches)
            print("tournoi round", tournoi_to_continue.rounds[i])
            #tournoi = tournoi_to_continue[1]
            #players = tournoi.players
            #serialized_matches_of_round = serialize_match(tournoi_to_continue.round[i].matches???)
            #serialized_rounds = tournoi.rounds
            #serialized_round = saving_round(tournoi_to_continue.rounds[i], serialized_matches_of_round)
            #"ranking_of_round_"+i = self.make_round(ranking_of_round_2, players, tournoi, serialized_rounds)


# PUIS REMETTRE CA ou équivalent ou rien??
# players = self.view_tournoi.final_players_ranking(players)
#         self.view_tournoi.end_tournoi(tournoi, players)
#         serialized_players_tournoi = serialize_player(players)
#         serialized_tournoi = serialize_tournoi(tournoi,
#                                                serialized_players_tournoi,
#                                                serialized_rounds)
# SCRAPE TOURNOI AVANT DE LE REMETTRE? remove
#         insert_tournoi(serialized_tournoi)
#print("end!")


#ANCIENNE FONCTION start_tournoi
        # round_2 = self.generate_rounds()
        # matches_second_round = \
        #     self.view_tournoi.generate_pairs_second_round(ranking)
        # serialized_matches_round_2 = serialize_match(matches_second_round)
        # round_2.heure_fin = str(datetime.datetime.now())
        # round_2.list_matchs.append(matches)
        # serialized_round_two = saving_round(round_2,
        #                                     serialized_matches_round_2)
        # rounds.append(round_2)
        # serialized_rounds.append(serialized_round_two)
        # ranking_round_2 = self.view_tournoi.set_ranking(players)
        # round_3 = self.generate_rounds()
        # matches_third_round = \
        #     self.view_tournoi.generate_pairs_second_round(ranking_round_2)
        # serialized_matches_round_3 = serialize_match(matches_third_round)
        # round_3.heure_fin = str(datetime.datetime.now())
        # round_3.list_matchs.append(matches_third_round)
        # serialized_round_three = saving_round(round_3,
        #                                       serialized_matches_round_3)
        # rounds.append(round_3)
        # serialized_rounds.append(serialized_round_three)
        # ranking_round_3 = self.view_tournoi.set_ranking(players)
        # round_4 = self.generate_rounds()
        # matches_fourth_round = \
        #     self.view_tournoi.generate_pairs(ranking_round_3, ranking_round_2)
        # serialized_matches_round_4 = serialize_match(matches_fourth_round)
        # round_4.heure_fin = str(datetime.datetime.now())
        # round_4.list_matchs.append(matches_fourth_round)
        # serialized_round_four = saving_round(round_4,
        #                                      serialized_matches_round_4)
        # rounds.append(round_4)
        # serialized_rounds.append(serialized_round_four)
        # players = self.view_tournoi.final_players_ranking(players)
        # tournoi = Tournoi(name, lieu, date_tournoi,
        #  controle_temps, description, rounds, players)
        # self.view_tournoi.end_tournoi(tournoi, players)
        # serialized_players_tournoi = serialize_player(players)
        # serialized_tournoi = serialize_tournoi(tournoi,
        # serialized_players_tournoi,
        # serialized_rounds)
        # insert_tournoi(serialized_tournoi)
