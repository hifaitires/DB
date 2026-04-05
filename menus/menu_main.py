# menus/menu_main.py
from utils import clear_screen
from .menu_list import list_tyres
from .menu_add import add_tyre
from .menu_logs import view_logs
from .menu_csv import export_csv, import_csv
from .menu_bulk_delete import bulk_delete


def main_menu(db):
    while True:
        clear_screen()
        print("=== TYRE STOCK SYSTEM ===\n")
        print("1) List / search tyres")
        print("2) Add tyre")
        print("3) View logs")
        print("4) Export to CSV")
        print("5) Import from CSV")
        print("6) Bulk delete tyres (IDs / ranges)")
        print("0) Exit\n")

        choice = input("Select: ").strip()

        if choice == "1":
            list_tyres(db)
        elif choice == "2":
            add_tyre(db)
        elif choice == "3":
            view_logs(db)
        elif choice == "4":
            export_csv(db)
        elif choice == "5":
            import_csv(db)
        elif choice == "6":
            bulk_delete(db)
        elif choice == "0":
            return
