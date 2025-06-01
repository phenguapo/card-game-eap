import random  # Για την τυχαία επιλογή πρώτου παίκτη

# Γενικά στοιχεία παικτών (λίστα και δείκτης τρέχοντος παίκτη)
players = []
current_index = 0

# Δημιουργία παικτών με βάση τη δυσκολία του παιχνιδιού
def setup_players(difficulty):
    """Δημιουργεί τους παίκτες ανάλογα με τη δυσκολία"""
    global players, current_index
    players = []  # Καθαρίζουμε τη λίστα κάθε φορά

    if difficulty == "Εύκολο":
        # Δύο ανθρώπινοι παίκτες
        players.append({"name": "Παίκτης 1", "score": 0, "is_computer": False})
        players.append({"name": "Παίκτης 2", "score": 0, "is_computer": False})
    elif difficulty == "Μέτριο":
        # Παίκτης + υπολογιστής
        players.append({"name": "Εσύ", "score": 0, "is_computer": False})
        players.append({"name": "Υπολογιστής", "score": 0, "is_computer": True})
    elif difficulty == "Δύσκολο":
        # Παίκτης + δύο υπολογιστές
        players.append({"name": "Εσύ", "score": 0, "is_computer": False})
        players.append({"name": "CPU 1", "score": 0, "is_computer": True})
        players.append({"name": "CPU 2", "score": 0, "is_computer": True})

    current_index = 0  # Ξεκινάμε πάντα από την αρχή

    # Έλεγχος αν υπάρχει υπολογιστής στο παιχνίδι
    has_computer = False
    for player in players:
        if player["is_computer"]:
            has_computer = True

    return (
        len(players),
        has_computer,
    )  # Επιστρέφει αριθμό παικτών και αν έχει υπολογιστή


# Επιλογή ποιος ξεκινάει πρώτος
def select_first_player():
    """Επιλέγει τυχαία ποιος θα ξεκινήσει"""
    global current_index
    current_index = random.randint(0, len(players) - 1)
    return players[current_index]


# Αλλαγή σειράς – πάει στον επόμενο παίκτη (ή όχι, ανάλογα την ενέργεια)
def get_next_player(current_player, action=None):
    """Επιστρέφει τον επόμενο παίκτη, ή τον ίδιο αν έχει δικαίωμα επανάληψης"""
    global current_index

    if action == "replay_2_cards" or action == "replay_1_card":
        return current_player  # Δεν αλλάζει σειρά
    elif action == "skip_next":
        current_index = (current_index + 2) % len(players)  # Παραλείπει έναν
    else:
        current_index = (current_index + 1) % len(players)  # Κανονική αλλαγή

    return players[current_index]


# Ελέγχει αν ο παίκτης είναι υπολογιστής
def is_computer_turn(player):
    return player["is_computer"]


# Προσθήκη πόντων στον παίκτη
def add_points(player, points):
    player["score"] += points


# Επιστροφή του παίκτη με τους περισσότερους πόντους
def get_winner():
    return max(players, key=lambda p: p["score"])


# Επιστρέφει όλους τους παίκτες
def get_all_players():
    return players


# Επιστρέφει τον παίκτη που έχει τώρα σειρά
def get_current_player():
    return players[current_index]


# Για αποθήκευση: επιστρέφει τα δεδομένα των παικτών σε μορφή λεξικού
def save_to_dict():
    return {"players": players, "current_index": current_index}


# Φόρτωση παικτών από αποθηκευμένο λεξικό
def load_from_save(data):
    global players, current_index
    players = data["players"]
    current_index = data["current_index"]
