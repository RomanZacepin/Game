
import flet as ft

from models import Player, ScoreCollection
from game import MemoryGame
from report import write_report


def main(page: ft.Page):
    player = Player("Student")
    scores = ScoreCollection()

    game = MemoryGame(page, player, scores)
    game.build()

    def on_disconnect(e):
        write_report(player, scores)

    page.on_disconnect = on_disconnect


if __name__ == "__main__":
    ft.run(main)
