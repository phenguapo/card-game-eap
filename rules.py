# rules.py
import random
import players
import deck

# Επιστρέφει True αν το παιχνίδι έχει τελειώσει
def is_game_over():
    return deck.remaining_cards() == 0


# Ενέργεια παίκτη
def player_turn(current_player):
    print(f"{current_player['name']} παίζει τώρα...")

    # Επιλογή δύο καρτών
    card1, card2 = deck.pick_two_cards()

    print(f"Επέλεξε: {card1} και {card2}")

    # Έλεγχος ισότητας
    if card1["value"] == card2["value"]:
        print("Ταιριάζουν! +1 ζεύγος")

        # Υπολογισμός πόντων
        if card1["value"] in ["J", "Q", "K"]:
            points = 10
        else:
            points = int(card1["value"])
        players.add_points(current_player, points * 2)

        # Ειδικοί κανόνες
        if card1["value"] == "J":
            return "replay_2_cards"
        elif card1["value"] in ["Q", "K"]:
            return "replay_1_card"
        elif card1["value"] == "K":
            return "skip_next"
    else:
        # Μη ταίριασμα -> επανατοποθέτηση
        deck.return_cards(card1, card2)
    return "normal"


# Ενέργεια υπολογιστή
def computer_turn():
    print("Ο υπολογιστής σκέφτεται...")

    history = deck.get_history()
    board = deck.get_visible_cards()

    for card in board:
        if any(c["value"] == card["value"] for c in history):
            match_card = deck.find_match_in_board(card)
            if match_card:
                print(f"Ο Υπολογιστής βρήκε ζευγάρι: {card} και {match_card}")
                players.add_points(players.get_current_player(), 10)
                deck.remove_cards(card, match_card)
                return "replay_2_cards"

    # Δεν βρήκε από ιστορικό => διαλέγει 2 τυχαίες
    card1, card2 = deck.pick_two_cards()
    if card1["value"] == card2["value"]:
        print(f"Ο Υπολογιστής βρήκε: {card1} και {card2}")
        points = 10 if card1["value"] in ["J", "Q", "K"] else int(card1["value"])
        players.add_points(players.get_current_player(), points * 2)
        return "replay_2_cards"
    else:
        deck.return_cards(card1, card2)
    return "normal"


# Επαναφορά κατάστασης από save
def load_from_save(data):
    deck.load_from_save(data["deck_state"])
