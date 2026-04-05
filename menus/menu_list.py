from utils import clear_screen, pause
from .sorting import sort_rows, sort_label, change_sort


def list_tyres(db):
    clear_screen()
    print("=== TYRE LIST / SEARCH ===\n")

    sku = input("Tyre SKU: ").strip()
    brand = input("Brand (or empty): ").strip()
    search = input("Search (size / description / service description): ").strip()

    rows = db.search_tyres(sku, brand, search)
    total = len(rows)
    if total == 0:
        clear_screen()
        print("=== RESULTS ===\n")
        print("No tyres found.")
        pause()
        return

    current_sort = "newest"
    rows = sort_rows(rows, current_sort)

    page_size = 25
    page = 0

    filter_sku = sku if sku else "ANY"
    filter_brand = brand if brand else "ANY"
    filter_search = search if search else "NONE"

    while True:
        clear_screen()
        max_page = (total - 1) // page_size + 1
        print(f"=== RESULTS (page {page + 1}/{max_page}) ===\n")
        print(
            f"Filter: sku={filter_sku} | brand={filter_brand} | search={filter_search}\n"
            f"Sort:   {sort_label(current_sort)}\n"
        )

        start = page * page_size
        end = start + page_size
        chunk = rows[start:end]

        print(
            f"{'ID':<4} {'Brand':<10} {'SKU':<10} "
            f"{'Size':<12} {'Type':<8} {'Pattern':<10} "
            f"{'Qty':<5} {'Price':>8} {'Added':<16}"
        )
        print("-" * 90)

        for rid, brand, sku, size, tyre_type, pattern, qty, price, desc, service_desc, added_ts in chunk:
            size_s = size if len(size) <= 12 else size[:9] + "..."
            pattern_s = (pattern or "")[:]
            if len(pattern_s) > 10:
                pattern_s = pattern_s[:7] + "..."
            desc_s = (desc or "")
            if len(desc_s) > 60:
                desc_s = desc_s[:57] + "..."
            service_desc_s = (service_desc or "")
            if len(service_desc_s) > 60:
                service_desc_s = service_desc_s[:57] + "..."
            added_s = (added_ts or "")[:16]

            print(
                f"{rid:<4} {brand[:10]:<10} {sku:<10} "
                f"{size_s:<12} {tyre_type[:8]:<8} {pattern_s:<10} "
                f"{qty:<5} {price:>8.2f} {added_s:<16}"
            )
            if desc_s:
                print(f"     desc:    {desc_s}")
            if service_desc_s:
                print(f"     service: {service_desc_s}")
            print("-" * 90)

        print("\nCommands:")
        print("  n = next page")
        print("  p = previous page")
        print("  s = change sort")
        print("  0 or ENTER = back to menu")
        choice = input("Or enter tyre ID to open: ").strip().lower()

        if choice == "n":
            if (page + 1) * page_size < total:
                page += 1
            continue
        elif choice == "p":
            if page > 0:
                page -= 1
            continue
        elif choice == "s":
            current_sort = change_sort(current_sort)
            rows = sort_rows(rows, current_sort)
            page = 0
            continue
        elif choice == "" or choice == "0":
            return
        elif choice.isdigit():
            from .menu_detail import tyre_detail
            tyre_detail(db, int(choice))
            return