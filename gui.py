import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import random
from deck import DeckManager

# ------------------------------------------------------------------------
PLAYER_LABELS = {
    "Players 2":        ["Player 1", "Player 2"],
    "Players 3":        ["Player 1", "Player 2", "Player 3"],
    "Players 4":        ["Player 1", "Player 2", "Player 3", "Player 4"],
    "Player - Computer":["Player",   "Computer"],
}
# ------------------------------------------------------------------------

class ScreenManager:
    """Ορισμός και αρχικοποίηση του μετρητή και των χαρακτηριστικών της κλάσης
    που θα χρησιμοποιηθούν για την λήψη των αρχικών διαστάσεων του καμβά"""

    canvas_count = 0
    instance_counter = 0  # Μετρητής για όλα τα instances
    initial_cnv_width = None
    initial_cnv_height = None

    def __init__(self, canvas):
        ScreenManager.instance_counter += 1
        self.instance_id = ScreenManager.instance_counter  # μοναδικό ID
        self.canvas = canvas
        self.bg_image = None
        self.bg = None
        self.label_menu = None
        self.label_game_level = None
        self.label_player_selection = None
        self.player_labels = PLAYER_LABELS

        # Ορισμός και αρχικοποίηση μεταβλητών γραμματοσειρών(font attributes)
        self.initial_fonts = {
            "title": 35,
            "menu": 30,
            "game_level": 25,
            "player_selection": 25,
            "button": button_font,
            "Score": 16,
            "rules": 18,
            "dropdown_menu": 18,
            "dropdown_fonts": 16,
        }

        # Μέθοδος για την απόδοση των διαστάσεων του καμβά
        self.canvas.update_idletasks()

        # Λήψη των αρχικών διαστάσεων του καμβά
        ScreenManager.canvas_count += 1
        if ScreenManager.canvas_count == 1:
            ScreenManager.initial_cnv_width = self.canvas.winfo_width()
            ScreenManager.initial_cnv_height = self.canvas.winfo_height()

    def show_error(self, message):
        from tkinter import messagebox

        messagebox.showerror("Σφάλμα", message)

    # Μέθοδος για την δημιουργία της εικόνας φόντου
    def background_image(self, image_path):
        # Άνοιγμα της εικόνας
        self.bg_image = Image.open(image_path)
        # Προσαρμογή της εικόνας στο μέγεθος του καμβά
        resized_bg = self.bg_image.resize(
            (self.canvas.winfo_width(), self.canvas.winfo_height()), Image.LANCZOS
        )
        # Δημιουργία αντικειμένου της αναπροσαρμοσμένης εικόνας για χρήση από tkinter
        self.bg = ImageTk.PhotoImage(resized_bg)
        # Φόρτωση της εικόνας στον καμβά (δημιουργία και ενημέρωση του ίδιου image_id κάθε φορά)
        self.image_id = self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

    # Μέθοδος για την φόρτωση του τίτλου του παιχνιδιού
    def load_title(self):
        # Δημιουργία του πλαισίου (frame) για τον τίτλο του παιχνιδιού
        self.frame_game_title = tk.Frame(
            self.canvas, bg="#b38f00", relief="raised", bd=10
        )
        self.frame_game_title.place(relx=0.5, rely=0.05, anchor="center")

        """ Δημιουργία του τίτλου παιχνιδιού μέσα στο πλαίσιο(frame) και χρήση της μεθόδου scaled_font_size() 
        για την διαμόρφωση μεγέθους γραμματοσειράς σε περίπτωση που έχει γίνει resize και τρέξει
         η μέθοδος σε επόμενη κλάση με αλλαγή οθόνης προς αποφυγή εμφάνισης αρχικού μεγέθους γραμ/σειράς"""
        self.game_title = tk.Label(
            self.frame_game_title,
            text="Memory Card Game",
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "title", self.canvas.winfo_width(), self.canvas.winfo_height()
                ),
                "bold",
            ),
            bg="darkgreen",
            fg="white",
        )
        self.game_title.pack(ipadx=100)

    # Μέθοδος για την καταστροφή των υφιστάμενων widgets προς χρήση σε αλλαγές οθόνης
    def destroy_widgets(self):
        for widget in self.canvas.winfo_children():
            widget.place_forget()

    # Μέθοδος για εύρεση των αναλογιών του καμβά (τρέχουσες διαστάσεις / αρχικές)
    def get_ratios(self, width, height):
        return (
            round(width / ScreenManager.initial_cnv_width, 2),
            round(height / ScreenManager.initial_cnv_height, 2),
        )

    # Μέθοδος για το κατάλληλο μέγεθος γραμματοσειράς αναλογικά με το μέγεθος του καμβά
    def scaled_font_size(self, font_key, width, height):
        width_ratio, height_ratio = self.get_ratios(width, height)

        if width_ratio == height_ratio and width == ScreenManager.initial_cnv_width:
            font = self.initial_fonts[font_key]
        elif width_ratio > height_ratio:
            font = int(height_ratio * self.initial_fonts[font_key])
        else:
            font = int(width_ratio * self.initial_fonts[font_key])
        return font

    # Μέθοδος για την αναδιαμόρφωση των widgets της οθόνης αναλογικά με το μέγεθος του καμβά
    def resize(self, event):
        width, height = event.width, event.height
        self.resize_background(width, height)
        self.resize_fonts(width, height)

    # Μέθοδος για την αναδιαμόρφωση της εικόνας του φόντου
    def resize_background(self, width, height):
        resized_bg = self.bg_image.resize((width, height), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.image_id, image=self.bg)

    # Μέθοδος για το καταλλήλο μέγεθος γραμματοσειράς
    def resize_fonts(self, width, height):
        # Ενημέρωση ετικετών
        self.game_title.config(
            font=(
                "Times New Roman",
                self.scaled_font_size("title", width, height),
                "bold",
            )
        )
        if self.label_menu:
            self.label_menu.config(
                font=(
                    "Times New Roman",
                    self.scaled_font_size("menu", width, height),
                    "bold",
                    "italic",
                )
            )
        style.configure(
            "My.TButton",
            background="#6666FF",
            foreground="white",
            font=(
                "Times New Roman",
                self.scaled_font_size("button", width, height),
                "bold",
            ),
        )
        if self.label_game_level:
            self.label_game_level.config(
                font=(
                    "Times New Roman",
                    self.scaled_font_size("game_level", width, height),
                    "bold",
                    "italic",
                )
            )
        if self.label_player_selection:
            self.label_player_selection.config(
                font=(
                    "Times New Roman",
                    self.scaled_font_size("player_selection", width, height),
                    "bold",
                    "italic",
                )
            )

    def uncompleted_game_management(self, mode):
        import save_load

        if mode == "load":
            try:
                if not isinstance(self, StartGame):
                    raise Exception(
                        "Η φόρτωση υποστηρίζεται μόνο στην οθόνη StartGame."
                    )

                (
                    deck_manager,
                    current_player_name,
                    scores,
                    level,
                    players,
                ) = save_load.load_game()

                self.update_data(level, players)

                self.deck_manager = deck_manager
                self.current_player = current_player_name
                self.current_player_index = self.player_order.index(current_player_name)
                self.scores = scores

                self.build_screen()

            except FileNotFoundError as e:
                self.show_error(f"Σφάλμα φόρτωσης αποθηκευμένου παιχνιδιού:\n{e}")
            except Exception as e:
                self.show_error(
                    f"Σφάλμα κατά την επιστροφή στο αποθηκευμένο παιχνίδι:\n{e}"
                )

        else:
            try:
                if not isinstance(self, StartGame):
                    raise Exception(
                        "Αυτή η οθόνη δεν υποστηρίζει αποθήκευση παιχνιδιού."
                    )

                save_load.save_game(
                    self.deck_manager,
                    self.current_player,
                    self.scores,
                    self.level,
                    self.players,
                )

            except Exception as e:
                self.show_error(f"Σφάλμα κατά την αποθήκευση του παιχνιδιού:\n{e}")


