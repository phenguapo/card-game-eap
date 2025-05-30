import json
import players

SAVE_FILE = "saved_game.json"


def save_game(deck_manager, current_player, scores):
    data = {
        "deck": deck_manager.save_to_dict(),
        "players": players.save_to_dict(),
        "current_player": current_player,
        "scores": scores,  # add this
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Το παιχνίδι αποθηκεύτηκε!")


def load_game():
    from deck import DeckManager  # Local import avoids circular issues

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Επαναφορά deck
    deck_manager = DeckManager()
    deck_manager.load_from_dict(data["deck"])  # FIXED

    # Επαναφορά παικτών
    players.load_from_save(data["players"])

    # Επιστροφή παίκτη ως string
    current_player_name = data["current_player"]

    print("Το παιχνίδι φορτώθηκε!")
    return deck_manager, current_player_name, data["scores"]
