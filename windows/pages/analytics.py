from datetime import date, timedelta

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

import db


class AnalyticsPage(QWidget):
    """Окно «Аналитика»."""

    def __init__(self, app):
        super().__init__()
        self.app = app

        # фон — светлый + прозрачный PNG с листиками
        self.bg = QLabel(self)
        self.bg.setGeometry(0, 0, 1920, 1080)
        self.bg.setStyleSheet("""
            QLabel {
                background-color: #F5FAF5;
                background-image: url(images/Fon_2.png);
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
        self.bg.lower()

        self.current_period = "day"   # day / week / year

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_period_buttons()
        self.create_period_label()
        self.create_stats_rows()
        self.create_chart()
        self.create_exit_button()
        self.create_minimize_button()

        self.bg.lower()

        self.update_stats()

    #  ВЕРХНЯЯ / НИЖНЯЯ / БОКОВЫЕ ПОЛОСКИ
    def create_top_bar(self):
        """Верхняя полоска."""
        self.top_bar = QLabel(self)
        self.top_bar.setGeometry(240, 0, 1440, 139)
        self.top_bar.setStyleSheet("""
            QLabel {
                background-color: #EAF3EB;
            }
        """)
        self.top_bar.lower()

        self.top_line = QLabel(self)
        self.top_line.setGeometry(240, 135, 1440, 5)
        self.top_line.setStyleSheet("""
            QLabel {
                background-color: #5D6D5F;
            }
        """)

    def create_bottom_bar(self):
        """Нижняя полоска."""
        self.bottom_bar = QLabel(self)
        self.bottom_bar.setGeometry(240, 1050, 1440, 139)
        self.bottom_bar.setStyleSheet("""
            QLabel {
                background-color: #EAF3EB;
            }
        """)
        self.bottom_bar.lower()

    def create_side_bars(self):
        """Боковые полоски."""
        self.left_bar = QLabel(self)
        self.left_bar.setGeometry(-9760, 0, 10000, 2000)
        self.left_bar.setStyleSheet("""
            QLabel {
                background-color: #8BA48B;
            }
        """)
        self.left_bar.lower()

        self.right_bar = QLabel(self)
        self.right_bar.setGeometry(1680, 0, 10000, 2000)
        self.right_bar.setStyleSheet("""
            QLabel {
                background-color: #8BA48B;
            }
        """)
        self.right_bar.lower()

    #  ЗАГОЛОВОК
    def create_title(self):
        """Заголовок «Флора-учёт» и «Аналитика»."""
        self.title = QLabel("Флора-учёт", self)
        self.title.setGeometry(290, 30, 423, 70)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 64px;
                font-family: 'Cormorant Infant';
                font-weight: 500;
                background: transparent;
            }
        """)

        self.subtitle = QLabel("Аналитика", self)
        self.subtitle.setGeometry(1140, 25, 423, 70)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 64px;
                font-family: 'Cormorant Infant';
                font-weight: 500;
                background: transparent;
            }
        """)

    #  КНОПКИ ПЕРИОДОВ
    def create_period_buttons(self):
        """Три кнопки: За сегодня / За текущую неделю / За текущий год."""
        self.btn_day = QPushButton("За сегодня", self)
        self.btn_day.setGeometry(305, 190, 340, 82)
        self.btn_day.clicked.connect(lambda: self.set_period("day"))

        self.btn_week = QPushButton("За текущую  неделю", self)
        self.btn_week.setGeometry(750, 190, 350, 82)
        self.btn_week.clicked.connect(lambda: self.set_period("week"))

        self.btn_year = QPushButton("За текущий год", self)
        self.btn_year.setGeometry(1195, 190, 340, 82)
        self.btn_year.clicked.connect(lambda: self.set_period("year"))

        for b in (self.btn_day, self.btn_week, self.btn_year):
            self.add_shadow(b)

        self.apply_button_styles()

    def apply_button_styles(self):
        """Активная кнопка — тёмная, остальные — светлые."""
        active = """
            QPushButton {
                background-color: #639A78;
                color: #F0F6F3;
                border-radius: 20px;
                font-size: 32px;
                font-weight: 500;
                font-family: 'Comic Relief';
                border: 1px solid #1D3A1C;
            }
        """
        inactive = """
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 20px;
                font-size: 32px;
                font-weight: 500;
                font-family: 'Comic Relief';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """
        self.btn_day.setStyleSheet(
            active if self.current_period == "day" else inactive
        )
        self.btn_week.setStyleSheet(
            active if self.current_period == "week" else inactive
        )
        self.btn_year.setStyleSheet(
            active if self.current_period == "year" else inactive
        )

    #  ЗАГОЛОВОК «Отчет за ...»
    def create_period_label(self):
        """Крупная подпись над статистикой."""
        self.period_label = QLabel("Отчет за сегодня", self)
        self.period_label.setGeometry(500, 290, 920, 70)
        self.period_label.setAlignment(Qt.AlignCenter)
        self.period_label.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 48px;
                font-family: 'Cormorant Infant';
                font-weight: 400;
                background: transparent;
            }
        """)

        self.period_line = QLabel(self)
        self.period_line.setGeometry(660, 355, 600, 3)
        self.period_line.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

    #  СТРОКИ СТАТИСТИКИ
    def create_stats_rows(self):
        """Пять строк статистики: слева подпись, справа цифра + сравнение."""
        rows = [
            ("Собрано за период:", "bouquets"),
            ("Продано за период:", "sold"),
            ("В наличии сейчас:", "stock"),
            ("Прибыль за период:", "profit"),
            ("Списано за период:", "spisano"),
        ]

        self.stats = {}

        y = 380
        for label_text, key in rows:
            lbl = QLabel(label_text, self)
            lbl.setGeometry(475, y, 500, 50)
            lbl.setStyleSheet("""
                QLabel {
                    color: #1D321C;
                    font-size: 42px;
                    font-family: 'Cormorant Infant';
                    background: transparent;
                }
            """)

            line = QLabel(self)
            line.setGeometry(475, y + 55, 500, 5)
            line.setStyleSheet("""
                QLabel {
                    background-color: #AFC9B9;
                }
            """)

            val = QLabel("0", self)
            val.setGeometry(1000, y, 420, 50)
            val.setAlignment(Qt.AlignCenter)
            val.setStyleSheet("""
                QLabel {
                    background-color: #90B29E;
                    color: #1D321C;
                    font-size: 28px;
                    font-family: 'Cormorant Infant';
                    border: 1px solid #1D3A1C;
                }
            """)
            self.add_shadow(val)

            cmp = QLabel("", self)
            cmp.setGeometry(1000, y + 50, 420, 30)
            cmp.setAlignment(Qt.AlignCenter)
            cmp.setStyleSheet("""
                QLabel {
                    color: #4A7C59;
                    font-size: 20px;
                    font-family: 'Cormorant Infant';
                    background: transparent;
                }
            """)

            self.stats[key] = {"value": val, "compare": cmp}

            y += 85

    #  КНОПКА «ПОКАЗАТЬ ГРАФИК» + «ОБНОВИТЬ»
    def create_chart(self):
        """Кнопки «Обновить» и «Показать график»."""
        self.refresh_btn = QPushButton("Обновить", self)
        self.refresh_btn.setGeometry(490, 840, 420, 75)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 38px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.refresh_btn)
        self.refresh_btn.clicked.connect(self.refresh_stats)

        self.chart_btn = QPushButton("Показать график", self)
        self.chart_btn.setGeometry(1000, 840, 420, 75)
        self.chart_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 38px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.chart_btn)
        self.chart_btn.clicked.connect(self.open_graph)

    def open_graph(self):
        """Открывает страницу с графиком."""
        self.app.go_to("graph")

    #  НАЗАД / СВЕРНУТЬ
    def create_exit_button(self):
        """Кнопка «Назад»."""
        self.exit_button = QPushButton("Назад", self)
        self.exit_button.setGeometry(300, 919, 153, 79)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #C8E6C9;
                color: #4A7C59;
                border-radius: 25px;
                font-size: 50px;
                font-family: 'Cormorant Infant';
                padding-bottom: 8px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #AFD2B1;
            }
        """)
        self.add_shadow(self.exit_button)
        self.exit_button.clicked.connect(self.go_back)

    def create_minimize_button(self):
        """Кнопка «Свернуть»."""
        self.min_button = QPushButton("—", self)
        self.min_button.setGeometry(1590, 150, 50, 50)
        self.min_button.setStyleSheet("""
            QPushButton {
                background-color: #C8E6C9;
                color: #4A7C59;
                border-radius: 10px;
                font-size: 24px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #AFD2B1;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(8)
        shadow.setYOffset(8)
        shadow.setColor(QColor("#D0DDD5"))
        self.min_button.setGraphicsEffect(shadow)

        self.min_button.clicked.connect(self.showMinimized)

    def go_back(self):
        """Возврат на главное окно с карточками."""
        self.app.go_to("main")

    #  ТЕНИ
    def add_shadow(self, widget):
        """Добавляет тень под элементом."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        widget.setGraphicsEffect(shadow)

    #  ЛОГИКА
    def refresh_stats(self):
        """Обновляет статистику: сначала досчитывает total, потом пересчитывает."""
        try:
            db.fix_orders_total()
        except Exception:
            pass
        self.update_stats()

    def showEvent(self, event):
        """При показе окна НЕ пересчитываем —
        обновление только по кнопке «Обновить»."""
        super().showEvent(event)

    def set_period(self, period):
        """Переключение периода: day / week / year."""
        self.current_period = period
        self.apply_button_styles()

        if period == "day":
            self.period_label.setText("Отчет за сегодня")
        elif period == "week":
            self.period_label.setText("Отчет за текущую неделю")
        else:
            self.period_label.setText("Отчет за текущий год")

        self.update_stats()

    def _get_ranges(self):
        """Возвращает диапазоны: текущий, прошлый, год назад."""
        today = date.today()

        if self.current_period == "day":
            d_from = today
            d_to = today
            prev_from = today - timedelta(days=1)
            prev_to = prev_from
        elif self.current_period == "week":
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            d_from = monday
            d_to = sunday
            prev_from = monday - timedelta(days=7)
            prev_to = sunday - timedelta(days=7)
        else:  # year
            d_from = date(today.year, 1, 1)
            d_to = date(today.year, 12, 31)
            prev_from = date(today.year - 1, 1, 1)
            prev_to = date(today.year - 1, 12, 31)

        # год назад — тот же период, только год вычесть
        # (29 февраля в невисокосный год сдвигаем на 28-е)
        year_ago_from = self._safe_replace_year(d_from, d_from.year - 1)
        year_ago_to = self._safe_replace_year(d_to, d_to.year - 1)

        return (
            d_from.strftime("%Y-%m-%d"), d_to.strftime("%Y-%m-%d"),
            prev_from.strftime("%Y-%m-%d"), prev_to.strftime("%Y-%m-%d"),
            year_ago_from.strftime("%Y-%m-%d"), year_ago_to.strftime("%Y-%m-%d"),
        )

    def _safe_replace_year(self, d, year):
        """replace(year=...) с защитой от 29 февраля."""
        try:
            return d.replace(year=year)
        except ValueError:
            return d.replace(year=year, day=28)

    def _fmt_percent(self, current, prev):
        """
        Возвращает строку вида '+15%' / '−8%' / ''.
        Если в прошлом периоде было 0 — сравнение не имеет смысла, возвращаем ''.
        """
        if prev == 0 and current == 0:
            return ""
        if prev == 0:
            return ""
        diff = ((current - prev) / prev) * 100
        sign = "+" if diff >= 0 else "−"
        return f"{sign}{abs(diff):.0f}%"

    def _get_prev_label(self):
        if self.current_period == "day":
            return "к вчера"
        elif self.current_period == "week":
            return "к прошлой неделе"
        else:
            return "к прошлому году"

    def _get_year_ago_label(self):
        today = date.today()
        if self.current_period == "day":
            d = self._safe_replace_year(today, today.year - 1)
            return f"к {d.strftime('%d.%m.%Y')}"
        elif self.current_period == "week":
            return "к той же неделе год назад"
        else:
            return f"к {today.year - 1}"

    def update_stats(self):
        """Считает все цифры и сравнения."""
        (d_from, d_to,
         prev_from, prev_to,
         ya_from, ya_to) = self._get_ranges()

        # текущий период
        # «собрано» — из букетов (по дате сборки)
        stats_b = db.get_bouquets_stats(d_from, d_to)
        collected = stats_b["collected"]

        # «в наличии сейчас» — из букетов (без даты)
        in_stock = db.count_unsold_bouquets()

        # «продано» и «прибыль» — из заказов (календарь)
        stats_o = db.get_orders_stats(d_from, d_to)
        sold = stats_o["sold"]
        profit = stats_o["profit"]

        # «списано» — из spisaniya
        spisano = db.get_spisano_stats(d_from, d_to)

        # прошлый период
        prev_stats_b = db.get_bouquets_stats(prev_from, prev_to)
        prev_collected = prev_stats_b["collected"]

        prev_stats_o = db.get_orders_stats(prev_from, prev_to)
        prev_sold = prev_stats_o["sold"]
        prev_profit = prev_stats_o["profit"]

        prev_spisano = db.get_spisano_stats(prev_from, prev_to)

        # год назад 
        ya_stats_b = db.get_bouquets_stats(ya_from, ya_to)
        ya_collected = ya_stats_b["collected"]

        ya_stats_o = db.get_orders_stats(ya_from, ya_to)
        ya_sold = ya_stats_o["sold"]
        ya_profit = ya_stats_o["profit"]

        ya_spisano = db.get_spisano_stats(ya_from, ya_to)

        #отображение
        self.stats["bouquets"]["value"].setText(
            f"{collected} шт."
        )
        self.stats["sold"]["value"].setText(
            f"{sold} шт."
        )
        self.stats["stock"]["value"].setText(
            f"{in_stock} шт."
        )
        self.stats["profit"]["value"].setText(
            f"{profit} ₽"
        )
        self.stats["spisano"]["value"].setText(
            f"{spisano} шт."
        )

        #сравнения
        prev_lbl = self._get_prev_label()
        ya_lbl = self._get_year_ago_label()

        def make_cmp(cur, prev, ya):
            p = self._fmt_percent(cur, prev)
            y = self._fmt_percent(cur, ya)
            parts = []
            if p:
                parts.append(f"{p} {prev_lbl}")
            if y:
                parts.append(f"{y} {ya_lbl}")
            return "   ".join(parts) if parts else "—"

        self.stats["bouquets"]["compare"].setText(make_cmp(
            collected, prev_collected, ya_collected
        ))
        self.stats["sold"]["compare"].setText(make_cmp(
            sold, prev_sold, ya_sold
        ))
        self.stats["stock"]["compare"].setText("")   # не сравниваем
        self.stats["profit"]["compare"].setText(make_cmp(
            profit, prev_profit, ya_profit
        ))
        self.stats["spisano"]["compare"].setText(make_cmp(
            spisano, prev_spisano, ya_spisano
        ))

    def showMinimized(self):
        """Свернуть окно приложения."""
        win = self.window()
        if win is not None:
            win.showMinimized()