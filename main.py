from views.view import TournoiView
from views.view_rapports import RapportsView
from controllers.base import Controller


def main():
    """deck = Deck()

    active_view = PlayerView()
    passive_views = (active_view, BroadcastView(), InternetStreamingView())
    views = Views(active_view, passive_views)

    checker = CheckerRankAndSuitIndex()

    """
    view_tournoi = TournoiView()
    view_rapports = RapportsView()
    game = Controller(view_tournoi, view_rapports)
    game.run()


if __name__ == "__main__":
    main()
