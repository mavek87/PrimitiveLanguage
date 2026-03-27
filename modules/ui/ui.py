import flet as ft
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.srs_engine.srs_controller import (
    get_due_cards,
    assess_recall,
    get_connection,
)


class LinguaPrimitivaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Lingua Primitiva"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.current_card_index = 0
        self.due_cards = []
        self.show_answer = False

        self.setup_ui()

    def setup_ui(self):
        self.page.clean()

        title = ft.Text(
            "Lingua Primitiva",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        subtitle = ft.Text(
            "Comunicazione di sopravvivenza",
            size=16,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_400,
        )

        review_btn = ft.Button(
            "🎴 Review Cards", width=200, height=50, on_click=self.start_review
        )

        frase_btn = ft.Button(
            "🧩 Costruisci Frasi",
            width=200,
            height=50,
            on_click=self.start_frase_builder,
        )

        stats_btn = ft.Button(
            "📊Statistiche", width=200, height=50, on_click=self.show_stats
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        title,
                        subtitle,
                        ft.Container(height=40),
                        review_btn,
                        frase_btn,
                        stats_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )

    def start_review(self, e):
        self.due_cards = get_due_cards(20)
        self.current_card_index = 0
        self.show_answer = False

        if not self.due_cards:
            self.page.clean()
            self.page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("✓ Tutte le carte sono state reviewate!", size=24),
                            ft.Text(
                                "Torna più tardi per altre sessioni.",
                                size=16,
                                color=ft.Colors.GREY_400,
                            ),
                            ft.Container(height=20),
                            ft.Button("← Torna al Menu", on_click=self.back_to_menu),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                )
            )
        else:
            self.show_card()

    def show_card(self):
        self.page.clean()

        card = self.due_cards[self.current_card_index]

        word_text = ft.Text(
            card["word"].upper(),
            size=48,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        image_container = ft.Container(
            content=ft.Icon("image", size=100, color=ft.Colors.GREY_600),
            width=300,
            height=200,
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
        )

        if card.get("image_url"):
            image_container = ft.Container(
                content=ft.Image(
                    src=card["image_url"],
                    width=300,
                    height=200,
                    fit=ft.ImageFit.COVER,
                    error_container=ft.Icon("broken_image", size=50),
                ),
                border_radius=10,
            )

        translation_text = ft.Text(
            f"→ {card['translation']}",
            size=24,
            color=ft.Colors.GREEN_300 if self.show_answer else ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER,
        )

        progress_text = ft.Text(
            f"Card {self.current_card_index + 1} / {len(self.due_cards)}",
            size=14,
            color=ft.Colors.GREY_500,
        )

        if not self.show_answer:
            show_btn = ft.Button(
                "Mostra Risposta", width=200, on_click=self.reveal_answer
            )

            self.page.add(
                ft.Container(
                    content=ft.Column(
                        [progress_text, image_container, word_text, show_btn],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                )
            )
        else:
            rating_buttons = ft.Row(
                [
                    ft.Button(
                        "Again\n(1)",
                        bgcolor=ft.Colors.RED_700,
                        on_click=lambda _: self.rate_card(1),
                    ),
                    ft.Button(
                        "Hard\n(2)",
                        bgcolor=ft.Colors.ORANGE_700,
                        on_click=lambda _: self.rate_card(2),
                    ),
                    ft.Button(
                        "Good\n(3)",
                        bgcolor=ft.Colors.GREEN_700,
                        on_click=lambda _: self.rate_card(3),
                    ),
                    ft.Button(
                        "Easy\n(4)",
                        bgcolor=ft.Colors.BLUE_700,
                        on_click=lambda _: self.rate_card(4),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )

            self.page.add(
                ft.Container(
                    content=ft.Column(
                        [
                            progress_text,
                            image_container,
                            word_text,
                            translation_text,
                            rating_buttons,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                )
            )

    def reveal_answer(self, e):
        self.show_answer = True
        self.show_card()

    def rate_card(self, rating):
        card = self.due_cards[self.current_card_index]
        assess_recall(card["concept_id"], rating)

        self.current_card_index += 1
        self.show_answer = False

        if self.current_card_index >= len(self.due_cards):
            self.review_complete()
        else:
            self.show_card()

    def review_complete(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "✓ Sessione Completata!", size=32, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            f"Hai reviewato {len(self.due_cards)} carte",
                            size=16,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Container(height=20),
                        ft.Button("← Torna al Menu", on_click=self.back_to_menu),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )

    def start_frase_builder(self, e):
        self.page.clean()

        self.phrase_blocks = [
            {"word": "io", "tier": 1},
            {"word": "tu", "tier": 1},
            {"word": "lui", "tier": 1},
            {"word": "andare", "tier": 2},
            {"word": "mangiare", "tier": 2},
            {"word": "bere", "tier": 2},
            {"word": "casa", "tier": 2},
            {"word": "acqua", "tier": 2},
            {"word": "buono", "tier": 3},
            {"word": "grande", "tier": 3},
        ]
        self.selected_words = []

        title = ft.Text("Costruisci la Frase", size=28, weight=ft.FontWeight.BOLD)

        instruction = ft.Text(
            "Clicca sulle parole per comporre la frase",
            size=14,
            color=ft.Colors.GREY_400,
        )

        self.result_text = ft.Text(
            "Clicca le parole qui sotto...",
            size=18,
            color=ft.Colors.GREY_500,
        )

        self.words_container = ft.Column(
            controls=[],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._update_word_buttons()

        result_label = ft.Text(
            "Frase costruita:",
            size=16,
            color=ft.Colors.GREY_400,
        )

        check_btn = ft.Button("Verifica", on_click=self.check_phrase, width=150)

        clear_btn = ft.Button("Pulisci", on_click=self.clear_phrase, width=150)

        back_btn = ft.Button("← Torna al Menu", on_click=self.back_to_menu)

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        title,
                        instruction,
                        ft.Container(height=20),
                        result_label,
                        ft.Container(height=10),
                        self.result_text,
                        ft.Container(height=30),
                        ft.Text("Parole disponibili:", size=16),
                        ft.Container(height=10),
                        self.words_container,
                        ft.Container(height=20),
                        ft.Row([check_btn, clear_btn], spacing=20),
                        ft.Container(height=20),
                        back_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    run_spacing=5,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )

    def _update_word_buttons(self):
        self.words_container.controls = []
        for block in self.phrase_blocks:
            word = block["word"]
            is_selected = word in self.selected_words

            btn = ft.Button(
                content=ft.Container(
                    content=ft.Text(word, size=16, color=ft.Colors.WHITE),
                    bgcolor=self._get_tier_color(block["tier"])
                    if not is_selected
                    else ft.Colors.GREEN_700,
                    padding=10,
                    border_radius=8,
                ),
                on_click=lambda _, w=word: self._on_word_click(w),
            )
            self.words_container.controls.append(btn)

    def _on_word_click(self, word):
        if word in self.selected_words:
            self.selected_words.remove(word)
        else:
            self.selected_words.append(word)

        phrase = " ".join(self.selected_words)
        if phrase:
            self.result_text.value = phrase
            self.result_text.color = ft.Colors.GREEN_300
        else:
            self.result_text.value = "Clicca le parole qui sotto..."
            self.result_text.color = ft.Colors.GREY_500

        self._update_word_buttons()
        self.page.update()

    def _get_tier_color(self, tier):
        colors = {
            1: ft.Colors.BLUE_700,
            2: ft.Colors.ORANGE_700,
            3: ft.Colors.PURPLE_700,
        }
        return colors.get(tier, ft.Colors.GREY_700)

    def check_phrase(self, e):
        if not self.selected_words:
            self.result_text.value = "Costruisci una frase prima!"
            self.result_text.color = ft.Colors.RED_300
        else:
            self.result_text.value = "Frase: " + " ".join(self.selected_words)
            self.result_text.color = ft.Colors.GREEN_300
        self.page.update()

    def clear_phrase(self, e):
        self.selected_words = []
        self.result_text.value = "Clicca le parole qui sotto..."
        self.result_text.color = ft.Colors.GREY_500
        self._update_word_buttons()
        self.page.update()

    def check_phrase(self, e):
        if not self.selected_words:
            self.result_text.value = "Costruisci una frase prima!"
            self.result_text.color = ft.Colors.RED_300
        else:
            self.result_text.value = "Frase: " + " ".join(self.selected_words)
            self.result_text.color = ft.Colors.GREEN_300
        self.page.update()

    def clear_phrase(self, e):
        self.selected_words = []
        self.result_text.value = ""
        self.page.update()

    def show_stats(self, e):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM UserMemory WHERE due_date <= datetime('now')"
        )
        due_now = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Concepts")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(interval) FROM UserMemory WHERE repetitions > 0")
        avg_interval = cursor.fetchone()[0] or 0

        conn.close()

        self.page.clean()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Statistiche", size=28, weight=ft.FontWeight.BOLD),
                        ft.Container(height=20),
                        ft.Text(f"Carte da revieware: {due_now}", size=18),
                        ft.Text(f"Totale carte: {total}", size=18),
                        ft.Text(
                            f"Intervallo medio: {avg_interval:.1f} giorni", size=18
                        ),
                        ft.Container(height=30),
                        ft.Button("← Torna al Menu", on_click=self.back_to_menu),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )

    def back_to_menu(self, e):
        self.current_card_index = 0
        self.due_cards = []
        self.show_answer = False
        self.setup_ui()
