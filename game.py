
import flet as ft
import asyncio
import time

from models import Deck, GameRecord, ScoreCollection
from ui_components import (
    TitleText,
    StatText,
    IconImage,
    CardContainer,
    CardsGrid,
    StatsRow,
    DifficultyRow,
    MenuButton,
    StyledDivider,
    ScoresText,
    WinDialog,
    MainColumn,
)


class MemoryGame:
    ICONS = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FFD700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#C0C0FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#FFD700" stroke="#FFA500" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#FF6B6B" stroke="#FF0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#FFD700" stroke="#FFA500" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#E0E0FF" stroke="#8888CC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#FFD700" stroke="#FFA500" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="#FF6B6B" stroke="#CC0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/></svg>',
    ]

    BACK_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>'
    PI = 3.14159

    def __init__(self, page, player, scores):
        self._page = page
        self._player = player
        self._scores = scores
        self._deck = None
        self._first_card_ui = None
        self._matches = 0
        self._errors = 0
        self._moves = 0
        self._lock = False
        self._game_over = False
        self._start_time = 0
        self._pairs = 6

        self._title = TitleText("Игра Память")
        self._matches_text = StatText("Найдено пар: 0")
        self._errors_text = StatText("Ошибок: 0")
        self._moves_text = StatText("Ходов: 0")
        self._timer_text = StatText("Время: 0:00")
        self._grid_container = ft.Container()
        self._scores_text = ScoresText()

        self._stats_row = StatsRow(
            self._matches_text,
            self._errors_text,
            self._moves_text,
            self._timer_text,
        )

        buttons = [
            MenuButton("Легко (4)", lambda e: self.start_new_game(4)),
            MenuButton("Средне (6)", lambda e: self.start_new_game(6)),
            MenuButton("Сложно (8)", lambda e: self.start_new_game(8)),
        ]
        self._difficulty_row = DifficultyRow(buttons)

        self._layout = MainColumn(
            self._title,
            self._difficulty_row,
            StyledDivider(),
            self._stats_row,
            StyledDivider(),
            self._grid_container,
            StyledDivider(),
            self._scores_text,
        )

    def _update_scores_display(self):
        if len(self._scores) == 0:
            self._scores_text.value = "🏆 Рекордов пока нет"
        else:
            lines = ["🏆 Лучшие результаты:"]
            for r in self._scores.sorted_by_time():
                name = {
                    "4": "Легко",
                    "6": "Средне",
                    "8": "Сложно",
                }.get(r.level, r.level)
                lines.append(
                    f"  {name}: {r.time_sec} сек, {r.moves} ходов"
                )
            self._scores_text.value = "\n".join(lines)

        self._page.update()

    async def _update_timer(self):
        while not self._game_over:
            elapsed = int(time.time() - self._start_time)
            minutes, seconds = divmod(elapsed, 60)
            self._timer_text.value = f"Время: {minutes}:{seconds:02d}"
            self._page.update()
            await asyncio.sleep(1)

    def _check_record(self, elapsed):
        record = GameRecord(
            level=str(self._pairs),
            time_sec=elapsed,
            moves=self._moves,
            errors=self._errors,
        )
        return self._scores.add(record)

    def _show_win_dialog(self):
        elapsed = int(time.time() - self._start_time)
        minutes, seconds = divmod(elapsed, 60)
        is_record = self._check_record(elapsed)

        def play_again(e):
            self._page.pop_dialog()
            self.start_new_game(self._pairs)

        controls = [
            ft.Text(f"Время: {minutes}:{seconds:02d}", size=16),
            ft.Text(f"Ходов: {self._moves}", size=16),
            ft.Text(f"Ошибок: {self._errors}", size=16),
        ]

        if is_record:
            controls.append(
                ft.Text(
                    "🏆 Новый рекорд!",
                    size=14,
                    color=ft.Colors.YELLOW_400,
                )
            )

        dialog = WinDialog(
            title="🎉 Победа!" if not is_record else "🏆 Новый рекорд!",
            content_controls=controls,
            on_play_again=play_again,
        )
        self._page.show_dialog(dialog)

    async def on_card_click(self, e):
        card_ui = e.control
        card = card_ui.card

        if (
            self._lock
            or self._game_over
            or card.revealed
            or card.matched
        ):
            return

        # Переворачиваем карточку и её иконку
        card_ui.content.src = card.value
        card_ui.content.rotate = ft.Rotate(angle=self.PI)
        card_ui.content.update()
        card_ui.rotate = ft.Rotate(angle=self.PI)
        card.open()
        card_ui.bgcolor = ft.Colors.BLUE_200
        card_ui.update()

        if self._first_card_ui is None:
            self._first_card_ui = card_ui
            return

        self._moves += 1
        self._moves_text.value = f"Ходов: {self._moves}"

        self._lock = True
        first_ui = self._first_card_ui
        first_card = first_ui.card

        if first_card == card:
            first_card.match()
            card.match()
            first_ui.bgcolor = ft.Colors.GREEN_300
            card_ui.bgcolor = ft.Colors.GREEN_300
            self._matches += 1
            self._matches_text.value = f"Найдено пар: {self._matches}"
            self._first_card_ui = None

            if self._matches == self._pairs:
                self._game_over = True
                await asyncio.sleep(0.5)
                self._show_win_dialog()
        else:
            self._errors += 1
            self._errors_text.value = f"Ошибок: {self._errors}"
            self._page.update()
            await asyncio.sleep(1)

            first_ui.content.src = self.BACK_ICON
            card_ui.content.src = self.BACK_ICON
            first_ui.content.rotate = ft.Rotate(angle=0)
            card_ui.content.rotate = ft.Rotate(angle=0)
            first_ui.content.update()
            card_ui.content.update()
            first_ui.rotate = ft.Rotate(angle=0)
            card_ui.rotate = ft.Rotate(angle=0)
            first_card.close()
            card.close()
            first_ui.bgcolor = ft.Colors.BLUE_400
            card_ui.bgcolor = ft.Colors.BLUE_400
            self._first_card_ui = None

        self._lock = False
        self._page.update()

    def start_new_game(self, pairs):
        self._pairs = pairs
        self._first_card_ui = None
        self._matches = 0
        self._errors = 0
        self._moves = 0
        self._lock = False
        self._game_over = False
        self._start_time = time.time()

        self._matches_text.value = "Найдено пар: 0"
        self._errors_text.value = "Ошибок: 0"
        self._moves_text.value = "Ходов: 0"
        self._timer_text.value = "Время: 0:00"

        self._deck = Deck(self.ICONS, pairs, self.BACK_ICON)

        grid = CardsGrid()
        for card in self._deck:
            grid.controls.append(
                CardContainer(
                    card,
                    self.on_card_click,
                    self.BACK_ICON,
                )
            )

        self._grid_container.content = grid
        self._update_scores_display()
        self._page.update()
        self._page.run_task(self._update_timer)

    def build(self):
        self._page.title = "Игра Память"
        self._page.padding = 20
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.bgcolor = ft.Colors.GREY_900
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.add(self._layout)
        self._update_scores_display()
        self.start_new_game(6)
