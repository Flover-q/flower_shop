import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "flower.db")


def _connect():
    """Открывает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def _column_exists(cur, table, column):
    """Проверяет, есть ли столбец в таблице."""
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def init_db():
    """Создаёт таблицы, если их ещё нет, и заполняет цветы/упаковки."""
    with _connect() as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                preferences TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bouquets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                flowers TEXT,
                pack TEXT,
                size TEXT,
                work TEXT,
                total TEXT,
                cost TEXT,
                sold INTEGER DEFAULT 0,
                count INTEGER DEFAULT 1,
                initial_count INTEGER DEFAULT 1
            )
        """)

        if not _column_exists(cur, "bouquets", "sold"):
            cur.execute(
                "ALTER TABLE bouquets ADD COLUMN sold INTEGER DEFAULT 0"
            )

        if not _column_exists(cur, "bouquets", "count"):
            cur.execute(
                "ALTER TABLE bouquets ADD COLUMN count INTEGER DEFAULT 1"
            )

        if not _column_exists(cur, "bouquets", "initial_count"):
            cur.execute(
                "ALTER TABLE bouquets ADD COLUMN initial_count INTEGER DEFAULT 1"
            )
            cur.execute(
                "UPDATE bouquets SET initial_count = count "
                "WHERE initial_count IS NULL"
            )

        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                number TEXT NOT NULL,
                bouquet TEXT,
                ready INTEGER DEFAULT 0,
                sold INTEGER DEFAULT 0,
                total INTEGER DEFAULT 0
            )
        """)

        if not _column_exists(cur, "orders", "sold"):
            cur.execute(
                "ALTER TABLE orders ADD COLUMN sold INTEGER DEFAULT 0"
            )

        if not _column_exists(cur, "orders", "total"):
            cur.execute(
                "ALTER TABLE orders ADD COLUMN total INTEGER DEFAULT 0"
            )

        cur.execute("""
            CREATE TABLE IF NOT EXISTS spisaniya (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                flower TEXT NOT NULL,
                count INTEGER,
                reason TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                bouquets INTEGER DEFAULT 0,
                profit INTEGER DEFAULT 0,
                spisano INTEGER DEFAULT 0
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS flowers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS packs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                size TEXT NOT NULL,
                price REAL NOT NULL,
                UNIQUE(name, size)
            )
        """)

        cur.execute("SELECT COUNT(*) FROM flowers")
        if cur.fetchone()[0] == 0:
            default_flowers = [
                ("Роза",       150),
                ("Тюльпан",     80),
                ("Хризантема", 120),
                ("Гербера",    130),
                ("Лилия",      250),
                ("Гвоздика",    70),
                ("Пион",       350),
                ("Ирис",       110),
                ("Фрезия",     140),
                ("Альстромерия", 160),
                ("Ромашка",     60),
                ("Лаванда",     90),
                ("Эустома",    180),
                ("Орхидея",    400),
                ("Гладиолус",  130),
            ]
            cur.executemany(
                "INSERT INTO flowers (name, price) VALUES (?, ?)",
                default_flowers
            )

        cur.execute("SELECT COUNT(*) FROM packs")
        if cur.fetchone()[0] == 0:
            default_packs = [
                ("Плёнка", "Маленький",  50),
                ("Плёнка", "Средний",   100),
                ("Плёнка", "Большой",   150),
                ("Бумага", "Маленький", 100),
                ("Бумага", "Средний",   200),
                ("Бумага", "Большой",   300),
                ("Коробка", "Маленький", 200),
                ("Коробка", "Средний",   400),
                ("Коробка", "Большой",   600),
            ]
            cur.executemany(
                "INSERT INTO packs (name, size, price) VALUES (?, ?, ?)",
                default_packs
            )

        con.commit()

    try:
        fix_orders_total()
    except Exception:
        pass


# ─── КЛИЕНТЫ ───────────────────────────────────────────────
def get_clients():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT name, phone, preferences FROM clients")
        rows = cur.fetchall()
    return [{"name": r[0], "phone": r[1], "preferences": r[2] or ""}
            for r in rows]


def add_client(name, phone, preferences=""):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO clients (name, phone, preferences) VALUES (?, ?, ?)",
            (name, phone, preferences)
        )
        con.commit()


def delete_client(name, phone):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM clients WHERE name = ? AND phone = ?",
            (name, phone)
        )
        con.commit()


# ─── БУКЕТЫ ────────────────────────────────────────────────
def get_bouquets():
    """Возвращает список словарей со всеми букетами."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, date, name, flowers, pack, size, work, total, cost,
                   sold, count, initial_count
            FROM bouquets ORDER BY id DESC
        """)
        rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "date": r[1], "name": r[2], "flowers": r[3] or "",
            "pack": r[4] or "", "size": r[5] or "",
            "work": r[6] or "", "total": r[7] or "", "cost": r[8] or "",
            "sold": bool(r[9]),
            "count": r[10] or 1,
            "initial_count": r[11] if r[11] is not None else (r[10] or 1),
        }
        for r in rows
    ]


def add_bouquet(date, name, flowers, pack, size, work, total, cost,
                sold=0, count=1):
    """Добавляет букет. sold=0 — не продан. count — сколько штук."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO bouquets
            (date, name, flowers, pack, size, work, total, cost, sold, count,
             initial_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, name, flowers, pack, size, work, total, cost, sold,
              count, count))
        con.commit()


