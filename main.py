# main.py
# Δημήτριος Μπραϊμης – βασικός κορμός του παιχνιδιού

from gui import start_interface

def main():
    try:
        start_interface()
    except Exception as e:
        print(f"[ΣΦΑΛΜΑ] Το παιχνίδι κατέρρευσε:\n{e}")

if __name__ == "__main__":
    main()
