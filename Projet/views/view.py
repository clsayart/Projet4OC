from Projet.models.match import Match


class TournoiView:
    def prompt_for_tournoi(self):
        name = input("Entrez le nom du Tournoi: ")
        lieu = input("Entrez le lieu du Tournoi: ")
        date_tournoi = input("Entrez la ou les dates du Tournoi: ")
        controle_temps = input("Entrez le type de contrôle de temps pour ce Tournoi (bullet, blitz ou coup rapide): ")
        description = input("Entrez la description du Tournoi: ")
        if not (name, lieu, date_tournoi, controle_temps, description):
            return None
        return name, lieu, date_tournoi, controle_temps, description

    def prompt_for_player(self):
        last_name = input("Entrez le nom de famille du Player: ")
        first_name = input("Entrez le prénom du Player: ")
        date_of_birth = input("Entrez la date de naissance du Player: ")
        sex = input("Entrez le sexe du Player: ")
        if not (last_name, first_name, date_of_birth, sex):
            return None
        print("variables", last_name, first_name, date_of_birth, sex)
        return last_name, first_name, date_of_birth, sex

    def menu(self):
        print("----------Tournoi---------\n")
        print("1. Start Tournoi - Please enter 1")
        print("2. View Rapports - Please enter 2")
        choice = input("please enter your choice: ")
        return choice

    def tournoi_commence(self):
        print("tournoi commencé")
        print("1. Afficher rapports souhaités")
        print("2. Continuer")
        choice_menu = input("please enter your choice: ")
        return choice_menu

    def prompt_for_round(self):
        name_round = input("Entrez le nom du Round: ")
        if not (name_round):
            return None
        return name_round

    def generate_pairs_first_round(self, players):
        players_sorted = sorted(players, key=lambda player: player.rank)
        print("players sorted", players_sorted)
        print("len(players_sorted)",len(players_sorted))
        len_int = int(len(players_sorted) / 2)
        # len_int = len(players_sorted) // 2
        split1 = players_sorted[:len_int]
        split2 = players_sorted[len_int:]
        print("splits", split1[0].first_name, split2)
        pairs = []

        print(len(split1))
        #for i in (0, len(split1) - 1):
        for i in range(4):
            pair = []
            print('split i', split1[i].first_name)
            pair.append(split1[i])
            pair.append(split2[i])
            print("pair1", pair)
            pairs.append(pair)
            print("pairs1", pairs)
        print("pairs", pairs)

        # for element in split1:
        #   pair = [element, split2[split1.index(element)]]
        #  pairs.append(pair)

        matches = list()
        for pair in pairs:
            print("Match " + pair[0].first_name + " " + pair[1].first_name)
            score_player1 = input("Score P1: ")
            score_player2 = input("Score P2: ")
            match = Match(pair[0], pair[1], score_player1, score_player2)
            print("HEERE", pair[0])
            matches.append(match)
        print("matches view", matches)
        return matches

    def set_ranking(self, players):
        ranking = []
        print("Mettez à jour le classement général des joueurs")
        for player in players:
            print("Player " + player.first_name)
            score = input("Score : ")
            ranking.append([player, float(score)])
        sorted_rank = sorted(ranking, key=lambda key_score: key_score[1],
                             reverse=True)
        print("ranking", ranking)
        print('sorted rank', sorted_rank)
        print("Classement des joueurs :")
        i = 1
        for rank in sorted_rank:
            print("Classé " + str(i) + " : " + rank[0].first_name +
                  " avec " + str(rank[1]) + " pts")
            i += 1
        #return ranking
        return sorted_rank


    def generate_pairs_second_round(self, ranking):
        matches = []
        print(ranking[0][0].first_name, ranking[1][0].first_name, ranking[2][0].first_name, ranking[3][0].first_name)
        print(str(ranking[0][0].first_name)
              + ' VS ' + str(ranking[2][0].first_name))
        score_p1 = input("Score P1: ")
        score_p2 = input("Score P2: ")
        print("gen pair 2nd r m 1", ranking[0][0], ranking[2][0], score_p1, score_p2)
        matches.append(Match(ranking[0][0], ranking[2][0], score_p1, score_p2))
        print("matches after first append", matches[0])

        print(str(ranking[1][0].first_name)
              + ' VS ' + str(ranking[3][0].first_name))
        score_p1 = input("Score P1: ")
        score_p2 = input("Score P2: ")
        print("gen pair 2nd r m 2", ranking[1][0], ranking[3][0], score_p1, score_p2)
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
                and previous_ranking[1][0].first_name == ranking[1][0].first_name:
            matches = self.generate_pairs_second_round(ranking)
            return matches
        else:
            matches = []
            print(ranking[0][0].first_name + " Versus " + ranking[1][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[0][0], ranking[1][0], score_p1, score_p2))
            print(ranking[2][0].first_name + " Versus " + ranking[3][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[2][0], ranking[3][0], score_p1, score_p2))
            print(ranking[4][0].first_name + " Versus " + ranking[5][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[4][0], ranking[5][0], score_p1, score_p2))
            print(ranking[6][0].first_name + " Versus " + ranking[7][0].first_name)
            score_p1 = input("Score P1: ")
            score_p2 = input("Score P2: ")
            matches.append(Match(ranking[6][0], ranking[7][0], score_p1, score_p2))
            return matches


    def final_players_ranking(self, players):
        for player in players:
            print("Joueur " + player.first_name)
            rank = input("Entrez le classement final : ")
            player.rank = int(rank)
        return players