def delete_bouquet_by_name(name, date):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM bouquets WHERE name = ? AND date = ?",
            (name, date)
        )
        con.commit()


def toggle_bouquet_sold(bouquet_id):
    """Переключает статус букета: продан / не продан."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE bouquets SET sold = 1 - sold WHERE id = ?",
            (bouquet_id,)
        )
        con.commit()


def update_bouquet_count(bouquet_id, new_count):
    """Меняет количество штук у букета (count)."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE bouquets SET count = ? WHERE id = ?",
            (new_count, bouquet_id)
        )
        con.commit()


def update_bouquet_initial_count(bouquet_id, new_count):
    """Меняет «Было всего» (initial_count) у букета.
    Если букет НЕ продан — синхронизирует и count."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT sold FROM bouquets WHERE id = ?",
            (bouquet_id,)
        )
        row = cur.fetchone()
        if row is None:
            return

        sold = row[0]

        if sold:
            cur.execute(
                "UPDATE bouquets SET initial_count = ? WHERE id = ?",
                (new_count, bouquet_id)
            )
        else:
            cur.execute(
                "UPDATE bouquets SET initial_count = ?, count = ? "
                "WHERE id = ?",
                (new_count, new_count, bouquet_id)
            )
        con.commit()


def count_unsold_bouquets():
    """Сколько букетов сейчас в наличии (сумма count у не проданных)."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT COALESCE(SUM(count), 0) FROM bouquets WHERE sold = 0"
        )
        return cur.fetchone()[0] or 0


def count_bouquets_total():
    """Сколько всего букетов собрано (сумма initial_count)."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT COALESCE(SUM(initial_count), 0) FROM bouquets")
        return cur.fetchone()[0] or 0


def count_unsold_by_name(name):
    """Сколько таких же букетов по названию сейчас не продано.
    Сравнение без учёта регистра."""
    if not name:
        return 0
    clean = name.strip().lower()
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT COALESCE(SUM(count), 0) FROM bouquets "
            "WHERE LOWER(TRIM(name)) = ? AND sold = 0",
            (clean,)
        )
        return cur.fetchone()[0] or 0


def get_bouquet_total_by_name(name):
    """Возвращает стоимость (total) последнего собранного букета с таким именем.
    Сравнение без учёта регистра. Если букетов нет — 0."""
    if not name:
        return 0
    clean = name.strip().lower()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT total FROM bouquets
            WHERE LOWER(TRIM(name)) = ?
            ORDER BY id DESC
            LIMIT 1
        """, (clean,))
        row = cur.fetchone()
        if row is None or row[0] in (None, ""):
            return 0
        try:
            return int(float(row[0]))
        except (TypeError, ValueError):
            return 0


def get_bouquets_stats(date_from, date_to):
    """Статистика букетов за период: собрано, продано, прибыль."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT
                COALESCE(SUM(initial_count), 0),
                COALESCE(SUM(CASE WHEN sold = 1 THEN initial_count ELSE 0 END), 0)
            FROM bouquets
            WHERE date BETWEEN ? AND ?
        """, (date_from, date_to))
        row = cur.fetchone()
        collected = row[0] or 0
        sold_count = row[1] or 0

        cur.execute("""
            SELECT COALESCE(SUM(CAST(total AS REAL) * initial_count), 0)
            FROM bouquets
            WHERE date BETWEEN ? AND ? AND sold = 1
        """, (date_from, date_to))
        profit = int(cur.fetchone()[0] or 0)

    return {
        "collected": collected,
        "sold":      sold_count,
        "profit":    profit,
    }