class MainMenu(ScreenManager):
    def __init__(self, canvas, controller):
        super().__init__(canvas)
        self.controller = controller

    def build_screen(self):
        self.destroy_widgets()
        self.background_image(os.path.join("assets/images", "cards.png"))
        self.load_title()
        # Δημιουργία πλαισίου(frame) για το menu
        menu_frame = tk.Frame(self.canvas, bg="darkgreen", relief="raised", bd=10)
        menu_frame.place(relx=0.5, rely=0.35, anchor="center")

        """ Προσθήκη ετικέτας(label) και διαμόρφωση μεγέθους γραμματοσειράς σε περίπτωση που έχει γίνει resize 
        και επιστρέψουμε  στην εν λόγω οθόνη από κάποια άλλη οθόνη """
        self.label_menu = tk.Label(
            menu_frame,
            text="MENU",
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "menu", self.canvas.winfo_width(), self.canvas.winfo_height()
                ),
                "bold",
                "italic",
            ),
            bg="darkgreen",
            fg="white",
        )
        self.label_menu.pack(padx=20)

        # Προσθήκη κουμπιών(buttons)
        label_menu_buttons = ["New Game", "Resume Game", "Exit"]

        for label in label_menu_buttons:
            if label == "New Game":
                command = lambda: self.controller.show_screen("game_level")
            elif label == "Resume Game":
                command = lambda: self.controller.resume_saved_game()
            else:
                command = root.destroy
            button = ttk.Button(
                menu_frame, text=label, style="My.TButton", command=command
            )
            button.pack(fill="x", padx=30, pady=10)

        self.canvas.bind("<Configure>", self.resize)


