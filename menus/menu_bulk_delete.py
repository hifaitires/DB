# menus/menu_bulk_delete.py
from utils import clear_screen, pause


def parse_id_list(spec: str):
    ids = set()
    parts = spec.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                a, b = part.split("-", 1)
                start = int(a.strip())
                end = int(b.strip())
            except ValueError:
                continue
            if start > end:
                start, end = end, start
            for i in range(start, end + 1):
                if i > 0:
                    ids.add(i)
        else:
            try:
                val = int(part)
                if val > 0:
                    ids.add(val)
            except ValueError:
                continue
    return sorted(ids)


def bulk_delete(db):
    clear_screen()
    print("=== BULK DELETE TYRES ===\n")
    print("You can enter:")
    print("  Single IDs:       1,5,7")
    print("  Ranges:           1-50")
    print("  Mix of both:      1,3-5,10\n")

    spec = input("Enter IDs / ranges to delete: ").strip()
    if not spec:
        print("No input given.")
        pause()
        return

    ids = parse_id_list(spec)
    if not ids:
        print("No valid IDs found in input.")
        pause()
        return

    # Preview what will be deleted
    conn = db.get_conn()
    cur = conn.cursor()
    placeholders = ",".join("?" for _ in ids)
    cur.execute(
        f"""
        SELECT id, brand, sku, size
        FROM tyres
        WHERE id IN ({placeholders});
        """,
        ids,
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("None of the given IDs exist.")
        pause()
        return

    print("\nThe following tyres will be deleted:\n")
    print(f"{'ID':<4} {'Brand':<12} {'SKU':<12} {'Size':<20}")
    print("-" * 60)
    existing_ids = []
    for tid, brand, sku, size in rows:
        print(f"{tid:<4} {brand[:11]:<12} {sku[:11]:<12} {size:<20}")
        existing_ids.append(tid)

    missing = [i for i in ids if i not in existing_ids]
    if missing:
        print("\nThese IDs were not found and will be ignored:")
        print(", ".join(str(i) for i in missing))

    print(f"\nTotal to delete: {len(existing_ids)}")
    confirm = input("Type YES to confirm bulk delete: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        pause()
        return

    db.log_bulk_delete_and_delete(existing_ids)
    print(f"Deleted {len(existing_ids)} tyres.")
    pause()