def get_spisano_stats(date_from, date_to):
    """Сколько списано за период."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(count), 0)
            FROM spisaniya
            WHERE date BETWEEN ? AND ?
        """, (date_from, date_to))
        return cur.fetchone()[0] or 0


def get_profit_by_day(date_from, date_to):
    """Возвращает словарь {date: profit} для графика (по букетам)."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT date, COALESCE(SUM(CAST(total AS REAL) * initial_count), 0)
            FROM bouquets
            WHERE date BETWEEN ? AND ? AND sold = 1
            GROUP BY date
            ORDER BY date
        """, (date_from, date_to))
        rows = cur.fetchall()
    return {r[0]: int(r[1] or 0) for r in rows}


def get_orders_stats(date_from, date_to):
    """
    Статистика заказов за период: продано, прибыль.

    Прибыль: если у заказа есть total — берём его.
    Если total = 0 — берём стоимость связанного букета.
    """
    with _connect() as con:
        cur = con.cursor()

        cur.execute("""
            SELECT COUNT(*) FROM orders
            WHERE date BETWEEN ? AND ? AND sold = 1
        """, (date_from, date_to))
        sold = cur.fetchone()[0] or 0

        cur.execute("""
            SELECT COALESCE(SUM(total), 0) FROM orders
            WHERE date BETWEEN ? AND ? AND sold = 1 AND total > 0
        """, (date_from, date_to))
        profit_with_total = int(cur.fetchone()[0] or 0)

        cur.execute("""
            SELECT id, bouquet FROM orders
            WHERE date BETWEEN ? AND ? AND sold = 1
                  AND (total = 0 OR total IS NULL)
        """, (date_from, date_to))
        rows = cur.fetchall()

        profit_from_bouquets = 0
        for order_id, bouquet in rows:
            if not bouquet:
                continue
            cur.execute("""
                SELECT total FROM bouquets
                WHERE LOWER(TRIM(name)) = ?
                ORDER BY id DESC
                LIMIT 1
            """, (bouquet.strip().lower(),))
            b = cur.fetchone()
            if b is None or b[0] in (None, ""):
                continue
            try:
                profit_from_bouquets += int(float(b[0]))
            except (TypeError, ValueError):
                pass

    return {
        "sold":   sold,
        "profit": profit_with_total + profit_from_bouquets,
    }


def get_orders_profit_by_day(date_from, date_to):
    """{date: profit} по проданным заказам за период."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT date, COALESCE(SUM(total), 0)
            FROM orders
            WHERE date BETWEEN ? AND ? AND sold = 1
            GROUP BY date
            ORDER BY date
        """, (date_from, date_to))
        rows = cur.fetchall()
    return {r[0]: int(r[1] or 0) for r in rows}


def get_orders_sold_by_day(date_from, date_to):
    """{date: count} по проданным заказам за период."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT date, COUNT(*)
            FROM orders
            WHERE date BETWEEN ? AND ? AND sold = 1
            GROUP BY date
            ORDER BY date
        """, (date_from, date_to))
        rows = cur.fetchall()
    return {r[0]: int(r[1] or 0) for r in rows}