class GameLevel(ScreenManager):
    def __init__(self, canvas, controller):
        super().__init__(canvas)
        self.controller = controller

    def build_screen(self):
        self.destroy_widgets()
        self.background_image(os.path.join("assets/images", "Game_selection.png"))
        self.load_title()
        # Δημιουργία πλαισίου(frame) για τα επιπεδα δυσκολίας και τοποθέτηση στον καμβά
        frame_game_level = tk.Frame(self.canvas, bg="green", relief="raised", bd=10)
        frame_game_level.place(relx=0.5, rely=0.45, anchor="center")

        """ Δημιουργία ετικέτας και τοποθέτηση στο πλαίσιο με παράλληλη διαμόρφωση μεγέθους γραμματοσειράς 
        σε περίπτωση που έχει γίνει resize και περάσουμε ή επιστρέψουμε στην εν λόγω οθόνη από κάποια άλλη οθόνη """
        self.label_game_level = tk.Label(
            frame_game_level,
            text="GAME LEVEL",
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "game_level", self.canvas.winfo_width(), self.canvas.winfo_height()
                ),
                "bold",
                "italic",
            ),
            bg="green",
            fg="white",
        )
        self.label_game_level.pack(padx=20)

        # Δημιουργία κουμπιών επιπέδων δυσκολίας
        label_levels = ["Easy", "Medium", "Hard", "Back To Menu"]
        for label in label_levels:
            if label == "Back To Menu":
                command = command = lambda: self.controller.show_screen("main_menu")
            else:
                command = command = lambda lvl=label: self.set_level(lvl)

            button = ttk.Button(
                frame_game_level, text=label, style="My.TButton", command=command
            )
            button.pack(fill="x", padx=30, pady=10)

        # Binding event σε περίπτωση αλλαγής μεγέθους καμβά
        self.canvas.bind("<Configure>", self.resize)

    def set_level(self, level):
        self.controller.level = level
        self.controller.show_screen("player_selection")


class PlayerSelection(ScreenManager):
    def __init__(self, canvas, level, controller):
        super().__init__(canvas)
        self.level = level
        self.controller = controller

    def update_data(self, level, players):
        self.level = level
        self.players = players
        self.vs_computer = players == "Player - Computer"
        self.image_id = None
        self.lock_board = False
        self.current_player = "Player"
        self.deck_manager = None  # force reinitialization
        self.card_widgets = []
        self.player_order = []
        self.scores = {}

    def build_screen(self):
        self.destroy_widgets()
        self.background_image(os.path.join("assets/images", "Game_selection.png"))
        self.load_title()
        # Δημιουργία πλαισίου για τα επερχόμενα widgets και τοποθέτηση στον καμβά
        frame_player_selection = tk.Frame(
            self.canvas, bg="green", relief="raised", bd=10
        )
        frame_player_selection.place(relx=0.5, rely=0.4, anchor="center")

        """ Δημιουργία ετικέτας και τοποθέτηση στο πλαίσιο με παράλληλη διαμόρφωση μεγέθους γραμματοσειράς 
        σε περίπτωση που έχει γίνει resize και περάσουμε ή επιστρέψουμε στην εν λόγω οθόνη από κάποια άλλη οθόνη """
        self.label_player_selection = tk.Label(
            frame_player_selection,
            text="PLAYER SELECTION",
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "player_selection",
                    self.canvas.winfo_width(),
                    self.canvas.winfo_height(),
                ),
                "bold",
                "italic",
            ),
            bg="green",
            fg="white",
        )
        self.label_player_selection.pack(padx=20)

        # Δημιουργία κουμπιών που αντιστοιχούν στους δυνητικούς συμμετέχοντες ανάλογα με το επίπεδο δυσκολίας
        self.label_players = {
            "Easy": ["Players 2", "Player - Computer", "Back to Levels"],
            "Medium": ["Players 2", "Players 3", "Player - Computer", "Back to Levels"],
            "Hard": [
                "Players 2",
                "Players 3",
                "Players 4",
                "Player - Computer",
                "Back to Levels",
            ],
        }

        for label in self.label_players[self.level]:
            if label == "Back to Levels":
                command = lambda: self.controller.show_screen("game_level")
            else:
                command = lambda p=label: self.set_players(p)
            button = ttk.Button(
                frame_player_selection, text=label, style="My.TButton", command=command
            )
            button.pack(fill="x", padx=50, pady=10)

        # Binding event σε περίπτωση αλλαγής μεγέθους καμβά
        self.canvas.bind("<Configure>", self.resize)

    def set_players(self, players):
        self.controller.players = players
        self.controller.show_screen("start_game")


