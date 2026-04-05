from utils import clear_screen, pause


def add_tyre(db):
    clear_screen()
    print("=== ADD NEW TYRE ===\n")

    sku = input("SKU: ").strip()
    brand = input("Brand: ").strip()
    size = input("Size (e.g. 205/55R16 91H): ").strip()
    tyre_type = input("Type (Summer/Winter/All-season/All-terrain/All-weather): ").strip()
    pattern = input("Pattern: ").strip()

    while True:
        q = input("Quantity (number): ").strip()
        try:
            qty = int(q)
            if qty < 0:
                print("Quantity cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number for quantity.")

    while True:
        p = input("Price (e.g. 79.90): ").strip().replace(",", ".")
        try:
            price = float(p)
            break
        except ValueError:
            print("Please enter a valid number for price (e.g. 79.90).")

    desc = input("Description: ").strip()
    service_desc = input("Service Description: ").strip()

    tyre_id = db.insert_tyre(sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc)
    db.log_action(tyre_id, "ADD")

    print("Added.")
    pause()