def sell_bouquet_by_name(name):
    """
    Уменьшает count на 1 у первого не проданного букета с таким названием.
    Сравнение без учёта регистра.
    Если count станет 0 — помечает букет как проданный.
    initial_count НЕ трогает.
    Возвращает True, если удалось.
    """
    if not name:
        return False
    clean = name.strip().lower()
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, count FROM bouquets
            WHERE LOWER(TRIM(name)) = ? AND sold = 0
            ORDER BY id
            LIMIT 1
        """, (clean,))
        row = cur.fetchone()
        if row is None:
            return False

        bouquet_id, cnt = row
        cnt = (cnt or 1) - 1

        if cnt <= 0:
            cur.execute(
                "UPDATE bouquets SET count = 0, sold = 1 WHERE id = ?",
                (bouquet_id,)
            )
        else:
            cur.execute(
                "UPDATE bouquets SET count = ? WHERE id = ?",
                (cnt, bouquet_id)
            )
        con.commit()
        return True


def mark_order_ready_by_name(name):
    """
    Устаревшая функция — оставлена для совместимости.
    Проксирует на sync_orders_by_bouquet_name.
    """
    return sync_orders_by_bouquet_name(name) > 0


# ─── СИНХРОНИЗАЦИЯ ЗАКАЗОВ И БУКЕТОВ ───────────────────────
def sync_orders_by_bouquet_name(name):
    """
    Обновляет статусы заказов с таким названием букета по состоянию букетов.
    """
    if not name:
        return 0

    clean_name = name.strip().lower()

    with _connect() as con:
        cur = con.cursor()

        cur.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN sold = 0 THEN 1 ELSE 0 END), 0),
                COALESCE(COUNT(*), 0)
            FROM bouquets
            WHERE LOWER(TRIM(name)) = ?
        """, (clean_name,))
        row = cur.fetchone()
        unsold = row[0] or 0
        total = row[1] or 0

        if total > 0 and unsold == 0:
            new_ready = 1
            new_sold = 1
        elif unsold > 0:
            new_ready = 1
            new_sold = 0
        else:
            return 0

        cur.execute("""
            SELECT total FROM bouquets
            WHERE LOWER(TRIM(name)) = ?
            ORDER BY id DESC
            LIMIT 1
        """, (clean_name,))
        t_row = cur.fetchone()
        total_value = 0
        if t_row is not None and t_row[0] not in (None, ""):
            try:
                total_value = int(float(t_row[0]))
            except (TypeError, ValueError):
                total_value = 0

        if new_sold == 1:
            cur.execute("""
                UPDATE orders
                SET ready = 1,
                    sold = 1,
                    total = CASE WHEN total = 0 THEN ? ELSE total END
                WHERE LOWER(TRIM(bouquet)) = ? AND sold = 0
            """, (total_value, clean_name))
        else:
            cur.execute("""
                UPDATE orders
                SET ready = 1,
                    sold = 0,
                    total = CASE WHEN total = 0 THEN ? ELSE total END
                WHERE LOWER(TRIM(bouquet)) = ? AND ready = 0 AND sold = 0
            """, (total_value, clean_name))

        con.commit()
        return cur.rowcount


def sync_all_orders():
    """Синхронизирует статусы всех заказов по их букетам."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT bouquet FROM orders")
        names = [r[0] for r in cur.fetchall() if r[0]]

    total = 0
    for name in names:
        total += sync_orders_by_bouquet_name(name)
    return total


# ─── ДОСЧЁТ СТОИМОСТИ ЗАКАЗОВ ──────────────────────────────
def fix_orders_total():
    """Проставляет total всем заказам, у которых total = 0."""
    with _connect() as con:
        cur = con.cursor()

        cur.execute("""
            SELECT id, bouquet FROM orders
            WHERE total = 0 OR total IS NULL
        """)
        rows = cur.fetchall()

        updated = 0
        for order_id, bouquet in rows:
            if not bouquet:
                continue

            cur.execute("""
                SELECT total FROM bouquets
                WHERE LOWER(TRIM(name)) = ?
                ORDER BY id DESC
                LIMIT 1
            """, (bouquet.strip().lower(),))
            b = cur.fetchone()
            if b is None or b[0] in (None, ""):
                continue

            try:
                value = int(float(b[0]))
            except (TypeError, ValueError):
                continue

            cur.execute(
                "UPDATE orders SET total = ? WHERE id = ?",
                (value, order_id)
            )
            updated += 1

        con.commit()
        return updated


# ─── ЗАКАЗЫ (КАЛЕНДАРЬ) ────────────────────────────────────
def get_orders_by_date(date_str):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, name, number, bouquet, ready, sold
            FROM orders WHERE date = ?
        """, (date_str,))
        rows = cur.fetchall()
    return [
        {"id": r[0], "name": r[1], "number": r[2],
         "bouquet": r[3] or "", "ready": bool(r[4]),
         "sold": bool(r[5])}
        for r in rows
    ]


