import random
from typing import Literal, Tuple, Dict

Action = Literal[
    "play_again",  # ο ίδιος παίκτης ξαναπαίζει
    "skip_next",  # ο επόμενος χάνει σειρά
    "allow_third",  # άνοιγμα 3ης κάρτας (μόνο Q+K)
    "none",
]  # καμιά ειδική ενέργεια

# points_for_value  (Ace = 1)
def points_for_value(val: int) -> int:
    if val == 1:  # Ace
        return 1
    if val in (11, 12, 13):  # J, Q, K
        return 10
    return val  # 2-10


class Card:
    def __init__(self, value, suit):
        self.value = value  # Αριθμητική τιμή (2-14)
        self.suit = suit  # Φύλο (clubs, diamonds, hearts, spades)
        self.is_open = False
        self.is_matched = False

    def __str__(self):
        return f"{self.value}_of_{self.suit}.png"


class DeckManager:
    def __init__(self):
        self.board = []
        self.history: list[tuple[int, int]] = []
        self.selected_cards = []
        self.suits = ["clubs", "diamonds", "hearts", "spades"]
        self.values = list(range(1, 14))
        self.allow_third = False
        self.qk_pair: list[tuple[int, int]] = []  # συντεταγμένες Q+K

    def remaining_unmatched(self) -> int:
        """Πόσα φύλλα δεν έχουν ταυτιστεί ακόμη;"""
        return sum(
            1 for row in self.board for card in row if card and not card.is_matched
        )

    def is_game_over(self) -> bool:
        """Τέλος αν τα αταίριαστα φύλλα είναι 0 **ή** 1."""
        return self.remaining_unmatched() <= 1

    def _fill_board(self, rows: int, cols: int, deck: list):
        self.board, idx = [], 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(deck[idx] if idx < len(deck) else None)
                idx += 1
            self.board.append(row)
        self.history.clear()
        self.selected_cards.clear()

    def create_board(self, difficulty: str):
        difficulty = difficulty.strip().lower()
        if difficulty == "easy":
            rows, cols = 4, 4
            allowed_values = [10, 11, 12, 13]  # 10-J-Q-K

        elif difficulty == "medium":
            rows, cols = 4, 10
            deck = [
                Card(v, s)  # 10 values × 4 suits
                for v in range(1, 11)
                for s in self.suits
            ]
            random.shuffle(deck)
            self._fill_board(rows, cols, deck)
            return

        elif difficulty == "hard":
            rows, cols = 4, 13
            allowed_values = self.values
        else:
            raise ValueError("Invalid difficulty level")

        total_cards = rows * cols

        deck: list[Card] = []
        suit_pool = {v: self.suits.copy() for v in allowed_values}

        while len(deck) < total_cards:
            viable_vals = [v for v, suits in suit_pool.items() if len(suits) >= 2]
            if not viable_vals:
                raise RuntimeError("Δεν υπάρχουν άλλα μοναδικά φύλλα!")

            value = random.choice(viable_vals)
            s1, s2 = random.sample(suit_pool[value], 2)

            suit_pool[value].remove(s1)
            suit_pool[value].remove(s2)

            deck.append(Card(value, s1))
            deck.append(Card(value, s2))

        random.shuffle(deck)

        self.board, index = [], 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(deck[index] if index < len(deck) else None)
                index += 1
            self.board.append(row)

        self.history = []
        self.selected_cards = []

    def select_card(self, row, col):
        if (
            row < 0
            or row >= len(self.board)
            or col < 0
            or col >= len(self.board[0])
            or self.board[row][col] is None
            or self.board[row][col].is_open
            or self.board[row][col].is_matched
        ):
            return False

        card = self.board[row][col]
        card.is_open = True
        self.selected_cards.append((row, col))
        self.update_history(row, col)  # pass coords ✔
        return len(self.selected_cards) == (1 if self.allow_third else 2)

    def check_match(self) -> tuple[bool, int, Action]:
        """
        Επιστρέφει (matched, points, action)
        action: play_again | skip_next | allow_third | none
        """

        if self.allow_third:
            (r, c) = self.selected_cards.pop()  # ακριβώς 1 κάρτα
            third = self.board[r][c]
            self.allow_third = False

            if third.value in (12, 13):  # Q ή K
                third.is_matched = True
                for rc in self.qk_pair:
                    self.board[rc[0]][rc[1]].is_matched = True
                self.qk_pair.clear()
                self._purge_matched_from_history()
                return True, 30, "none"

            self.selected_cards = [(r, c)] + self.qk_pair.copy()
            self.qk_pair.clear()
            return False, 0, "none"

        # κανονικό ζεύγος
        if len(self.selected_cards) != 2:
            return False, 0, "none"

        (r1, c1), (r2, c2) = self.selected_cards
        card1, card2 = self.board[r1][c1], self.board[r2][c2]

        # ειδική περίπτωση Q+K
        if {card1.value, card2.value} == {12, 13}:
            self.qk_pair = [(r1, c1), (r2, c2)]
            self.selected_cards.clear()
            self.allow_third = True
            self.close_all()
            return True, 0, "allow_third"

        # match μόνο αν ίδια value
        if card1.value != card2.value:
            return False, 0, "none"

        # επιτυχία (ίσα φύλλα)
        self.selected_cards.clear()
        card1.is_matched = card2.is_matched = True
        self._purge_matched_from_history()
        pts = points_for_value(card1.value) * 2

        if card1.value == 11:  # J + J
            return True, pts, "play_again"
        if card1.value == 13:  # K + K
            return True, pts, "skip_next"

        return True, pts, "none"

    def close_all(self):
        for row in self.board:
            for card in row:
                if card and not card.is_matched:
                    card.is_open = False

    def update_history(self, row: int, col: int):
        """Κρατά τα 5 πιο πρόσφατα κλειστά/αταίριαστα φύλλα."""
        if (row, col) in self.history:
            self.history.remove((row, col))  # φρεσκάρισμα θέσης
        self.history.append((row, col))
        if len(self.history) > 5:
            self.history.pop(0)

    def _purge_matched_from_history(self) -> None:
        """Remove from history any coordinates whose card is now matched."""
        self.history = [
            (r, c) for (r, c) in self.history if not self.board[r][c].is_matched
        ]

    def save_to_dict(self):
        board_data = []
        for row in self.board:
            row_data = []
            for card in row:
                if card is None:
                    row_data.append(None)
                else:
                    row_data.append(
                        {
                            "value": card.value,
                            "suit": card.suit,
                            "is_matched": card.is_matched,
                            "is_open": card.is_open,  # ★ ΝΕΟ ★
                        }
                    )
            board_data.append(row_data)
        return {"board": board_data}

    def load_from_dict(self, data):
        self.board = []
        for row_data in data["board"]:
            row = []
            for cell in row_data:
                if cell is None:
                    row.append(None)
                else:
                    c = Card(cell["value"], cell["suit"])
                    c.is_matched = cell["is_matched"]
                    c.is_open = cell.get("is_open", False)  # ★
                    row.append(c)
            self.board.append(row)
