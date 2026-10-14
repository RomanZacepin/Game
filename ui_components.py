
import flet as ft


class TitleText(ft.Text):
    def __init__(self, value):
        super().__init__(
            value,
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        )


class StatText(ft.Text):
    def __init__(self, value, color=ft.Colors.WHITE):
        super().__init__(
            value,
            size=16,
            color=color,
            text_align=ft.TextAlign.CENTER,
        )


class IconImage(ft.Image):
    def __init__(self, src, size=50):
        super().__init__(
            src=src,
            width=size,
            height=size,
            fit=ft.BoxFit.CONTAIN,
        )


class CardContainer(ft.Container):
    def __init__(self, card, on_click_handler, back_icon):
        self._card = card
        super().__init__(
            content=IconImage(back_icon),
            width=90,
            height=90,
            bgcolor=ft.Colors.BLUE_400,
            border_radius=12,
            alignment=ft.Alignment.CENTER,
            on_click=on_click_handler,
            data=card,
            animate_rotation=ft.Animation(
                300, ft.AnimationCurve.EASE_OUT_BACK
            ),
            animate=ft.Animation(
                200, ft.AnimationCurve.EASE_IN_OUT
            ),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=ft.Colors.with_opacity(
                    0.3, ft.Colors.BLACK
                ),
            ),
        )

    @property
    def card(self):
        return self._card


class CardsGrid(ft.GridView):
    def __init__(self):
        super().__init__(
            expand=True,
            max_extent=110,
            spacing=10,
            run_spacing=10,
        )


class StatsRow(ft.Row):
    def __init__(self, *controls):
        super().__init__(
            controls=list(controls),
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )


class DifficultyRow(ft.Row):
    def __init__(self, buttons):
        super().__init__(
            controls=buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )


class MenuButton(ft.Button):
    def __init__(self, label, on_click_handler):
        super().__init__(label, on_click=on_click_handler)


class StyledDivider(ft.Divider):
    def __init__(self):
        super().__init__(color=ft.Colors.GREY_700)


class ScoresText(ft.Text):
    def __init__(self):
        super().__init__(
            "",
            size=14,
            color=ft.Colors.GREY_400,
            text_align=ft.TextAlign.CENTER,
        )


class WinDialog(ft.AlertDialog):
    def __init__(self, title, content_controls, on_play_again):
        super().__init__(
            title=ft.Text(title),
            content=ft.Column(
                content_controls,
                tight=True,
                spacing=8,
            ),
            actions=[
                ft.Button(
                    "Играть снова",
                    on_click=on_play_again,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )


class MainColumn(ft.Column):
    def __init__(self, *controls):
        super().__init__(
            controls=list(controls),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )
