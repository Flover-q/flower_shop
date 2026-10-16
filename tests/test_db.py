"""
Модульные тесты для db.py.

Проверяют основные функции работы с базой данных:
- создание таблиц
- добавление и чтение цветов
- добавление и чтение букетов
- добавление и чтение заказов
- добавление и чтение клиентов
- упаковка
- отчёты и аналитика
"""

import os
import sys

# чтобы Python видел корень проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db


# ---------- Базовые ----------

def test_init_db():
    """База создаётся, таблицы есть."""
    db.init_db()
    flowers = db.get_flowers()
    assert isinstance(flowers, dict)


def test_add_and_get_flower():
    """Цветок добавляется и находится в списке."""
    db.init_db()
    name = "ТестовыйЦветок"
    db.add_flower(name, 123)
    flowers = db.get_flowers()
    assert name in flowers
    assert flowers[name] == 123
    db.delete_flower(name)


def test_update_flower_price():
    """Цена цветка обновляется."""
    db.init_db()
    name = "ТестовыйЦветок2"
    db.add_flower(name, 100)
    db.update_flower_price(name, 250)
    flowers = db.get_flowers()
    assert flowers[name] == 250
    db.delete_flower(name)


def test_add_and_get_bouquet():
    """Букет добавляется и находится в списке."""
    db.init_db()
    name = "ТестовыйБукет"
    db.add_bouquet(
        "2026-01-01", name, "Роза×1", "Плёнка", "Маленький",
        "50", "200", "150", sold=0, count=1
    )
    bouquets = db.get_bouquets()
    names = [b.get("name") for b in bouquets]
    assert name in names
    db.delete_bouquet_by_name(name, "2026-01-01")


def test_add_and_get_client():
    """Клиент добавляется и находится в списке."""
    db.init_db()
    name = "ТестовыйКлиент"
    phone = "1234567890"
    db.add_client(name, phone, "Розы")
    clients = db.get_clients()
    names = [c.get("name") for c in clients]
    assert name in names
    db.delete_client(name, phone)


def test_count_unsold_bouquets():
    """Счётчик непроданных букетов — число."""
    db.init_db()
    count = db.count_unsold_bouquets()
    assert isinstance(count, int)
    assert count >= 0


def test_add_and_get_spisanie():
    """Списание добавляется и находится."""
    db.init_db()
    db.add_spisanie("2026-01-01", "Роза", 3, "Увядание")
    rows = db.get_spisaniya("2026-01-01", "2026-01-01")
    assert isinstance(rows, list)
    assert any(r["flower"] == "Роза" for r in rows)


# ---------- Упаковка ----------

def test_add_and_get_pack():
    """Упаковка добавляется и читается."""
    db.init_db()
    name, size = "ТестПлёнка", "Маленький"
    db.add_pack(name, size, 100)
    packs = db.get_packs()
    assert (name, size) in packs
    assert packs[(name, size)] == 100
    db.delete_pack(name, size)


def test_update_pack_price():
    """Цена упаковки обновляется."""
    db.init_db()
    name, size = "ТестПлёнка2", "Большой"
    db.add_pack(name, size, 150)
    db.update_pack_price(name, size, 250)
    packs = db.get_packs()
    assert packs[(name, size)] == 250
    db.delete_pack(name, size)


def test_delete_pack():
    """Упаковка удаляется."""
    db.init_db()
    name, size = "ТестПлёнка3", "Средний"
    db.add_pack(name, size, 120)
    db.delete_pack(name, size)
    packs = db.get_packs()
    assert (name, size) not in packs


def test_get_pack_names_and_sizes():
    """Списки имён и размеров упаковки возвращаются."""
    db.init_db()
    db.add_pack("ТестУпак", "XL", 200)
    names = db.get_pack_names()
    sizes = db.get_pack_sizes()
    assert "ТестУпак" in names
    assert "XL" in sizes
    db.delete_pack("ТестУпак", "XL")


# ---------- Заказы ----------

def _find_order_id(orders, name):
    """Вспомогательная функция: найти id заказа по имени."""
    for o in orders:
        if o["name"] == name:
            return o["id"]
    return None