class StartGame(ScreenManager):
    def __init__(self, canvas, level, players, controller):
        self.card_faces = {}  # image references
        super().__init__(canvas)
        self.level = level
        self.players = players
        self.controller = controller
        self.lock_board = False
        self.current_player = "Player"  # or index 0
        self.vs_computer = self.players == "Player - Computer"
        self.card_positions = {}  # at start of method or __init__


    def show_banner(self, text):
        if hasattr(self, "turn_banner"):
            self.turn_banner.destroy()

        self.turn_banner = tk.Label(
            self.canvas,
            text=text,
            font=("Times New Roman", 22, "bold"),
            bg="darkblue",
            fg="white",
        )
        self.turn_banner.place(relx=0.5, rely=0.02, anchor="center")

    def update_data(self, level, players):
        self.level = level
        self.players = players
        self.vs_computer = players == "Player - Computer"

        self.player_order = PLAYER_LABELS[self.players]

        self.lock_board = False
        self.current_player = "Player 1"
        self.deck_manager = None
        self.card_widgets = []
        self.scores = {}

    def build_screen(self):
        self.destroy_widgets()
        self.canvas.delete("all")

        # Καθορισμός δεδομένων για διάταξη παικτών
        players_layout = {
            "Easy": {
                "Players 2": ([0.245, 0.67], ["w", "e"]),
                "Player - Computer": ([0.245, 0.67], ["w", "e"]),
            },
            "Medium": {
                "Players 2": ([0.245, 0.67], ["w", "e"]),
                "Players 3": ([0.245, 0.46, 0.67], ["w", "center", "e"]),
                "Player - Computer": ([0.245, 0.67], ["w", "e"]),
            },
            "Hard": {
                "Players 2": ([0.245, 0.67], ["w", "e"]),
                "Players 3": ([0.245, 0.46, 0.67], ["w", "center", "e"]),
                "Players 4": (
                    [0.245, 0.385, 0.525, 0.67],
                    ["w", "center", "center", "e"],
                ),
                "Player - Computer": ([0.245, 0.67], ["w", "e"]),
            },
        }

        self.relx_players_values = players_layout[self.level][self.players][0]
        self.anchor_players_values = players_layout[self.level][self.players][1]

        self.player_order = PLAYER_LABELS[self.players]

        # Χρήσιμο για εναλλαγή σειράς παικτών
        self.player_order = PLAYER_LABELS[self.players]
        self.current_player_index = 0
        self.current_player = self.player_order[self.current_player_index]

        # Μηδενισμός σκορ

        if not hasattr(self, "scores") or not self.scores:
            self.scores = {player: 0 for player in self.player_order}

        self.start_game_layout_buttons()
        self.show_score()
        self.show_cards()
        self.show_banner(f"{self.current_player}'s turn")

        self.show_banner(f"{self.current_player}'s turn")

        if self.vs_computer and self.current_player == "Computer":
            self.lock_board = True
            self.canvas.after(1000, self.computer_play)

    # Μέθοδος για την δημιουργία και διάταξη των κουμπιών
    def start_game_layout_buttons(self):

        # Δημιουργία πλαισίου για το κουμπί του μενού
        frame_dropdown_menu = tk.Frame(self.canvas)
        frame_dropdown_menu.place(relx=0.0, rely=0.023, anchor="w")

        # Μενού στην κεντρική οθόνη
        clicked_option = tk.StringVar()
        clicked_option.set("Menu")
        options = [
            "Rules of the Game",
            "Save Game",
            "Back To Initial Menu",
            "Play Again",
            "Exit",
        ]
        dropdown = tk.OptionMenu(
            frame_dropdown_menu, clicked_option, *options, command=self.select_menu
        )
        dropdown.config(
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "dropdown_menu",
                    self.canvas.winfo_width(),
                    self.canvas.winfo_height(),
                ),
                "bold",
                "italic",
            ),
            bg="#6666FF",
            fg="white",
            relief="raised",
            activebackground="#FFFF99",
            activeforeground="black",
        )

        # Ρύθμιση της γραμματοσειράς του dropdown menu
        menu = dropdown.nametowidget(dropdown.menuname)
        menu.config(
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "dropdown_fonts",
                    self.canvas.winfo_width(),
                    self.canvas.winfo_height(),
                ),
            ),
            bg="#FFFF99",
            fg="black",
            activebackground="#6666FF",
            activeforeground="white",
        )
        dropdown.pack(side="left")

        # Πλήκτρο επιστροφής στην προηγούμενη οθόνη
        back_button = ttk.Button(
            frame_dropdown_menu,
            text="⬅",
            width=6,
            style="My.TButton",
            command=lambda: self.controller.show_screen("player_selection"),
        )
        back_button.pack(side="left", fill="both")

        # Λεξικό προς χρήση για την δημιουργία κουμπιών των παικτών
        self.player_order = PLAYER_LABELS[self.players]

        # Δημιουργία πλαισίων για τα κουμπιά των παικτών και για το σκορ
        self.list_frames = []
        # Δημιουργία πλαισίων για τα ονόματα των παικτών και για το σκορ
        self.list_frames = []
        for i, name in enumerate(PLAYER_LABELS[self.players]):
            frame = tk.Frame(self.canvas, bg="")
            self.list_frames.append(frame)
            frame.place(relx=self.relx_players_values[i], rely=0.9)

            player_lbl = tk.Label(
                frame,
                text=name,
                font=("Times New Roman", 16, "bold"),
                bg="#6666FF",
                fg="white",
                relief="raised",
                padx=8,
                pady=2,
            )
            player_lbl.pack()

    # Μέθοδος για την ενεργοποίηση των επιλογών του μενού
    def select_menu(self, choice):
        if choice == "Save Game":
            self.uncompleted_game_management("save")
        elif choice == "Back To Initial Menu":
            self.controller.show_screen("main_menu")
        elif choice == "Play Again":
            self.controller.show_screen("start_game")
        elif choice == "Rules of the Game":
            self.game_rules()
        else:
            root.destroy()

    # Μέθοδος για την εμφάνιση των κανόνων του παιχνιδιού
    def game_rules(self):
        self.destroy_widgets()
        try:
            with open("assets/rules/rules.txt", "r", encoding="utf-8") as file:
                rules_text = file.read()
        except FileNotFoundError:
            rules_text = "Το αρχείο κανόνων δεν βρέθηκε."

        self.text_widget = tk.Text(
            self.canvas,
            wrap="word",
            font=(
                "Times New Roman",
                self.scaled_font_size(
                    "rules", self.canvas.winfo_width(), self.canvas.winfo_height()
                ),
            ),
            bg="#001f3f",  # Dark navy
            fg="white",
            insertbackground="white",
            padx=20,
            pady=20,
            relief="groove",
            borderwidth=4,
        )
        self.text_widget.insert("1.0", rules_text)
        self.text_widget.config(state="disabled")  # Read-only
        self.text_widget.place(relx=0.2, rely=0.08, relwidth=0.6, relheight=0.75)

        return_button = ttk.Button(
            self.canvas,
            text="⬅ Back to Game",
            style="My.TButton",
            command=lambda: self.controller.show_screen("start_game"),
        )
        return_button.place(relx=0.4, rely=0.86, relwidth=0.2, relheight=0.06)

        self.canvas.bind("<Configure>", self.resize_game_rules)

    # Αναπροσαρμογή της γραμματοσειράς των κανόνων του παιχνιδιού
    def resize_game_rules(self, event):

        width, height = event.width, event.height
        self.resize_background(width, height)
        width_ratio, height_ratio = self.get_ratios(width, height)

        if width_ratio == height_ratio and width == ScreenManager.initial_cnv_width:
            self.text_widget.config(
                font=("Times New Roman", self.scaled_font_size("rules", width, height))
            )
        elif width_ratio > height_ratio:
            self.text_widget.config(
                font=("Times New Roman", self.scaled_font_size("rules", width, height))
            )
        else:
            self.text_widget.config(
                font=("Times New Roman", self.scaled_font_size("rules", width, height))
            )

        style.configure(
            "My.TButton",
            background="#6666FF",
            foreground="white",
            font=(
                "Times New Roman",
                self.scaled_font_size("button", width, height),
                "bold",
            ),
        )

    # Μέθοδος για την εμφάνιση των τραπουλόχαρτων
    def show_cards(self):
        # Διαμόρφωση μεγέθους της τράπουλας
        self.card_width = int(self.canvas.winfo_width() * 0.057)  # was 0.06
        self.card_height = int(self.canvas.winfo_height() * 0.11)  # was 0.16
        self.card_photo = Image.open(os.path.join("assets/images", "image_card.jpg"))
        card_initial_size = self.card_photo.resize((self.card_width, self.card_height))
        self.card_back = ImageTk.PhotoImage(card_initial_size)

        # Κλήση της μεθόδου για την εμφάνιση της τράπουλας
        self.cards_layout()

        # Binding event για την αναδιαμόρφωση του μεγέθους της τράπουλας σε περίπτωση αλλαγής μεγέθους καμβά
        self.canvas.bind("<Configure>", self.resize_cards)

    # Μέθοδος για την δημιουργία της διάταξης της τράπουλας
    def cards_layout(self):
        if (
            not hasattr(self, "deck_manager")
            or self.deck_manager is None
            or not getattr(self.deck_manager, "board", None)
        ):
            self.deck_manager = DeckManager()
            difficulty = self.level.strip().lower()
            self.deck_manager.create_board(difficulty)

        board = self.deck_manager.board

        card_layout_settings = {
            "easy": (0.365, 0.1),
            "medium": (0.15, 0.1),
            "hard": (0.05, 0.1),
        }

        difficulty = self.level.strip().lower()
        card_layout_x, card_layout_y = card_layout_settings[difficulty]
        y = card_layout_y

        self.card_widgets = []

        for i, row in enumerate(board):
            x = card_layout_x
            widget_row = []
            for j, card in enumerate(row):
                if card is not None:
                    label = tk.Label(
                        self.canvas, image=self.card_back, bg="white", relief="raised"
                    )
                    label.image = self.card_back
                    label.row = i
                    label.col = j

                    label.bind(
                        "<Button-1>",
                        lambda event, row=i, col=j: self.on_card_click(row, col),
                    )
                    label.place(relx=x, rely=y, relwidth=0.06, relheight=0.12)

                    if card.is_open:
                        card_name = str(card).lower().replace(" ", "_")
                        card_path = os.path.join("assets/images/cards", card_name)

                        try:
                            face_image = Image.open(card_path)
                            face_image = face_image.resize(
                                (self.card_width, self.card_height), Image.LANCZOS
                            )
                            card_face = ImageTk.PhotoImage(face_image)

                            label.config(image=card_face, text="")
                            label.image = card_face
                        except Exception as e:
                            self.show_error(
                                f"Could not load card image: {card_path} | {e}"
                            )

                    widget_row.append(label)
                else:
                    widget_row.append(None)
                x += 0.07
            y += 0.18
            self.card_widgets.append(widget_row)

        self.card_faces.clear()

    def on_card_click(self, row, col, bypass_lock=False):
        if (not bypass_lock) and (
            self.lock_board or (self.vs_computer and self.current_player == "Computer")
        ):
            return

        card = self.deck_manager.board[row][col]
        if card.is_open or card.is_matched:
            return

        if len(self.deck_manager.selected_cards) >= 2:
            return

        needs_check = self.deck_manager.select_card(row, col)

        label = self.card_widgets[row][col]
        card_name = str(card)  # p.x. '10_of_spades.png'
        card_path = os.path.join("assets/images/cards", card_name)

        try:
            face_img = Image.open(card_path)
            face_img = face_img.resize(
                (self.card_width, self.card_height), Image.LANCZOS
            )
            card_face = ImageTk.PhotoImage(face_img)

            label.config(image=card_face, text="")
            label.image = card_face
            self.card_faces[f"{row}_{col}"] = card_face
            self.canvas.update()
        except Exception as e:
            self.show_error(f"error loading {card_path}: {e}")
            label.config(text="?", font=("Arial", 12), bg="red", fg="white")

        card.is_open = True

        if needs_check:
            self.lock_board = True
            self.canvas.after(500, self.resolve_turn)

    def update_score_label(self, player):
        self.score_labels[player].config(text=f"Score: {self.scores[player]}")

    def close_selected_cards(self):
        for (r, c) in self.deck_manager.selected_cards:
            lbl = self.card_widgets[r][c]
            lbl.config(image=self.card_back)
            lbl.image = self.card_back
            self.deck_manager.board[r][c].is_open = False
        self.deck_manager.selected_cards.clear()

    def resolve_turn(self):
        matched, pts, action = self.deck_manager.check_match()

        if matched:
            self.scores[self.current_player] += pts
            self.update_score_label(self.current_player)


            if action == "third_match_close_all":
                self.close_selected_cards()

            if action == "allow_third":
                self.lock_board = False
                if self.vs_computer and self.current_player == "Computer":
                    self.canvas.after(500, self.computer_play)
                return

            if self.deck_manager.is_game_over():
                self.check_game_over()
                return

            advance = 0 if action == "play_again" else 1
            if action == "skip_next":
                advance = 2

            self.current_player_index = (self.current_player_index + advance) % len(self.player_order)
            self.current_player = self.player_order[self.current_player_index]
            self.show_banner(f"{self.current_player}'s turn")

            if self.vs_computer and self.current_player == "Computer":
                self.lock_board = True
                self.canvas.after(500, self.computer_play)
            else:
                self.lock_board = False

            self.check_game_over()
            return

        # --- Περίπτωση “χωρίς ταίρι” (matched=False): κλείνουμε όλες τις selected_cards
        self.close_selected_cards()
        self.lock_board = False

        self.current_player_index = (self.current_player_index + 1) % len(self.player_order)
        self.current_player = self.player_order[self.current_player_index]

        if self.deck_manager.is_game_over():
            self.check_game_over()
            return

        self.show_banner(f"{self.current_player}'s turn")
        if self.vs_computer and self.current_player == "Computer":
            self.lock_board = True
            self.canvas.after(500, self.computer_play)

        self.check_game_over()

    def computer_play(self):
        bd = self.deck_manager
        hist = [
            (r, c)
            for (r, c) in bd.history
            if not bd.board[r][c].is_matched and not bd.board[r][c].is_open
        ]

        val_map = {}
        pair = None
        for r, c in hist:
            v = bd.board[r][c].value
            val_map.setdefault(v, []).append((r, c))
            if len(val_map[v]) == 2:
                pair = val_map[v]
                break

        if pair:
            bd.history = [rc for rc in bd.history if rc not in pair]
            (r1, c1), (r2, c2) = pair
            self.on_card_click(r1, c1, bypass_lock=True)
            self.canvas.after(500, lambda: self.on_card_click(r2, c2, bypass_lock=True))
            return

        closed = [
            (i, j)
            for i, row in enumerate(bd.board)
            for j, card in enumerate(row)
            if card and not card.is_open and not card.is_matched
        ]

        if len(closed) < 2:
            return

        r1, c1 = random.choice(closed)
        self.on_card_click(r1, c1, bypass_lock=True)

        def play_second_card():
            new_closed = [
                (i, j)
                for i, row in enumerate(bd.board)
                for j, card in enumerate(row)
                if card
                and not card.is_open
                and not card.is_matched
                and (i, j) != (r1, c1)
            ]

            mate = next(
                (
                    (r, c)
                    for (r, c) in hist
                    if bd.board[r][c].value == bd.board[r1][c1].value
                ),
                None,
            )

            if mate and mate in new_closed:
                if mate in bd.history:
                    bd.history.remove(mate)
                self.on_card_click(mate[0], mate[1], bypass_lock=True)
            elif new_closed:
                r2, c2 = random.choice(new_closed)
                self.on_card_click(r2, c2, bypass_lock=True)

        self.canvas.after(500, play_second_card)

    def resize_cards(self, event):
        """Μέθοδος για την αναδιαμόρφωση του μεγέθους της τράπουλας σε περίπτωση αλλαγής μεγέθους καμβά."""
        if not hasattr(self, "card_positions"):
            return

        if event.width <= 1 or event.height <= 1:
            return

        canvas_w, canvas_h = event.width, event.height

        new_w = max(30, int(canvas_w * 0.06))
        aspect = self.card_photo.height / self.card_photo.width
        new_h = int(new_w * aspect)

        if getattr(self, "_last_card_size", None) == (new_w, new_h):
            return
        self._last_card_size = (new_w, new_h)

        resized_img = self.card_photo.resize((new_w, new_h), Image.LANCZOS)
        self.card_back = ImageTk.PhotoImage(resized_img)

        relw = new_w / canvas_w
        relh = new_h / canvas_h

        for lbl, (relx, rely) in self.card_positions.items():
            card = self.deck_manager.board[lbl.row][lbl.col]

            if card.is_open:
                card_name = str(card).lower().replace(" ", "_")
                card_path = os.path.join("assets/images/cards", card_name)
                try:
                    face_image = Image.open(card_path)
                    face_image = face_image.resize((new_w, new_h), Image.LANCZOS)
                    card_face = ImageTk.PhotoImage(face_image)
                    lbl.configure(image=card_face)
                    lbl.image = card_face
                except Exception as e:
                    self.show_error(
                        f"Could not resize face card image: {card_path} | {e}"
                    )
            else:
                lbl.configure(image=self.card_back)
                lbl.image = self.card_back

            lbl.place_configure(relx=relx, rely=rely, relwidth=relw, relheight=relh)

        new_font = (
            "Times New Roman",
            self.scaled_font_size("button", canvas_w, canvas_h),
            "bold",
        )
        style.configure("My.TButton", font=new_font)

    # Μέθοδος για την δημιουργία ετικετών για το σκορ των παικτών
    def show_score(self):
        self.score_labels = {}

        for i, player in enumerate(PLAYER_LABELS[self.players]):
            frame = self.list_frames[i]
            label = tk.Label(
                frame,
                text=f"Score: {self.scores[player]}",
                font=(
                    "Times New Roman",
                    self.scaled_font_size(
                        "Score", self.canvas.winfo_width(), self.canvas.winfo_height()
                    ),
                    "bold",
                ),
                bg="#FFFF99",
                fg="black",
            )
            label.pack(fill="x")
            self.score_labels[player] = label

    def check_game_over(self):
        if self.deck_manager.is_game_over():
            winner = self.get_winner()
            if winner == "Tie":
                message = f"Game Over! It's a tie!\nFinal Score: {self.scores}"
            else:
                message = f"Game Over! {winner} wins!\nFinal Score: {self.scores}"

            messagebox.showinfo("Game Over", message)
            self.controller.show_screen("main_menu")

    def get_winner(self):
        max_score = max(self.scores.values())
        winners = [p for p, s in self.scores.items() if s == max_score]
        return winners[0] if len(winners) == 1 else "Tie"


