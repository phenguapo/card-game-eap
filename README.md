# Παιχνίδι Μνήμης με Κάρτες

Ένα παιχνίδι μνήμης με κάρτες με γραφικό περιβάλλον (GUI), αναπτυγμένο σε Python με χρήση της βιβλιοθήκης Tkinter, στο πλαίσιο ομαδικής εργασίας στο Ελληνικό Ανοικτό Πανεπιστήμιο. Το παιχνίδι υποστηρίζει πολλαπλά επίπεδα δυσκολίας και λειτουργίες παίκτη, συμπεριλαμβανομένου του ανθρώπου εναντίον υπολογιστή.

## Εγκατάσταση

Κάντε clone το repository και βεβαιωθείτε ότι είναι εγκατεστημένη η Python (συνιστάται η έκδοση 3.10 ή νεότερη).

Εγκαταστήστε τις απαραίτητες βιβλιοθήκες. Επιλέξτε μία από τις παρακάτω εντολές:

```bash
# Συνιστώμενο
pip install pillow

# Εναλλακτικά
pip3 install pillow

# Αν χρησιμοποιείτε εικονικό περιβάλλον (παράδειγμα)
python -m venv venv
source venv/bin/activate  # Σε Windows: venv\Scripts\activate
pip install pillow
```

## Εκτέλεση του Προγράμματος

Εκτελέστε το κύριο αρχείο:

```bash
python main.py
```

Εναλλακτικά:

```bash
python3 main.py
```
Ή:
```bash
py main.py
```

Βεβαιωθείτε ότι ο φάκελος `assets/` (με τις εικόνες και τους κανόνες) βρίσκεται στον root φάκελο του project.

## Δομή
- `assets/` - Περιέχει όλες τις εικόνες, τα εικονίδια και τους κανόνες
- `build/` - Αρχεία που δημιουργούνται από το pyinstaller
- `dist/` - Περιέχει την .exe έκδοση του παιχνιδιού καθώς και τον φάκελο assets για αυτή
- `main.py` - Σημείο εκκίνησης του παιχνιδιού
- `gui.py` - Περιέχει το γραφικό περιβάλλον και τη σχετική λογική
- `deck.py` - Διαχειρίζεται την τράπουλα και τους κανόνες του παιχνιδιού
- `README.md` - Αυτές οι οδηγίες
- `save_load.py` - Χειρίζεται την αποθήκευση και φόρτωση του παιχνιδιού
- `saved_game.json` - (ΠΡΟΑΙΡΕΤΙΚΟ) Περιέχει τα αποθηκευμένα δεδομένα, δημιουργείται κάθε φορά που γίνεται αποθήκευση
- `.gitignore` - Χρησιμοποιείται για σωστή διαχείριση εκδόσεων του project

## Dependencies

- Python 3.8+
- Pillow (PIL)
- Tkinter (περιλαμβάνεται στη βασική βιβλιοθήκη της Python)

---

# Memory Card Game

A GUI-based memory card game developed in Python using Tkinter as part of a team project in the Hellenic Open University. The game supports multiple difficulty levels and player modes including human vs. computer.

## Installation

Clone the repository and ensure Python is installed (v3.10+ recommended).

Install the required dependencies. You may choose one of the following commands:

```bash
# Recommended
pip install pillow

# Alternative
pip3 install pillow

# If using a virtual environment (example)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pillow
```

## Running the Project

Run the main module:

```bash
python main.py
```

Alternatively:

```bash
python3 main.py
```
Or:
```bash
py main.py
```

Ensure the `assets/` directory (with images and rules) is located in the project root.

## Project Structure
- `assets/` - Contains all images and icons as well as the rules
- `build/` - Generated files by pyinstaller
- `dist/` - Contains the .exe version of the game as well as an assets folder for it
- `main.py` - Entry point to start the game
- `gui.py` - Contains all UI components and logic
- `deck.py` - Manages the card deck and game rules
- `README.md` - These instructions
- `save_load.py` - Handles saving and loading of the game
- `saved_game.json` -  (OPTIONAL) Contains saved data, generated on every save
- `.gitignore` - Used for correct versioning of the project

## Dependencies

- Python 3.8+
- Pillow (PIL)
- Tkinter (comes with Python standard library)
