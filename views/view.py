from models.match import Match
from datetime import datetime


class TournoiView:
    def prompt_for_tournoi(self):
        try:
            name = input("Entrez le nom du Tournoi: ")
        except ValueError:
            name = input("Entrez le nom du Tournoi: ")
        try:
            lieu = input("Entrez le lieu du Tournoi: ")
        except ValueError:
            lieu = input("Entrez le lieu du Tournoi: ")
        date_tournoi = \
            str(input('Entrez la date du Tournoi (format: yyyy-mm-dd): '))
        date_variable = False
        while date_variable is False:
            try:
                date_tournoi_formatted = \
                    datetime.strptime(date_tournoi, "%Y-%m-%d")
                date_variable = True
            except ValueError:
                date_tournoi = \
                    str(input('Entrez la date au format = yyyy-mm-dd! Date: '))
        controle_temps = \
            input("Entrez le type de contrôle de temps "
                  "pour ce Tournoi "
                  "(bullet, blitz ou coup rapide): ")
        while controle_temps not in ['bullet', 'blitz', 'coup rapide']:
            controle_temps = \
                input("Entrez le bon type de contrôle de temps: "
                      "bullet, blitz ou coup rapide: ")
        description = input("Entrez la description du Tournoi: ")
        if not (name, lieu,
                str(date_tournoi_formatted),
                controle_temps, description):
            return None
        return \
            name, lieu, \
            str(date_tournoi_formatted), \
            controle_temps, description

    def prompt_for_player(self):
        try:
            last_name = input("Entrez le nom de famille du Player: ")
        except ValueError:
            last_name = input("Entrez le nom de famille du Player: ")
        try:
            first_name = input("Entrez le prénom du Player: ")
        except ValueError:
            first_name = input("Entrez le prénom du Player: ")
        date_of_birth = \
            input("Entrez la date de naissance "
                  "du Player (format: yyyy-mm-dd): ")
        dateOB_variable = False
        while dateOB_variable is False:
            try:
                date_of_birth_formatted = \
                    datetime.strptime(date_of_birth, "%Y-%m-%d")
                dateOB_variable = True
            except ValueError:
                date_of_birth = \
                    str(input('Entrez la date au bon format = '
                              'yyyy-mm-dd! Date: '))

        sex = input("Entrez le sexe du Player: ")
        while sex not in ['F', 'M']:
            sex = input("Entrez F ou M pour le sexe du Player: ")
        if not (last_name, first_name, str(date_of_birth_formatted), sex):
            return None
        return last_name, first_name, str(date_of_birth_formatted), sex

    def menu(self):
        print("----------Tournoi---------\n")
        print("1. Commencer Tournoi - Entrez 1")
        print("2. Voir Rapports - Entrez 2")
        print("3. Continuer précédent Tournoi - Entrez 3")
        choice = input("please enter your choice: ")
        while choice not in ['1', '2', '3']:
            choice = input("Please enter 1, 2, or 3! Choice : ")
        return choice

    def prompt_for_round(self):
        name_round = input("Entrez le nom du Round: ")
        if not (name_round):
            return None
        return name_round

    def generate_pairs_first_round(self, players):
        players_sorted = sorted(players, key=lambda player: player.rank)
        len_int = int(len(players_sorted) / 2)
        split1 = players_sorted[:len_int]
        split2 = players_sorted[len_int:]
        pairs = []

        for i in range(4):
            pair = [split1[i], split2[i]]
            pairs.append(pair)

        matches = list()
        for pair in pairs:
            print("Match " + pair[0].first_name + " " + pair[1].first_name)

            score_player1 = input("Score P1: ")
            while score_player1 not in ['0', '0.5', '1']:
                score_player1 = input("Please enter 0, 0.5, or 1! Score : ")
            score_player2 = input("Score P2: ")
            while score_player2 not in ['0', '0.5', '1']:
                score_player2 = input("Please enter 0, 0.5, or 1! Score : ")
            match = Match(pair[0], pair[1], score_player1, score_player2)
            matches.append(match)
        return matches

    def set_ranking(self, players):
        ranking = []
        print("Mettez à jour le classement général des joueurs")
        for player in players:
            print("Player " + player.first_name)
            score = input("Score : ")
            test_variable = False
            while test_variable is False:
                try:
                    score = float(score)
                    test_variable = True
                except ValueError:
                    score = input("Please enter a number! Score : ")
            ranking.append([player, float(score)])

        sorted_rank = sorted(ranking, key=lambda key_score: key_score[1],
                             reverse=True)
        print("Classement des joueurs :")
        i = 1
        for rank in sorted_rank:
            print("Classé " + str(i) + " : " + rank[0].first_name +
                  " avec " + str(rank[1]) + " pts")
            i += 1

        return sorted_rank

    def generate_pairs_second_round(self, ranking):
        matches = []
        print(str(ranking[0][0].first_name)
              + ' VS ' + str(ranking[2][0].first_name))
        score_p1 = input("Score P1: ")
        score_p2 = input("Score P2: ")
        matches.append(Match(ranking[0][0], ranking[2][0], score_p1, score_p2))

        print(str(ranking[1][0].first_name)
              + ' VS ' + str(ranking[3][0].first_name))
        score_p1 = input("Score P1: ")
        score_p2 = input("Score P2: ")
        matches.append(Match(ranking[1][0], ranking[3][0], score_p1, score_p2))
        print(str(ranking[4][0].first_name)
              + ' VS ' + str(ranking[5][0].first_name))
        score_p1 = input("Score J1: ")
        score_p2 = input("Score J2: ")
        matches.append(Match(ranking[4][0], ranking[5][0], score_p1, score_p2))
        print(str(ranking[6][0].first_name)
              + ' VS ' + str(ranking[7][0].first_name))
        score_p1 = input("Score J1: ")
        score_p2 = input("Score J2: ")
        matches.append(Match(ranking[6][0], ranking[7][0], score_p1, score_p2))
        return matches

    def generate_pairs(self, ranking, previous_ranking):
        if previous_ranking[0][0].first_name == ranking[0][0].first_name \
                and previous_ranking[1][0].first_name == \
                ranking[1][0].first_name:
            matches = self.generate_pairs_second_round(ranking)
            return matches
        else:
            matches = []
            print(ranking[0][0].first_name + " Versus " +
                  ranking[1][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[0][0], ranking[1][0],
                                 score_p1, score_p2))
            print(ranking[2][0].first_name + " Versus " +
                  ranking[3][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[2][0], ranking[3][0],
                                 score_p1, score_p2))
            print(ranking[4][0].first_name + " Versus " +
                  ranking[5][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[4][0], ranking[5][0],
                                 score_p1, score_p2))
            print(ranking[6][0].first_name + " Versus " +
                  ranking[7][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[6][0], ranking[7][0],
                                 score_p1, score_p2))
            return matches

    def end_tournoi(self, tournoi, players):
        print("Terminer ?\n1. Terminer\n2.Modifier classement joueurs")
        text = input("Votre choix : ")
        while text not in ['1', '2']:
            text = input("Please enter 1 or 2! Choice : ")
        if int(text) == 1:
            print("Tournoi Terminé")
            pass
        elif int(text) == 2:
            players = self.final_players_ranking(players)
            tournoi.players = players
            print("Tournoi Terminé")
            pass

    def final_players_ranking(self, players):
        for player in players:
            print("Joueur " + player.first_name)
            rank = input("Entrez le classement final : ")
            test_variable_rank = False
            while test_variable_rank is False:
                try:
                    rank = float(rank)
                    test_variable_rank = True
                except ValueError:
                    rank = input("Please enter a number! Score : ")
            player.rank = int(rank)
        return players
