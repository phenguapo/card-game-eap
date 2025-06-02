# deck.py

import random
from typing import Literal, Tuple, List, Optional

Action = Literal[
    "play_again",             # ο ίδιος παίκτης παίζει ξανά
    "skip_next",              # ο επόμενος παίκτης χάνει σειρά
    "allow_third",            # Q+K ανιχνεύτηκε ⇒ αναμονή για τρίτη κάρτα
    "third_match_close_all",  # η τρίτη κάρτα ταυτίστηκε με Q/K ⇒ κλείσιμο και των τριών, κατανομή πόντων
    "none",                   # καμία ειδική ενέργεια
]

def points_for_value(val: int) -> int:
    """
    Επιστρέφει την τιμή-πόντο μιας κάρτας:
      Άσσος (1) → 1 πόντος,
      2–10 → η αριθμητική τιμή,
      J(11), Q(12), K(13) → 10 πόντοι.
    """
    if val == 1:
        return 1
    if val in (11, 12, 13):
        return 10
    return val


class Card:
    def __init__(self, value: int, suit: str):
        self.value = value            # τιμή 1–13
        self.suit = suit              # χρώμα: “clubs”, “diamonds”, “hearts”, “spades”
        self.is_open = False          # σημειώνει εάν η κάρτα είναι ανοιχτή
        self.is_matched = False       # σημειώνει εάν η κάρτα έχει ταυτοποιηθεί

    def __str__(self):
        return f"{self.value}_of_{self.suit}.png"