def test_add_and_get_order():
    """Заказ добавляется и читается по дате."""
    db.init_db()
    db.add_order("2026-12-31", "ТестКлиент", "999", "Роза×5")
    orders = db.get_orders_by_date("2026-12-31")
    names = [o["name"] for o in orders]
    assert "ТестКлиент" in names
    oid = _find_order_id(orders, "ТестКлиент")
    if oid:
        db.delete_order(oid)


def test_delete_order():
    """Заказ удаляется по id."""
    db.init_db()
    db.add_order("2026-12-30", "ТестУдаление", "111", "Пион×3")
    orders = db.get_orders_by_date("2026-12-30")
    oid = _find_order_id(orders, "ТестУдаление")
    assert oid is not None

    db.delete_order(oid)
    orders_after = db.get_orders_by_date("2026-12-30")
    names = [o["name"] for o in orders_after]
    assert "ТестУдаление" not in names


def test_toggle_order_status():
    """Статус заказа циклично переключается: В сборке → Готов → Продан → В сборке."""
    db.init_db()
    db.add_order("2026-12-29", "ТестСтатус", "222", "Тюльпан×7")
    orders = db.get_orders_by_date("2026-12-29")
    oid = _find_order_id(orders, "ТестСтатус")

    db.toggle_order_status(oid)
    orders = db.get_orders_by_date("2026-12-29")
    o = [x for x in orders if x["id"] == oid][0]
    assert o["ready"] is True
    assert o["sold"] is False

    db.toggle_order_status(oid)
    orders = db.get_orders_by_date("2026-12-29")
    o = [x for x in orders if x["id"] == oid][0]
    assert o["ready"] is True
    assert o["sold"] is True

    db.toggle_order_status(oid)
    orders = db.get_orders_by_date("2026-12-29")
    o = [x for x in orders if x["id"] == oid][0]
    assert o["ready"] is False
    assert o["sold"] is False

    db.delete_order(oid)


def test_set_order_sold():
    """set_order_sold ставит ready=1, sold=1."""
    db.init_db()
    db.add_order("2026-12-28", "ТестПродан", "333", "Хризантема×10")
    orders = db.get_orders_by_date("2026-12-28")
    oid = _find_order_id(orders, "ТестПродан")

    db.set_order_sold(oid)
    orders = db.get_orders_by_date("2026-12-28")
    o = [x for x in orders if x["id"] == oid][0]
    assert o["ready"] is True
    assert o["sold"] is True

    db.delete_order(oid)


def test_get_orders_all():
    """get_orders_all возвращает словарь по датам."""
    db.init_db()
    db.add_order("2026-11-01", "ТестВсеЗаказы", "444", "Роза×1")
    all_orders = db.get_orders_all()
    assert isinstance(all_orders, dict)
    assert "2026-11-01" in all_orders
    orders = all_orders["2026-11-01"]
    oid = _find_order_id(orders, "ТестВсеЗаказы")
    if oid:
        db.delete_order(oid)


# ---------- Отчёты и аналитика ----------

def test_get_bouquets_stats():
    """Сводка по букетам: собрано, продано, прибыль."""
    db.init_db()
    df, dt = "2020-01-01", "2030-12-31"

    db.add_bouquet(
        "2026-06-01", "ТестБукет1", "Роза×5", "Плёнка", "M",
        "200", "1500", "800", sold=1, count=2
    )
    db.add_bouquet(
        "2026-06-01", "ТестБукет2", "Пион×3", "Бумага", "L",
        "300", "2000", "1200", sold=0, count=1
    )

    stats = db.get_bouquets_stats(df, dt)
    assert isinstance(stats, dict)
    assert "collected" in stats
    assert "sold" in stats
    assert "profit" in stats
    assert stats["collected"] >= 3
    assert stats["sold"] >= 2

    db.delete_bouquet_by_name("ТестБукет1", "2026-06-01")
    db.delete_bouquet_by_name("ТестБукет2", "2026-06-01")