class GuiController:
    def __init__(self, root):
        self.root = root
        # Δημιουργία Καμβά
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="darkgreen")
        self.canvas.pack(fill="both", expand=True)

        # Δημιουργία αντικειμένων
        self.screens = {
            "main_menu": MainMenu(self.canvas, self),
            "game_level": GameLevel(self.canvas, self),
        }

        self.current_screen = None
        self.show_screen("main_menu")

    def show_screen(self, screen_name):
        if screen_name == "player_selection":
            if "player_selection" not in self.screens:
                self.screens["player_selection"] = PlayerSelection(
                    self.canvas, self.level, self
                )
            else:
                self.screens["player_selection"].update_data(self.level, self.players)
            self.current_screen = self.screens["player_selection"]

        elif screen_name == "start_game":
            level = self.level
            players = self.players

            if "start_game" not in self.screens:
                self.screens["start_game"] = StartGame(
                    self.canvas, level, players, self
                )
            else:
                self.screens["start_game"].update_data(level, players)
            self.current_screen = self.screens["start_game"]

        else:
            self.current_screen = self.screens[screen_name]

        self.current_screen.build_screen()

    def resume_saved_game(self):
        from save_load import load_game

        try:
            deck_manager, current_player, scores, level, players = load_game()

            if "start_game" not in self.screens:
                self.screens["start_game"] = StartGame(
                    self.canvas, level, players, self
                )

            start_screen = self.screens["start_game"]
            start_screen.update_data(level, players) # type: ignore

            start_screen.deck_manager = deck_manager
            start_screen.current_player = current_player

            start_screen.current_player_index = start_screen.player_order.index( # type: ignore
                current_player
            )
            start_screen.scores = scores

            self.level = level
            self.players = players
            self.current_screen = start_screen
            self.current_screen.build_screen()

        except FileNotFoundError as e:
            self.current_screen.show_error(f"Αρχείο δεν βρέθηκε:\n{e}")
        except Exception as e:
            self.current_screen.show_error(f"Σφάλμα φόρτωσης παιχνιδιού:\n{e}")


def start_interface():
    global root, style, button_font
    # Δημιουργία παραθύρου
    root = tk.Tk()
    root.state("zoomed")
    root.geometry("1000x700+700+150")
    root.minsize(width=800, height=600)
    root.title("Card Game")
    root.iconbitmap(os.path.join("assets/images", "card_deck.ico"))

    # Δημιουργία στυλ κουμπιών
    button_font = 16
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "My.TButton",
        background="#6666FF",
        foreground="white",
        font=("Times New Roman", button_font, "bold"),
    )
    style.map(
        "My.TButton",
        foreground=[("active", "black")],
        background=[("active", "#FFFF99")],
    )

    # Εκκίνηση του μενού
    GuiController(root)
    # Εκκίνηση του main loop
    root.mainloop()


if __name__ == "__main__":
    start_interface()
