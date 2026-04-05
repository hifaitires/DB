import os

from utils import clear_screen, pause, base_dir


def export_csv(db):
    clear_screen()
    print("=== EXPORT TO CSV (TYRES ONLY) ===\n")
    filename = input("CSV filename (default: tyres_export.csv): ").strip() or "tyres_export.csv"
    path = os.path.join(base_dir(), filename)

    count = db.export_csv(path)
    if count == 0:
        print("No tyres to export.")
    else:
        print(f"Exported {count} rows to {path}")
    pause()


def import_csv(db):
    clear_screen()
    print("=== IMPORT FROM CSV (TYRES ONLY) ===\n")
    print("Expected header (semicolon separated):")
    print("sku;brand;size;tyre_type;pattern;quantity;price;description;service_description\n")

    filename = input("CSV filename (relative to this folder): ").strip()
    if not filename:
        print("No file given.")
        pause()
        return

    path = os.path.join(base_dir(), filename)
    result = db.import_csv(path)

    if result == -1:
        print(f"File not found: {path}")
    elif result == -2:
        print("CSV has no header.")
    elif result == -3:
        print("CSV header missing required columns.")
    else:
        print(f"Imported {result} rows from {path}")
    pause()