def test_get_spisano_stats():
    """Сколько списано за период."""
    db.init_db()
    df, dt = "2020-01-01", "2030-12-31"

    db.add_spisanie("2026-07-15", "Роза", 7, "Увядание")
    db.add_spisanie("2026-07-16", "Пион", 3, "Бой")

    total = db.get_spisano_stats(df, dt)
    assert isinstance(total, int)
    assert total >= 10


def test_get_profit_by_day():
    """Прибыль по дням — словарь {дата: сумма}."""
    db.init_db()
    df, dt = "2020-01-01", "2030-12-31"

    db.add_bouquet(
        "2026-08-01", "ТестПрибыль1", "Роза×5", "Плёнка", "M",
        "200", "1000", "500", sold=1, count=2
    )
    db.add_bouquet(
        "2026-08-02", "ТестПрибыль2", "Пион×3", "Бумага", "L",
        "300", "1500", "700", sold=1, count=1
    )

    profit = db.get_profit_by_day(df, dt)
    assert isinstance(profit, dict)
    assert "2026-08-01" in profit
    assert "2026-08-02" in profit
    assert profit["2026-08-01"] >= 2000
    assert profit["2026-08-02"] >= 1500

    db.delete_bouquet_by_name("ТестПрибыль1", "2026-08-01")
    db.delete_bouquet_by_name("ТестПрибыль2", "2026-08-02")


def test_get_analytics():
    """get_analytics возвращает словарь со сводкой."""
    db.init_db()
    df, dt = "2020-01-01", "2030-12-31"

    # get_analytics читает из таблицы analytics,
    # поэтому используем add_analytics — как в реальном приложении
    db.add_analytics("2026-09-10", bouquets=5, profit=3000, spisano=4)

    result = db.get_analytics(df, dt)
    assert isinstance(result, dict)
    assert "bouquets" in result
    assert "profit" in result
    assert "spisano" in result
    assert result["bouquets"] >= 5
    assert result["profit"] >= 3000
    assert result["spisano"] >= 4


# ---------- Счётчики букетов ----------

def test_count_bouquets_total():
    """count_bouquets_total возвращает число собранных букетов."""
    db.init_db()
    before = db.count_bouquets_total()

    db.add_bouquet(
        "2026-10-01", "ТестСчётчикТотал", "Роза×2", "Плёнка", "M",
        "100", "500", "300", sold=0, count=3
    )
    after = db.count_bouquets_total()
    assert after >= before + 3

    db.delete_bouquet_by_name("ТестСчётчикТотал", "2026-10-01")


def test_count_unsold_by_name():
    """count_unsold_by_name считает непроданные букеты по имени."""
    db.init_db()
    # Изначально — 0
    assert db.count_unsold_by_name("ТестПоИмени") == 0

    db.add_bouquet(
        "2026-10-02", "ТестПоИмени", "Пион×3", "Бумага", "L",
        "150", "800", "500", sold=0, count=2
    )
    db.add_bouquet(
        "2026-10-03", "ТестПоИмени", "Пион×5", "Бумага", "L",
        "200", "1000", "700", sold=0, count=4
    )
    assert db.count_unsold_by_name("ТестПоИмени") == 6  # 2 + 4

    # Проверка регистронезависимости
    assert db.count_unsold_by_name("тестпоимени") == 6

    # Пустое имя — 0
    assert db.count_unsold_by_name("") == 0

    db.delete_bouquet_by_name("ТестПоИмени", "2026-10-02")
    db.delete_bouquet_by_name("ТестПоИмени", "2026-10-03")


