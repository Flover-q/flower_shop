"""Тесты для модуля db.py."""
import os
import sys
import unittest

# чтобы импортировать db из корня проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db


class TestFlowers(unittest.TestCase):
    """Тесты для справочника цветов."""

    def setUp(self):
        """Перед каждым тестом пересоздаём БД."""
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)
        db.init_db()

    def test_add_flower(self):
        """Можно добавить цветок."""
        db.add_flower("Тестовый цветок", 100)
        flowers = db.get_flowers()
        self.assertIn("Тестовый цветок", flowers)
        self.assertEqual(flowers["Тестовый цветок"], 100)

    def test_delete_flower(self):
        """Можно удалить цветок."""
        db.add_flower("Удаляемый", 50)
        db.delete_flower("Удаляемый")
        flowers = db.get_flowers()
        self.assertNotIn("Удаляемый", flowers)

    def test_update_flower_price(self):
        """Можно изменить цену цветка."""
        db.add_flower("Роза_тест", 100)
        db.update_flower_price("Роза_тест", 200)
        flowers = db.get_flowers()
        self.assertEqual(flowers["Роза_тест"], 200)


class TestBouquets(unittest.TestCase):
    """Тесты для букетов."""

    def setUp(self):
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)
        db.init_db()

    def test_add_bouquet(self):
        """Можно добавить букет."""
        db.add_bouquet(
            "2026-10-13", "Тестовый", "Роза×5", "Плёнка", "Средний",
            "100", "500", "300", sold=0, count=1
        )
        bouquets = db.get_bouquets()
        self.assertEqual(len(bouquets), 1)
        self.assertEqual(bouquets[0]["name"], "Тестовый")

    def test_toggle_bouquet_sold(self):
        """Можно пометить букет проданным."""
        db.add_bouquet(
            "2026-10-13", "Тоггл", "Роза×5", "Плёнка", "Средний",
            "100", "500", "300", sold=0, count=1
        )
        b = db.get_bouquets()[0]
        db.toggle_bouquet_sold(b["id"])
        b2 = db.get_bouquets()[0]
        self.assertTrue(b2["sold"])

    def test_count_unsold(self):
        """Считает непроданные букеты."""
        db.add_bouquet(
            "2026-10-13", "A", "Роза×1", "", "", "0", "100", "50",
            sold=0, count=1
        )
        db.add_bouquet(
            "2026-10-13", "B", "Роза×1", "", "", "0", "100", "50",
            sold=0, count=1
        )
        self.assertEqual(db.count_unsold_bouquets(), 2)


class TestSpisaniya(unittest.TestCase):
    """Тесты для списаний."""

    def setUp(self):
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)
        db.init_db()

    def test_add_spisanie(self):
        """Можно добавить списание."""
        db.add_spisanie("2026-10-13", "Роза", 5, "Увядание")
        rows = db.get_spisaniya("2026-10-01", "2026-10-31")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["flower"], "Роза")
        self.assertEqual(rows[0]["count"], 5)


if __name__ == "__main__":
    unittest.main()