def get_orders_all():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT date, id, name, number, bouquet, ready, sold
            FROM orders
        """)
        rows = cur.fetchall()

    result = {}
    for r in rows:
        date_str = r[0]
        result.setdefault(date_str, []).append({
            "id": r[1], "name": r[2], "number": r[3],
            "bouquet": r[4] or "", "ready": bool(r[5]),
            "sold": bool(r[6])
        })
    return result


def add_order(date_str, name, number, bouquet, ready=False, total=0):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO orders (date, name, number, bouquet, ready, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date_str, name, number, bouquet, 1 if ready else 0, total))
        con.commit()


def delete_order(order_id):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        con.commit()


def toggle_order_status(order_id):
    """
    Переключает статус заказа по кругу:
    В сборке → Готов → Продан → В сборке.
    """
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT ready, sold FROM orders WHERE id = ?",
            (order_id,)
        )
        row = cur.fetchone()
        if row is None:
            return

        ready, sold = row

        if sold:
            cur.execute(
                "UPDATE orders SET ready = 0, sold = 0 WHERE id = ?",
                (order_id,)
            )
        elif ready:
            cur.execute(
                "UPDATE orders SET sold = 1 WHERE id = ?",
                (order_id,)
            )
        else:
            cur.execute(
                "UPDATE orders SET ready = 1 WHERE id = ?",
                (order_id,)
            )
        con.commit()


def set_order_sold(order_id):
    """Помечает заказ как «Продан» (ready=1, sold=1)."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            UPDATE orders
            SET ready = 1, sold = 1
            WHERE id = ?
        """, (order_id,))
        con.commit()


# ─── СПИСАНИЯ ──────────────────────────────────────────────
def get_spisaniya(date_from, date_to):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT date, flower, count, reason
            FROM spisaniya
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """, (date_from, date_to))
        rows = cur.fetchall()

        # забираем цены цветов один раз
        cur.execute("SELECT name, price FROM flowers")
        prices = {r[0]: r[1] for r in cur.fetchall()}

    result = []
    for r in rows:
        flower = r[1]
        count = r[2] or 0
        price = prices.get(flower, 0)
        loss = int(price * count)

        result.append({
            "date": r[0],
            "flower": flower,
            "count": count,
            "reason": r[3],
            "price": price,
            "loss": loss,
        })
    return result


def add_spisanie(date_str, flower, count, reason):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO spisaniya (date, flower, count, reason)
            VALUES (?, ?, ?, ?)
        """, (date_str, flower, count, reason))
        con.commit()


# ─── АНАЛИТИКА ─────────────────────────────────────────────
def get_analytics(date_from, date_to):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT
                COALESCE(SUM(bouquets), 0),
                COALESCE(SUM(profit), 0),
                COALESCE(SUM(spisano), 0)
            FROM analytics
            WHERE date BETWEEN ? AND ?
        """, (date_from, date_to))
        row = cur.fetchone()
    return {
        "bouquets": row[0],
        "profit":   row[1],
        "spisano":  row[2],
    }


def add_analytics(date_str, bouquets=0, profit=0, spisano=0):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO analytics (date, bouquets, profit, spisano)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                bouquets = bouquets + excluded.bouquets,
                profit   = profit   + excluded.profit,
                spisano  = spisano  + excluded.spisano
        """, (date_str, bouquets, profit, spisano))
        con.commit()


# ─── ЦВЕТЫ ─────────────────────────────────────────────────
def get_flowers():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT name, price FROM flowers ORDER BY name")
        rows = cur.fetchall()
    return {r[0]: r[1] for r in rows}


def add_flower(name, price):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO flowers (name, price) VALUES (?, ?)",
            (name, price)
        )
        con.commit()


def delete_flower(name):
    with _connect() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM flowers WHERE name = ?", (name,))
        con.commit()


def update_flower_price(name, new_price):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE flowers SET price = ? WHERE name = ?",
            (new_price, name)
        )
        con.commit()


# ─── УПАКОВКИ ──────────────────────────────────────────────
def get_packs():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT name, size, price FROM packs")
        rows = cur.fetchall()
    return {(r[0], r[1]): r[2] for r in rows}


def get_pack_names():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT name FROM packs ORDER BY name")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def get_pack_sizes():
    with _connect() as con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT size FROM packs ORDER BY size")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def add_pack(name, size, price):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO packs (name, size, price) VALUES (?, ?, ?)",
            (name, size, price)
        )
        con.commit()


def delete_pack(name, size):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM packs WHERE name = ? AND size = ?",
            (name, size)
        )
        con.commit()


def update_pack_price(name, size, new_price):
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE packs SET price = ? WHERE name = ? AND size = ?",
            (new_price, name, size)
        )
        con.commit()