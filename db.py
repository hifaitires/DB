import sqlite3
import os
import csv


class TyreDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def get_conn(self):
        return sqlite3.connect(self.db_path, timeout=5.0)

    def init_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tyres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT NOT NULL,
                brand TEXT NOT NULL,
                size TEXT NOT NULL,
                tyre_type TEXT NOT NULL,
                pattern TEXT,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                service_description TEXT,
                added_ts TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tyre_id INTEGER,
                action TEXT NOT NULL,
                sku TEXT,
                brand TEXT,
                size TEXT,
                tyre_type TEXT,
                pattern TEXT,
                quantity INTEGER,
                price REAL,
                description TEXT,
                service_description TEXT,
                ts TEXT DEFAULT (datetime('now','localtime'))
            );
            """
        )

        cur.execute("PRAGMA table_info(tyres);")
        cols = [row[1] for row in cur.fetchall()]
        if "added_ts" not in cols:
            cur.execute("ALTER TABLE tyres ADD COLUMN added_ts TEXT;")
        if "service_description" not in cols:
            cur.execute("ALTER TABLE tyres ADD COLUMN service_description TEXT;")

        cur.execute("PRAGMA table_info(logs);")
        log_cols = [row[1] for row in cur.fetchall()]
        if "service_description" not in log_cols:
            cur.execute("ALTER TABLE logs ADD COLUMN service_description TEXT;")

        conn.commit()
        conn.close()

    def insert_tyre(self, sku, brand, size, tyre_type, pattern, quantity, price, description, service_description):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO tyres (
                sku, brand, size, tyre_type, pattern, quantity, price,
                description, service_description, added_ts
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'));
            """,
            (sku, brand, size, tyre_type, pattern, quantity, price, description, service_description),
        )
        tyre_id = cur.lastrowid
        conn.commit()
        conn.close()
        return tyre_id

    def get_tyre(self, tyre_id: int):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, sku, brand, size, tyre_type, pattern, quantity, price,
                   description, service_description, added_ts
            FROM tyres
            WHERE id = ?;
            """,
            (tyre_id,),
        )
        row = cur.fetchone()
        conn.close()
        return row

    def update_tyre(self, tyre_id, sku, brand, size, tyre_type, pattern, quantity, price, description, service_description):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE tyres
            SET sku = ?,
                brand = ?,
                size = ?,
                tyre_type = ?,
                pattern = ?,
                quantity = ?,
                price = ?,
                description = ?,
                service_description = ?
            WHERE id = ?;
            """,
            (sku, brand, size, tyre_type, pattern, quantity, price, description, service_description, tyre_id),
        )
        conn.commit()
        conn.close()

    def update_quantity(self, tyre_id, new_qty):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE tyres SET quantity = ? WHERE id = ?;",
            (new_qty, tyre_id),
        )
        conn.commit()
        conn.close()

    def delete_tyre(self, tyre_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM tyres WHERE id = ?;", (tyre_id,))
        conn.commit()
        conn.close()

    def log_action(self, tyre_id, action):
        tyre = self.get_tyre(tyre_id)

        conn = self.get_conn()
        cur = conn.cursor()

        if tyre:
            tid, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc, added_ts = tyre
            cur.execute(
                """
                INSERT INTO logs (
                    tyre_id, action, sku, brand, size, tyre_type, pattern,
                    quantity, price, description, service_description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (tid, action, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc),
            )
        else:
            cur.execute(
                """
                INSERT INTO logs (tyre_id, action)
                VALUES (?, ?);
                """,
                (tyre_id, action),
            )

        conn.commit()
        conn.close()

    def search_tyres(self, sku, brand, search_text):
        query = """
            SELECT id, brand, sku, size, tyre_type, pattern, quantity, price,
                   description, service_description, added_ts
            FROM tyres
            WHERE 1=1
        """
        params = []

        if sku and sku.lower() != "all":
            if len(sku) == 2:
                query += " AND LOWER(sku) LIKE LOWER(?)"
                params.append(f"%{sku}")
            else:
                query += " AND LOWER(sku) = LOWER(?)"
                params.append(sku)

        if brand:
            query += " AND LOWER(brand) = LOWER(?)"
            params.append(brand)

        if search_text:
            like = f"%{search_text}%"
            query += """
                AND (
                    LOWER(size) LIKE LOWER(?)
                    OR LOWER(description) LIKE LOWER(?)
                    OR LOWER(service_description) LIKE LOWER(?)
                )
            """
            params.extend([like, like, like])

        query += " ORDER BY added_ts DESC;"

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_logs_latest(self, limit=200):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, ts, action, tyre_id, brand, sku, quantity, price
            FROM logs
            ORDER BY ts DESC, id DESC
            LIMIT ?;
            """,
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()
        return rows

    def export_csv(self, path):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT sku, brand, size, tyre_type, pattern, quantity, price, description, service_description
            FROM tyres
            ORDER BY id ASC;
            """
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return 0

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "sku", "brand", "size", "tyre_type", "pattern",
                "quantity", "price", "description", "service_description"
            ])
            writer.writerows(rows)

        return len(rows)

    def import_csv(self, path):
        if not os.path.exists(path):
            return -1

        with open(path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            if not reader.fieldnames:
                return -2

            required = ["sku", "brand", "size", "tyre_type", "pattern", "quantity", "price", "description"]
            if any(col not in reader.fieldnames for col in required):
                return -3

            conn = self.get_conn()
            cur = conn.cursor()
            count = 0

            for row in reader:
                try:
                    cur.execute(
                        """
                        INSERT INTO tyres (
                            sku, brand, size, tyre_type, pattern, quantity, price,
                            description, service_description, added_ts
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'));
                        """,
                        (
                            row["sku"].strip(),
                            row["brand"].strip(),
                            row["size"].strip(),
                            row["tyre_type"].strip(),
                            row["pattern"].strip(),
                            int(row["quantity"]),
                            float(str(row["price"]).replace(",", ".")),
                            row["description"].strip(),
                            row.get("service_description", "").strip(),
                        ),
                    )
                    count += 1
                except Exception:
                    continue

            conn.commit()
            conn.close()
            return count

    def log_bulk_delete_and_delete(self, tyre_ids):
        if not tyre_ids:
            return

        conn = self.get_conn()
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in tyre_ids)

        cur.execute(
            f"""
            SELECT id, sku, brand, size, tyre_type, pattern, quantity, price, description, service_description
            FROM tyres
            WHERE id IN ({placeholders});
            """,
            tyre_ids,
        )
        rows = cur.fetchall()

        for tid, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc in rows:
            cur.execute(
                """
                INSERT INTO logs (
                    tyre_id, action, sku, brand, size, tyre_type, pattern,
                    quantity, price, description, service_description
                )
                VALUES (?, 'DELETE', ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (tid, sku, brand, size, tyre_type, pattern, qty, price, desc, service_desc),
            )

        cur.execute(f"DELETE FROM tyres WHERE id IN ({placeholders});", tyre_ids)

        conn.commit()
        conn.close()