# menus/menu_logs.py
from utils import clear_screen, pause


def view_logs(db):
    clear_screen()
    print("=== VIEW LOGS (LATEST 200) ===\n")

    rows = db.get_logs_latest(limit=200)
    if not rows:
        print("No log entries.")
        pause()
        return

    print(f"{'LogID':<6} {'Time':<19} {'Action':<10} {'TID':<4} "
          f"{'Brand':<10} {'SKU':<10} {'Qty':<5} {'Price':>8}")
    print("-" * 90)

    for log_id, ts, action, tyre_id, brand, sku, qty, price in rows:
        brand_s = (brand or "")[:10]
        sku_s = (sku or "")[:10]
        qty_s = "" if qty is None else str(qty)
        price_s = "" if price is None else f"{price:>8.2f}"
        print(
            f"{log_id:<6} {ts:<19} {action[:9]:<10} {str(tyre_id or ''):<4} "
            f"{brand_s:<10} {sku_s:<10} {qty_s:<5} {price_s}"
        )

    pause()
