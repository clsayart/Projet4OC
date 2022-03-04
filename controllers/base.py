from models.round import Round
from models.players import Player
from models.tournoi import Tournoi
from views.view_rapports import insert_players, \
    serialize_match, serialize_tournoi, serialize_tournoi_start, \
    insert_tournoi, saving_round, saving_players, remove_tournoi, \
    serialize_match_continued, saving_round_continued
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
            last_name, first_name, date_of_birth, sex = \
                self.view_tournoi.prompt_for_player()
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
        name, lieu, date_tournoi, controle_temps, description = \
            self.view_tournoi.prompt_for_tournoi()
        tournoi = Tournoi(name, lieu, date_tournoi,
                          controle_temps, description)
        serialized_tournoi = serialize_tournoi_start(tournoi)
        insert_tournoi(serialized_tournoi)
        players = self.get_players()
        serialized_players = saving_players(players)
        # print(serialized_players)
        insert_players(serialized_players)
        print('Joueurs bien enregistrés!')
        print("Il est temps de commencer les rounds!")
        result_round = self.generate_rounds()
        matches = self.view_tournoi.generate_pairs_first_round(players)
        serialized_matches_round_1 = serialize_match(matches)
        ranking_of_round_1 = self.view_tournoi.set_ranking(players)
        rounds = []
        serialized_rounds = []
        result_round.list_matchs.append(matches)
        result_round.heure_fin = str(datetime.datetime.now())
        serialized_round_one = saving_round(result_round,
                                            serialized_matches_round_1)
        rounds.append(result_round)
        serialized_rounds.append(serialized_round_one)
        # UPDATE PLAYERS RANKING
        updated_players = self.update_players_ranking(players,
                                                      ranking_of_round_1)
        serialized_updated_players = saving_players(updated_players)
        # REMOVE ANCIEN TOURNOI
        remove_tournoi(tournoi.nom)
        # INSERT NOUVEAU TOURNOI
        serialized_tournoi = serialize_tournoi(tournoi,
                                               serialized_updated_players,
                                               serialized_rounds)
        insert_tournoi(serialized_tournoi)
        ranking_of_round_2 = self.make_round_two(ranking_of_round_1,
                                                 players, tournoi,
                                                 serialized_rounds)
        ranking_of_round_3 = self.make_round(ranking_of_round_1,
                                             ranking_of_round_2, players,
                                             tournoi, serialized_rounds)
        self.make_round(ranking_of_round_2, ranking_of_round_3,
                        players, tournoi, serialized_rounds)
        print("Tournoi terminé et enregistré!")

    def make_round(self, ranking, previous_ranking,
                   players, tournoi, serialized_rounds):
        round = self.generate_rounds()
        matches_of_round = self.view_tournoi.generate_pairs(ranking,
                                                            previous_ranking)
        serialized_matches_of_round = serialize_match(matches_of_round)
        round.heure_fin = str(datetime.datetime.now())
        round.list_matchs.append(matches_of_round)
        serialized_round = saving_round(round, serialized_matches_of_round)
        serialized_rounds.append(serialized_round)
        ranking_of_round = self.view_tournoi.set_ranking(players)
        # UPDATE PLAYERS RANKING
        updated_players_indef = \
            self.update_players_ranking(players, ranking_of_round)
        serialized_updated_players_indef = \
            saving_players(updated_players_indef)
        # REMOVE ANCIEN TOURNOI
        remove_tournoi(tournoi.nom)
        # INSERT NOUVEAU TOURNOI
        serialized_tournoi_indef = \
            serialize_tournoi(tournoi,
                              serialized_updated_players_indef,
                              serialized_rounds)
        insert_tournoi(serialized_tournoi_indef)
        return ranking_of_round

    def make_round_two(self, ranking, players, tournoi, serialized_rounds):
        round = self.generate_rounds()
        matches_of_round = \
            self.view_tournoi.generate_pairs_second_round(ranking)
        serialized_matches_of_round = serialize_match(matches_of_round)
        round.heure_fin = str(datetime.datetime.now())
        round.list_matchs.append(matches_of_round)
        serialized_round = saving_round(round, serialized_matches_of_round)
        serialized_rounds.append(serialized_round)
        ranking_of_round = self.view_tournoi.set_ranking(players)
        updated_players_indef = self.update_players_ranking(players,
                                                            ranking_of_round)
        serialized_updated_players_indef = \
            saving_players(updated_players_indef)
        remove_tournoi(tournoi.nom)
        serialized_tournoi_indef = \
            serialize_tournoi(tournoi,
                              serialized_updated_players_indef,
                              serialized_rounds)
        insert_tournoi(serialized_tournoi_indef)
        return ranking_of_round

    def players_ranking_updated(self, players, ranking):
        sorted_players = sorted(players,
                                key=lambda k: k['first_name'])
        sorted_ranking = sorted(ranking,
                                key=lambda k: k[0].first_name)
        i = 0
        while i < len(sorted_players) - 1:
            sorted_players.rank = sorted_ranking[1]
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
        if len(tournoi_to_continue.players) == 0:
            players = self.get_players()
            serialized_players = saving_players(players)
            # print(serialized_players)
            insert_players(serialized_players)
        else:
            players = tournoi_to_continue.players

        serialized_rounds = []
        for round_to_reserialize in tournoi_to_continue.rounds:
            serialized_matches_of_round = \
                serialize_match_continued(round_to_reserialize.list_matchs)
            serialized_round = \
                saving_round_continued(round_to_reserialize,
                                       serialized_matches_of_round)
            serialized_rounds.append(serialized_round)

        if len(tournoi_to_continue.rounds) == 0:
            result_round = self.generate_rounds()
            matches = self.view_tournoi.generate_pairs_first_round(players)
            serialized_matches_round_1 = serialize_match(matches)
            ranking_of_round_1 = self.view_tournoi.set_ranking(players)
            rounds = []
            result_round.list_matchs.append(matches)
            result_round.heure_fin = str(datetime.datetime.now())
            serialized_round_one = saving_round(result_round,
                                                serialized_matches_round_1)
            rounds.append(result_round)
            serialized_rounds.append(serialized_round_one)
            ranking_of_round_2 = \
                self.make_round_two(ranking_of_round_1,
                                    players,
                                    tournoi_to_continue,
                                    serialized_rounds)
            ranking_of_round_3 = \
                self.make_round(ranking_of_round_1,
                                ranking_of_round_2,
                                players,
                                tournoi_to_continue,
                                serialized_rounds)
            self.make_round(ranking_of_round_2,
                            ranking_of_round_3,
                            players,
                            tournoi_to_continue,
                            serialized_rounds)
        elif len(tournoi_to_continue.rounds) == 1:
            ranking_to_continue = []
            for player in players:
                score = player.rank
                ranking_to_continue.append([player, float(score)])
            ranking_of_round_2 = self.make_round_two(ranking_to_continue,
                                                     players,
                                                     tournoi_to_continue,
                                                     serialized_rounds)
            ranking_of_round_3 = self.make_round(ranking_to_continue,
                                                 ranking_of_round_2,
                                                 players, tournoi_to_continue,
                                                 serialized_rounds)
            self.make_round(ranking_of_round_2,
                            ranking_of_round_3, players,
                            tournoi_to_continue, serialized_rounds)
        elif len(tournoi_to_continue.rounds) == 2:
            ranking_to_continue = []
            for player in players:
                score = player.rank
                ranking_to_continue.append([player, float(score)])
            ranking_of_round_2 = ranking_to_continue
            ranking_of_round_3 = self.make_round_two(ranking_of_round_2,
                                                     players,
                                                     tournoi_to_continue,
                                                     serialized_rounds)
            self.make_round(ranking_of_round_2, ranking_of_round_3,
                            players, tournoi_to_continue,
                            serialized_rounds)
        else:
            ranking_to_continue = []
            for player in players:
                score = player.rank
                ranking_to_continue.append([player, float(score)])
            ranking_of_round_3 = ranking_to_continue
            self.make_round_two(ranking_of_round_3, players,
                                tournoi_to_continue, serialized_rounds)
        print("Tournoi terminé et enregistré!")