def test_get_bouquet_total_by_name():
    """get_bouquet_total_by_name возвращает total последнего букета с таким именем."""
    db.init_db()
    assert db.get_bouquet_total_by_name("ТестЦены") == 0
    assert db.get_bouquet_total_by_name("") == 0

    db.add_bouquet(
        "2026-10-04", "ТестЦены", "Роза×1", "Плёнка", "S",
        "50", "300", "150", sold=0, count=1
    )
    assert db.get_bouquet_total_by_name("ТестЦены") == 300

    # Добавляем более новый букет с тем же именем — должен вернуться его total
    db.add_bouquet(
        "2026-10-05", "ТестЦены", "Роза×2", "Плёнка", "M",
        "100", "600", "400", sold=0, count=1
    )
    assert db.get_bouquet_total_by_name("ТестЦены") == 600
    # Регистронезависимость
    assert db.get_bouquet_total_by_name("тестцены") == 600

    db.delete_bouquet_by_name("ТестЦены", "2026-10-04")
    db.delete_bouquet_by_name("ТестЦены", "2026-10-05")


# ---------- Продажа букетов ----------

def test_toggle_bouquet_sold():
    """toggle_bouquet_sold переключает sold туда-обратно."""
    db.init_db()
    db.add_bouquet(
        "2026-11-10", "ТестToggle", "Роза×1", "Плёнка", "S",
        "50", "300", "150", sold=0, count=1
    )
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == "ТестToggle"][0]
    assert b["sold"] is False

    db.toggle_bouquet_sold(b["id"])
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == "ТестToggle"][0]
    assert b["sold"] is True

    db.toggle_bouquet_sold(b["id"])
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == "ТестToggle"][0]
    assert b["sold"] is False

    db.delete_bouquet_by_name("ТестToggle", "2026-11-10")


def test_update_bouquet_count():
    """update_bouquet_count меняет количество штук у букета."""
    db.init_db()
    db.add_bouquet(
        "2026-11-11", "ТестСчётчик", "Пион×3", "Бумага", "M",
        "100", "500", "300", sold=0, count=5
    )
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == "ТестСчётчик"][0]
    assert b["count"] == 5

    db.update_bouquet_count(b["id"], 2)
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == "ТестСчётчик"][0]
    assert b["count"] == 2

    db.delete_bouquet_by_name("ТестСчётчик", "2026-11-11")


def test_sell_bouquet_by_name():
    """sell_bouquet_by_name уменьшает count на 1."""
    db.init_db()
    # Уникальное имя, чтобы не пересекаться со старыми данными
    unique_name = "ТестПродажаУникальный123"
    db.add_bouquet(
        "2026-11-12", unique_name, "Тюльпан×5", "Плёнка", "M",
        "100", "700", "400", sold=0, count=2
    )

    # Находим id нашего букета
    bouquets = db.get_bouquets()
    my = [x for x in bouquets if x["name"] == unique_name][0]
    my_id = my["id"]
    assert my["count"] == 2

    # Продаём 1 шт — count станет 1
    assert db.sell_bouquet_by_name(unique_name) is True

    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["id"] == my_id][0]
    assert b["count"] == 1
    assert b["sold"] is False

    # Несуществующий букет
    assert db.sell_bouquet_by_name("ТакогоНет") is False

    # Пустое имя
    assert db.sell_bouquet_by_name("") is False

    db.delete_bouquet_by_name(unique_name, "2026-11-12")

def test_update_bouquet_initial_count():
    """update_bouquet_initial_count меняет 'Было всего' у букета."""
    db.init_db()
    unique_name = "ТестБылоВсего"
    db.add_bouquet(
        "2026-11-13", unique_name, "Роза×3", "Плёнка", "M",
        "150", "900", "500", sold=0, count=3
    )
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["name"] == unique_name][0]
    my_id = b["id"]
    assert b["initial_count"] == 3

    # Меняем «Было всего» на 5 — у непроданного синхронизируется и count
    db.update_bouquet_initial_count(my_id, 5)
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["id"] == my_id][0]
    assert b["initial_count"] == 5
    assert b["count"] == 5

    # Помечаем проданным и меняем initial_count — count не должен меняться
    db.toggle_bouquet_sold(my_id)
    db.update_bouquet_initial_count(my_id, 7)
    bouquets = db.get_bouquets()
    b = [x for x in bouquets if x["id"] == my_id][0]
    assert b["initial_count"] == 7
    assert b["count"] == 5  # не изменился, т.к. букет продан

    db.delete_bouquet_by_name(unique_name, "2026-11-13")