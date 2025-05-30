import random


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
        self.history = []
        self.selected_cards = []
        self.suits = ["clubs", "diamonds", "hearts", "spades"]
        self.values = list(range(2, 15))  # 2-10, 11: J, 12: Q, 13: K, 14: Ace

    def create_board(self, difficulty):
        difficulty = difficulty.strip().lower()
        if difficulty == "easy":
            rows, cols = 2, 8
            allowed_values = [10, 11, 12, 13]  # Μόνο 10 και φιγούρες
        elif difficulty == "medium":
            rows, cols = 4, 10
            allowed_values = list(range(2, 11))  # 2 έως 10
        elif difficulty == "hard":
            rows, cols = 4, 13
            allowed_values = self.values  # Πλήρης τράπουλα
        else:
            raise ValueError("Invalid difficulty level!")

        total_cards = rows * cols
        pairs_needed = total_cards // 2

        # Δημιουργούμε όλα τα δυνατά μοναδικά φύλλα (value, suit)
        full_unique_cards = [
            (value, suit) for value in allowed_values for suit in self.suits
        ]

        # Τσεκ αν υπάρχουν αρκετά μοναδικά για τα απαιτούμενα pairs
        if pairs_needed > len(full_unique_cards):
            raise ValueError("Δεν υπάρχουν αρκετά μοναδικά ζευγάρια καρτών για αυτό το επίπεδο.")

        # Επιλογή n μοναδικών φύλλων
        selected_pairs = random.sample(full_unique_cards, pairs_needed)

        # Δημιουργία deck με 2 copies από κάθε ζεύγος
        deck = []
        for value, suit in selected_pairs:
            deck.append(Card(value, suit))
            deck.append(Card(value, suit))

        random.shuffle(deck)

        # Δημιουργία πίνακα καρτών
        self.board = []
        index = 0
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
        self.update_history(card)

        return (
            len(self.selected_cards) == 2
        )  # Επέστρεψε True αν πρέπει να γίνει έλεγχος

    def check_match(self):
        if len(self.selected_cards) != 2:
            return False

        (r1, c1), (r2, c2) = self.selected_cards
        card1 = self.board[r1][c1]
        card2 = self.board[r2][c2]

        # if card1.value == card2.value:
        #     card1.is_matched = True
        #     card2.is_matched = True
        #     self.selected_cards = []
        #     return True
        if card1.value == card2.value and card1.suit == card2.suit:
            card1.is_matched = True
            card2.is_matched = True
            self.selected_cards = []
            return True

        return False  # Δεν αδειάζουμε selected_cards, το GUI θα το κάνει μετά

    # def close_all(self):
    #     for row in self.board:
    #         for card in row:
    #             if card and not card.is_matched:
    #                 card.is_open = False

    def update_history(self, card):
        self.history.append(card)
        if len(self.history) > 5:
            self.history.pop(0)

        # Αφαίρεση καρτών ίδιας αξίας (εκτός της τρέχουσας)
        self.history = [c for c in self.history if c.value != card.value or c == card]

    # def remove_card(self, row, col):
    #     self.board[row][col] = None

    # def reset_card_position(self, row, col):
    #     card = self.board[row][col]
    #     if card and not card.is_matched:
    #         card.is_open = False

    def get_board_size(self):
        return len(self.board), len(self.board[0])

    def is_game_over(self):
        for row in self.board:
            for card in row:
                if card and not card.is_matched:
                    return False
        return True

    # new
    def save_to_dict(self):
        return [
            [
                {
                    "value": card.value,
                    "suit": card.suit,
                    "is_open": card.is_open,
                    "is_matched": card.is_matched,
                }
                if card
                else None
                for card in row
            ]
            for row in self.board
        ]

    # new
    def load_from_dict(self, data):
        self.board = []
        for row_data in data:
            row = []
            for card_data in row_data:
                if card_data:
                    card = Card(card_data["value"], card_data["suit"])
                    card.is_open = card_data["is_open"]
                    card.is_matched = card_data["is_matched"]
                    row.append(card)
                else:
                    row.append(None)
            self.board.append(row)
