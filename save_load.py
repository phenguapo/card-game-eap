import json
from deck import DeckManager

SAVE_FILE = "saved_game.json"


def save_game(deck_manager, current_player, scores, level, players):
    data = {
        "deck": deck_manager.save_to_dict(),
        "current_player": current_player,
        "scores": scores,
        "level": level,
        "players": players,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_game():
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    deck_manager = DeckManager()
    deck_manager.load_from_dict(data["deck"])
    return (
        deck_manager,
        data["current_player"],
        data["scores"],
        data["level"],
        data["players"],
    )
