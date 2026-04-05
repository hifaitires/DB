from utils import clear_screen, pause


def tyre_detail(db, tyre_id: int):
    tyre = db.get_tyre(tyre_id)
    if not tyre:
        print("Tyre not found.")
        pause()
        return

    while True:
        clear_screen()
        tid, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc, added_ts = tyre
        print("=== TYRE DETAIL ===\n")
        print(f"ID:                  {tid}")
        print(f"SKU:                 {sku}")
        print(f"Brand:               {brand}")
        print(f"Size:                {size}")
        print(f"Type:                {tyre_type}")
        print(f"Pattern:             {pattern}")
        print(f"Quantity:            {qty}")
        print(f"Price:               {price:.2f}")
        print(f"Description:         {desc}")
        print(f"Service Description: {service_desc}")
        print(f"Added time:          {added_ts}\n")

        print("1) Edit")
        print("2) Change quantity")
        print("3) Delete")
        print("0) Back")

        c = input("Select: ").strip()

        if c == "1":
            edit_tyre(db, tyre_id)
            tyre = db.get_tyre(tyre_id)
        elif c == "2":
            change_quantity(db, tyre_id)
            tyre = db.get_tyre(tyre_id)
        elif c == "3":
            delete_tyre(db, tyre_id)
            return
        elif c == "0":
            return


def edit_tyre(db, tyre_id: int):
    tyre = db.get_tyre(tyre_id)
    if not tyre:
        return

    tid, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc, added_ts = tyre

    clear_screen()
    print("=== EDIT TYRE ===\n")
    print("Leave empty to keep current value.\n")

    new_sku = input(f"SKU [{sku}]: ").strip() or sku
    new_brand = input(f"Brand [{brand}]: ").strip() or brand
    new_size = input(f"Size [{size}]: ").strip() or size
    new_type = input(f"Type [{tyre_type}]: ").strip() or tyre_type
    new_pattern = input(f"Pattern [{pattern}]: ").strip() or pattern

    while True:
        q = input(f"Quantity [{qty}]: ").strip()
        if not q:
            new_qty = qty
            break
        try:
            new_qty = int(q)
            if new_qty < 0:
                print("Quantity cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number.")

    while True:
        p = input(f"Price [{price}]: ").strip()
        if not p:
            new_price = price
            break
        p_norm = p.replace(",", ".")
        try:
            new_price = float(p_norm)
            break
        except ValueError:
            print("Please enter a valid number (e.g. 79.90).")

    new_desc = input(f"Description [{desc}]: ").strip() or desc
    new_service_desc = input(f"Service Description [{service_desc}]: ").strip() or service_desc

    db.log_action(tyre_id, "UPDATE")
    db.update_tyre(
        tyre_id, new_sku, new_brand, new_size, new_type,
        new_pattern, new_qty, new_price, new_desc, new_service_desc
    )

    print("Updated.")
    pause()


def change_quantity(db, tyre_id: int):
    tyre = db.get_tyre(tyre_id)
    if not tyre:
        return

    qty = tyre[6]

    clear_screen()
    print("=== CHANGE QUANTITY ===\n")
    print(f"Current quantity: {qty}")
    print("Enter +5 / -3 to change relatively, or a new absolute number.\n")

    while True:
        diff = input("Quantity change or new value: ").strip()
        if not diff:
            print("No input given.")
            pause()
            return

        try:
            if diff.startswith("+") or diff.startswith("-"):
                new_qty = qty + int(diff)
            else:
                new_qty = int(diff)
        except ValueError:
            print("Please enter something like +5, -3, or 10.")
            continue

        if new_qty < 0:
            print("Quantity cannot be negative.")
            continue

        break

    db.log_action(tyre_id, "QTY_CHANGE")
    db.update_quantity(tyre_id, new_qty)

    print("Quantity updated.")
    pause()


def delete_tyre(db, tyre_id: int):
    tyre = db.get_tyre(tyre_id)
    if not tyre:
        return

    clear_screen()
    print("=== DELETE TYRE ===\n")
    print(f"Are you sure you want to delete: {tyre[2]} / {tyre[1]} / {tyre[3]}")
    confirm = input("Type YES to confirm: ").strip()

    if confirm != "YES":
        print("Cancelled.")
        pause()
        return

    db.log_action(tyre_id, "DELETE")
    db.delete_tyre(tyre_id)

    print("Deleted.")
    pause()