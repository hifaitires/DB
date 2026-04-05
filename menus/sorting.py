def sort_rows(rows, mode):
    """
    rows:
    (id, brand, sku, size, tyre_type, pattern, quantity, price,
     description, service_description, added_ts)
    quantity index = 6
    added_ts index = 10
    """
    if mode == "id_asc":
        return sorted(rows, key=lambda r: r[0])

    if mode == "id_desc":
        return sorted(rows, key=lambda r: r[0], reverse=True)

    if mode == "qty_asc":
        return sorted(rows, key=lambda r: r[6])

    if mode == "qty_desc":
        return sorted(rows, key=lambda r: r[6], reverse=True)

    if mode == "brand_size":
        return sorted(rows, key=lambda r: (r[1].lower(), r[3].lower()))

    with_ts = [r for r in rows if r[10] is not None]
    without_ts = [r for r in rows if r[10] is None]

    if mode == "oldest":
        with_ts_sorted = sorted(with_ts, key=lambda r: r[10])
        return with_ts_sorted + without_ts

    # default newest
    with_ts_sorted = sorted(with_ts, key=lambda r: r[10], reverse=True)
    return with_ts_sorted + without_ts


def sort_label(mode):
    return {
        "id_asc": "ID ascending",
        "id_desc": "ID descending",
        "qty_asc": "Quantity ascending",
        "qty_desc": "Quantity descending",
        "newest": "Newest first (added time)",
        "oldest": "Oldest first (added time)",
        "brand_size": "Brand, size",
    }.get(mode, "Newest first (added time)")


def change_sort(current_sort: str) -> str:
    from utils import clear_screen

    while True:
        clear_screen()
        print("=== CHANGE SORT ===\n")
        print(f"Current sort: {sort_label(current_sort)}\n")
        print("1) ID ascending")
        print("2) ID descending")
        print("3) Newest first (added time)")
        print("4) Oldest first (added time)")
        print("5) Brand, size")
        print("6) Quantity ascending")
        print("7) Quantity descending")
        print("0) Keep current\n")

        choice = input("Select sort (0-7): ").strip()

        if choice == "1":
            return "id_asc"
        elif choice == "2":
            return "id_desc"
        elif choice == "3":
            return "newest"
        elif choice == "4":
            return "oldest"
        elif choice == "5":
            return "brand_size"
        elif choice == "6":
            return "qty_asc"
        elif choice == "7":
            return "qty_desc"
        elif choice == "0" or choice == "":
            return current_sort