class DeckManager:
    def __init__(self):
        self.board: List[List[Optional[Card]]] = []       # 2D πίνακας κάρτας
        self.history: List[Tuple[int,int]] = []           # ιστορικό τελευταίων ανοιγμένων μη-ταυτοποιημένων (max 5)
        self.selected_cards: List[Tuple[int,int]] = []    # coords των τρεχόντων ανοιγμένων φύλλων
        self.suits = ["clubs", "diamonds", "hearts", "spades"]
        self.values = list(range(1, 14))  # 1..13
        self.allow_third = False
        self.qk_pair: List[Tuple[int,int]] = []           # όταν Q+K ανοίγουν, αποθηκεύουμε coords εδώ

    def remaining_unmatched(self) -> int:
        """Επιστρέφει πόσες κάρτες δεν έχουν ταυτοποιηθεί ακόμη."""
        return sum(
            1 for row in self.board for card in row if card and not card.is_matched
        )

    def is_game_over(self) -> bool: # Αμυντικός μηχανισμός
        """Το παιχνίδι τελειώνει αν υπάρχουν 0 ή 1 μη-ταυτοποιημένες κάρτες."""
        return self.remaining_unmatched() <= 1

    def _fill_board(self, rows: int, cols: int, deck: List[Card]):
        """
        Σχηματίζει το 2D πίνακα self.board από τη λίστα deck,
        γράφοντας κάρτες row×cols διαστάσεων.
        """
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
        """
        Δημιουργεί νέο board (πίνακα καρτών) ανάλογα με το επίπεδο δυσκολίας:
          - “easy”: 4×4, μόνο τιμές {10,11,12,13}
          - “medium”: 4×10, τιμές 1–10
          - “hard”: 4×13, τιμές 1–13
        Κάθε τιμή εμφανίζεται ακριβώς δύο φορές (game memory).
        """
        diff = difficulty.strip().lower()
        if diff == "easy":
            rows, cols = 4, 4
            allowed_values = [10, 11, 12, 13]
        elif diff == "medium":
            rows, cols = 4, 10
            deck = [Card(v, s) for v in range(1, 11) for s in self.suits]
            random.shuffle(deck)
            self._fill_board(rows, cols, deck)
            return
        elif diff == "hard":
            rows, cols = 4, 13
            allowed_values = self.values
        else:
            raise ValueError("Invalid difficulty level")

        total_cards = rows * cols
        deck: List[Card] = []
        suit_pool = {v: self.suits.copy() for v in allowed_values}

        while len(deck) < total_cards:
            viable = [v for v, suits in suit_pool.items() if len(suits) >= 2]
            if not viable:
                raise RuntimeError("Δεν υπάρχουν αρκετά διαθέσιμα ζεύγη φυλών!")
            val = random.choice(viable)
            s1, s2 = random.sample(suit_pool[val], 2)
            suit_pool[val].remove(s1)
            suit_pool[val].remove(s2)
            deck.append(Card(val, s1))
            deck.append(Card(val, s2))

        random.shuffle(deck)
        self._fill_board(rows, cols, deck)

    def select_card(self, row: int, col: int) -> bool:
        """
        Προσπαθεί να ανοίξει την κάρτα στη θέση (row, col). Επιστρέφει True
        αν τώρα έχουμε “αρκετές” κάρτες για να καλέσουμε check_match():
          • Αν allow_third == False, ανοίγονται 2 κάρτες, μετά check_match().
          • Αν allow_third == True (υπήρξε Q+K), ανοίγει ακριβώς 1 ακόμη (τρίτη), μετά check_match().
        Αν η κάρτα είναι ήδη ανοιχτή ή ταυτοποιημένη ή εκτός πινάκων, επιστρέφει False.
        """
        if (
            row < 0 or row >= len(self.board)
            or col < 0 or col >= len(self.board[0])
            or self.board[row][col] is None
            or self.board[row][col].is_open
            or self.board[row][col].is_matched
        ):
            return False

        card = self.board[row][col]
        card.is_open = True
        self.selected_cards.append((row, col))
        self.update_history(row, col)

        needed = 1 if self.allow_third else 2
        return len(self.selected_cards) == needed

    def check_match(self) -> tuple[bool, int, Action]:
        """
        Επιστρέφει (matched, points, action):
          matched: True αν βρέθηκε ταίρι / ειδική περίπτωση
          points: κερδισμένοι πόντοι (0 αν allow_third ή no-match)
          action: “play_again”, “skip_next”, “allow_third”, “third_match_close_all”, ή “none”
        """

        # --- Επεξεργασία όταν allow_third == True (υπήρξε Q+K προηγουμένως) ---
        if self.allow_third:
            (r3, c3) = self.selected_cards.pop()
            third = self.board[r3][c3]
            self.allow_third = False

            # Τα αρχικά coords του Q+K είναι στην self.qk_pair
            original_coords = self.qk_pair.copy()
            self.qk_pair.clear()

            matched_initial = None
            unmatched_initial = None
            for (ri, ci) in original_coords:
                if self.board[ri][ci].value == third.value:
                    matched_initial = (ri, ci)
                else:
                    unmatched_initial = (ri, ci)

            # Αν η τρίτη είναι Q (12) ή K (13) και ταιριάζει με ένα από τα αρχικά
            if matched_initial and third.value in (12, 13):
                third.is_matched = True
                mi_r, mi_c = matched_initial
                self.board[mi_r][mi_c].is_matched = True

                if unmatched_initial:
                    ui_r, ui_c = unmatched_initial
                    self.board[ui_r][ui_c].is_open = False

                self.selected_cards = [unmatched_initial] if unmatched_initial else []

                # Καθαρίζουμε το history από τυποποιημένες κάρτες
                self._purge_matched_from_history()

                pts = points_for_value(third.value) * 2
                return True, pts, "third_match_close_all"

            to_close = [(r3, c3)] + original_coords
            for (r, c) in to_close:
                self.board[r][c].is_open = False

            self.selected_cards = to_close[:]
            return False, 0, "none"

        if len(self.selected_cards) != 2:
            return False, 0, "none"

        (r1, c1), (r2, c2) = self.selected_cards
        card1 = self.board[r1][c1]
        card2 = self.board[r2][c2]


        if card1.value == 13 and card2.value == 12:
            self.qk_pair = [(r1, c1), (r2, c2)]
            self.selected_cards.clear()
            self.allow_third = True
            return True, 0, "allow_third"

        if card1.value != card2.value:
            return False, 0, "none"

        card1.is_matched = True
        card2.is_matched = True
        self.selected_cards.clear()
        self._purge_matched_from_history()

        pts = points_for_value(card1.value) * 2

        # J+J ⇒ ο ίδιος παίκτης ξαναπαίζει
        if card1.value == 11:
            return True, pts, "play_again"
        # K+K ⇒ ο επόμενος χάνει σειρά
        if card1.value == 13:
            return True, pts, "skip_next"
        # Κανονικό ταίριασμα
        return True, pts, "none"

    def close_all(self):
        """Κλείνει όλες τις μη-ταυτοποιημένες κάρτες."""
        for row in self.board:
            for card in row:
                if card and not card.is_matched:
                    card.is_open = False

    def update_history(self, row: int, col: int):
        """
        Κρατά έως και τις 5 πιο πρόσφατες συντεταγμένες άνοιγματος κάρτας που ΔΕΝ
        έχουν ταυτοποιηθεί. Αν η συντεταγμένη υπάρχει ήδη, αφαιρείται και επανατοποθετείται στο τέλος.
        """
        if (row, col) in self.history:
            self.history.remove((row, col))
        self.history.append((row, col))
        if len(self.history) > 5:
            self.history.pop(0)

    def _purge_matched_from_history(self):
        """Αφαιρεί από το history οποιεσδήποτε συντεταγμένες καρτών που ήδη ταυτοποιήθηκαν."""
        self.history = [
            (r, c) for (r, c) in self.history
            if not self.board[r][c].is_matched
        ]

    def save_to_dict(self):
        """Μετατρέπει την κατάσταση του ταμπλό σε λεξικό για αποθήκευση."""
        board_data = []
        for row in self.board:
            row_data = []
            for card in row:
                if card is None:
                    row_data.append(None)
                else:
                    row_data.append({
                        "value": card.value,
                        "suit":  card.suit,
                        "is_matched": card.is_matched,
                        "is_open": card.is_open,
                    })
            board_data.append(row_data)
        return {"board": board_data}

    def load_from_dict(self, data):
        """Φορτώνει αποθηκευμένη κατάσταση ταμπλό από λεξικό (Resume Game)."""
        self.board = []
        for row_data in data["board"]:
            row: List[Optional[Card]] = []
            for cell in row_data:
                if cell is None:
                    row.append(None)
                else:
                    c = Card(cell["value"], cell["suit"])
                    c.is_matched = cell["is_matched"]
                    c.is_open    = cell.get("is_open", False)
                    row.append(c)
            self.board.append(row)
        self.history.clear()
        self.selected_cards.clear()
        self.allow_third = False
        self.qk_pair.clear()
