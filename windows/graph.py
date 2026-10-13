from datetime import date, timedelta

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QGraphicsDropShadowEffect, QWidget,
    QDateEdit, QScrollArea, QComboBox, QMenu, QWidgetAction, QCheckBox,
    QVBoxLayout
)
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFont, QIcon
from PyQt5.QtCore import Qt, QRect, QDate, QPoint

import db
from windows.green_calendar import GreenCalendar


SCROLLBAR_STYLE = """
    QScrollBar:horizontal {
        background-color: #EAF3EB;
        height: 14px;
        border: none;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background-color: #90B29E;
        min-width: 40px;
        border-radius: 7px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #72917F;
    }
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0px;
        height: 0px;
        background: transparent;
        border: none;
    }
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: transparent;
    }
    QScrollBar:vertical {
        background-color: #EAF3EB;
        width: 14px;
        border: none;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #90B29E;
        min-height: 40px;
        border-radius: 7px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #72917F;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        width: 0px;
        height: 0px;
        background: transparent;
        border: none;
    }
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: transparent;
    }
"""


MONTH_NAMES_RU = [
    "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]

MONTH_SHORT_RU = [
    "", "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
    "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
]


class BarChart(QWidget):
    """Столбчатый график в стиле программы."""

    def __init__(self, parent=None, color="#639A78", title=""):
        super().__init__(parent)
        self.data = []
        self.color = QColor(color)
        self.title = title
        self.setStyleSheet("background: transparent;")

    def set_data(self, data):
        self.data = list(data)
        self.update_width()
        self.update()

    def update_width(self):
        n = len(self.data) or 1
        min_width = 1200
        width = max(min_width, n * 70)
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        painter.setPen(QPen(QColor("#1D3A1C"), 2))
        painter.setBrush(QBrush(QColor("#F0F6F3")))
        painter.drawRect(0, 0, w - 1, h - 1)

        if self.title:
            painter.setPen(QColor("#124612"))
            f = QFont("Cormorant Infant", 18, QFont.Bold)
            painter.setFont(f)
            painter.drawText(
                QRect(20, 5, w - 40, 42),
                Qt.AlignLeft | Qt.AlignVCenter, self.title
            )

        if not self.data:
            painter.end()
            return

        pad_left = 30
        pad_right = 30
        pad_top = 55
        pad_bottom = 70

        chart_w = w - pad_left - pad_right
        chart_h = h - pad_top - pad_bottom

        n = len(self.data)
        max_val = max(v for _, v in self.data) or 1

        col_w = chart_w / n
        bar_w = col_w * 0.6
        gap = col_w * 0.4

        for i, (label, value) in enumerate(self.data):
            x = pad_left + i * col_w + gap / 2
            bar_h = (value / max_val) * chart_h
            y = pad_top + chart_h - bar_h

            painter.setPen(QPen(QColor("#1D3A1C"), 1))
            painter.setBrush(QBrush(self.color))
            painter.drawRect(int(x), int(y), int(bar_w), int(bar_h))

            if value > 0:
                painter.setPen(QColor("#124612"))
                f = QFont("Cormorant Infant", 14)
                painter.setFont(f)
                painter.drawText(
                    QRect(int(x - 30), int(y - 30),
                          int(bar_w + 60), 30),
                    Qt.AlignCenter, str(int(value))
                )

            painter.setPen(QColor("#1D321C"))
            f = QFont("Cormorant Infant", 14)
            painter.setFont(f)
            painter.drawText(
                QRect(int(x - 30), h - pad_bottom + 15,
                      int(bar_w + 60), 40),
                Qt.AlignCenter, label
            )

        painter.end()


class GraphWindow(QMainWindow):
    """Окно «График» — отдельное окно с двумя графиками."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Флора-учёт")
        self.setWindowIcon(QIcon("images/flower.ico"))
        self.setWindowIcon(QIcon("images/flower.ico"))
        self.showFullScreen()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5FAF5;
                background-image: url(images/Fon_2.png);
                background-position: center;
                background-repeat: no-repeat;
            }
        """)

        self.current_period = "day"
        self.selected_months = set()
        self.selected_years = set()

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_period_buttons()
        self.create_charts()
        self.create_exit_button()
        self.create_minimize_button()

        self.set_period("day")

    def create_top_bar(self):
        self.top_bar = QLabel(self)
        self.top_bar.setGeometry(240, 0, 1440, 139)
        self.top_bar.setStyleSheet(
            "QLabel { background-color: #EAF3EB; }"
        )
        self.top_bar.lower()

        self.top_line = QLabel(self)
        self.top_line.setGeometry(240, 135, 1440, 5)
        self.top_line.setStyleSheet(
            "QLabel { background-color: #5D6D5F; }"
        )

    def create_bottom_bar(self):
        self.bottom_bar = QLabel(self)
        self.bottom_bar.setGeometry(240, 1050, 1440, 139)
        self.bottom_bar.setStyleSheet(
            "QLabel { background-color: #EAF3EB; }"
        )
        self.bottom_bar.lower()

    def create_side_bars(self):
        self.left_bar = QLabel(self)
        self.left_bar.setGeometry(-9760, 0, 10000, 2000)
        self.left_bar.setStyleSheet(
            "QLabel { background-color: #8BA48B; }"
        )
        self.left_bar.lower()

        self.right_bar = QLabel(self)
        self.right_bar.setGeometry(1680, 0, 10000, 2000)
        self.right_bar.setStyleSheet(
            "QLabel { background-color: #8BA48B; }"
        )
        self.right_bar.lower()

    def create_title(self):
        self.title = QLabel("Флора-учёт", self)
        self.title.setGeometry(290, 30, 423, 70)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

        self.subtitle = QLabel("График", self)
        self.subtitle.setGeometry(1140, 25, 423, 70)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

    def create_period_buttons(self):
        """Три кнопки + поля + кнопка «Применить»."""
        self.btn_day = QPushButton("День", self)
        self.btn_day.setGeometry(280, 170, 240, 65)
        self.btn_day.clicked.connect(lambda: self.set_period("day"))

        self.btn_month = QPushButton("Месяц", self)
        self.btn_month.setGeometry(540, 170, 240, 65)
        self.btn_month.clicked.connect(lambda: self.set_period("month"))

        self.btn_year = QPushButton("Год", self)
        self.btn_year.setGeometry(800, 170, 240, 65)
        self.btn_year.clicked.connect(lambda: self.set_period("year"))

        for b in (self.btn_day, self.btn_month, self.btn_year):
            self.add_shadow(b)

        date_style = """
            QDateEdit {
                background-color: #EBF5EB;
                color: #000000;
                font-weight: 500;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 38px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 38px;
                border: none;
                background: transparent;
            }
            QDateEdit::down-arrow {
                image: url(images/vniz.png);
                width: 28px;
                height: 28px;
            }
        """
        combo_style = """
            QComboBox {
                background-color: #EBF5EB;
                color: #000000;
                font-weight: 500;
                font-size: 24px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 40px;
            }
            QComboBox::down-arrow {
                image: url(images/vniz.png);
                width: 28px;
                height: 28px;
            }
            QComboBox QAbstractItemView {
                background-color: #F0F6F3;
                color: #1D321C;
                selection-background-color: #B5DCC5;
                selection-color: #1D321C;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                outline: none;
            }
        """

        label_style = """
            QLabel {
                color: #124612; font-size: 30px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """

        plus_btn_style = """
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 10px;
                font-size: 30px;
                font-weight: 700;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """

        Y = 175

        # режим «День»: С: / По: 
        self.label_from = QLabel("С:", self)
        self.label_from.setGeometry(1050, Y - 3, 40, 55)
        self.label_from.setStyleSheet(label_style)

        self.date_from = QDateEdit(self)
        self.date_from.setGeometry(1090, Y, 220, 55)
        self.date_from.setCalendarPopup(True)
        self.date_from.setCalendarWidget(GreenCalendar())
        self.date_from.setDate(QDate.currentDate().addDays(-6))
        self.date_from.setDisplayFormat("dd.MM.yyyy")
        self.date_from.setStyleSheet(date_style)
        self.add_shadow(self.date_from)

        self.label_to = QLabel("По:", self)
        self.label_to.setGeometry(1330, Y - 3, 60, 55)
        self.label_to.setStyleSheet(label_style)

        self.date_to = QDateEdit(self)
        self.date_to.setGeometry(1390, Y, 220, 55)
        self.date_to.setCalendarPopup(True)
        self.date_to.setCalendarWidget(GreenCalendar())
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("dd.MM.yyyy")
        self.date_to.setStyleSheet(date_style)
        self.add_shadow(self.date_to)

        # режим «Месяц»: Месяц: [___▼] [+] Год: [___▼]
        self.label_month = QLabel("Месяц:", self)
        self.label_month.setGeometry(1050, Y - 3, 90, 55)
        self.label_month.setStyleSheet(label_style)

        self.month_combo = QComboBox(self)
        self.month_combo.setGeometry(1145, Y, 150, 55)
        self.month_combo.setStyleSheet(combo_style)
        for i in range(1, 13):
            self.month_combo.addItem(MONTH_NAMES_RU[i], i)
        self.month_combo.setCurrentIndex(date.today().month - 1)
        self.add_shadow(self.month_combo)

        self.months_btn = QPushButton("+", self)
        self.months_btn.setGeometry(1300, Y, 55, 55)
        self.months_btn.setStyleSheet(plus_btn_style)
        self.add_shadow(self.months_btn)
        self.months_btn.clicked.connect(self.show_months_menu)

        # год для режима «Месяц»
        self.label_year_month = QLabel("Год:", self)
        self.label_year_month.setGeometry(1370, Y - 3, 60, 55)
        self.label_year_month.setStyleSheet(label_style)

        self.year_combo_month = QComboBox(self)
        self.year_combo_month.setGeometry(1430, Y, 150, 55)
        self.year_combo_month.setStyleSheet(combo_style)
        for y in range(2020, 2031):
            self.year_combo_month.addItem(str(y), y)
        self.year_combo_month.setCurrentText(str(date.today().year))
        self.add_shadow(self.year_combo_month)

        # режим «Год»: Год: [___▼] [+]
        self.label_year = QLabel("Год:", self)
        self.label_year.setGeometry(1080, Y - 3, 60, 55)
        self.label_year.setStyleSheet(label_style)

        self.year_combo = QComboBox(self)
        self.year_combo.setGeometry(1140, Y, 150, 55)
        self.year_combo.setStyleSheet(combo_style)
        for y in range(2020, 2031):
            self.year_combo.addItem(str(y), y)
        self.year_combo.setCurrentText(str(date.today().year))
        self.add_shadow(self.year_combo)

        self.years_btn = QPushButton("+", self)
        self.years_btn.setGeometry(1300, Y, 55, 55)
        self.years_btn.setStyleSheet(plus_btn_style)
        self.add_shadow(self.years_btn)
        self.years_btn.clicked.connect(self.show_years_menu)

        # кнопка «Применить»
        self.apply_btn = QPushButton("Применить", self)
        self.apply_btn.setGeometry(1050, 250, 530, 60)
        self.apply_btn.clicked.connect(self.update_charts)
        self.add_shadow(self.apply_btn)

        self.apply_button_styles()

    def show_months_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
                padding: 6px;
            }
            QWidget {
                background-color: #F0F6F3;
            }
        """)

        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(6, 6, 6, 6)
        vbox.setSpacing(2)

        self.month_checks = {}
        for i in range(1, 13):
            cb = QCheckBox(MONTH_NAMES_RU[i])
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 22px;
                    font-family: 'Cormorant Infant';
                    color: #1D321C;
                    padding: 4px 10px;
                    spacing: 10px;
                    background-color: #F0F6F3;
                }
                QCheckBox:hover {
                    background-color: #EAF3EB;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid #5D6D5F;
                    border-radius: 4px;
                    background-color: #F0F6F3;
                }
                QCheckBox::indicator:checked {
                    background-color: #639A78;
                    border: 2px solid #1D3A1C;
                }
            """)
            if i in self.selected_months:
                cb.setChecked(True)
            cb.stateChanged.connect(self.on_month_check_changed)
            vbox.addWidget(cb)
            self.month_checks[i] = cb

        action = QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.addAction(action)

        pos = self.months_btn.mapToGlobal(
            QPoint(0, self.months_btn.height())
        )
        menu.exec_(pos)

    def show_years_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
                padding: 6px;
            }
            QWidget {
                background-color: #F0F6F3;
            }
        """)

        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(6, 6, 6, 6)
        vbox.setSpacing(2)

        self.year_checks = {}
        for y in range(2020, 2031):
            cb = QCheckBox(str(y))
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 22px;
                    font-family: 'Cormorant Infant';
                    color: #1D321C;
                    padding: 4px 10px;
                    spacing: 10px;
                    background-color: #F0F6F3;
                }
                QCheckBox:hover {
                    background-color: #EAF3EB;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid #5D6D5F;
                    border-radius: 4px;
                    background-color: #F0F6F3;
                }
                QCheckBox::indicator:checked {
                    background-color: #639A78;
                    border: 2px solid #1D3A1C;
                }
            """)
            if y in self.selected_years:
                cb.setChecked(True)
            cb.stateChanged.connect(self.on_year_check_changed)
            vbox.addWidget(cb)
            self.year_checks[y] = cb

        action = QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.addAction(action)

        pos = self.years_btn.mapToGlobal(
            QPoint(0, self.years_btn.height())
        )
        menu.exec_(pos)

    def on_month_check_changed(self):
        self.selected_months = {
            i for i, cb in self.month_checks.items() if cb.isChecked()
        }

    def on_year_check_changed(self):
        self.selected_years = {
            y for y, cb in self.year_checks.items() if cb.isChecked()
        }

    def apply_button_styles(self):
        active = """
            QPushButton {
                background-color: #639A78;
                color: #F0F6F3;
                border-radius: 20px;
                font-size: 30px;
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
                font-size: 30px;
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
        self.btn_month.setStyleSheet(
            active if self.current_period == "month" else inactive
        )
        self.btn_year.setStyleSheet(
            active if self.current_period == "year" else inactive
        )
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #639A78;
                color: #F0F6F3;
                border-radius: 20px;
                font-size: 30px;
                font-weight: 500;
                font-family: 'Comic Relief';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #548268;
            }
        """)

    def show_period_widgets(self, mode):
        for w in (
            self.label_from, self.date_from,
            self.label_to, self.date_to,
            self.label_month, self.month_combo, self.months_btn,
            self.label_year, self.year_combo, self.years_btn,
            self.label_year_month, self.year_combo_month,
        ):
            w.hide()

        if mode == "day":
            self.label_from.show()
            self.date_from.show()
            self.label_to.show()
            self.date_to.show()

        elif mode == "month":
            self.label_month.show()
            self.month_combo.show()
            self.months_btn.show()
            self.label_year_month.show()
            self.year_combo_month.show()

        elif mode == "year":
            self.label_year.show()
            self.year_combo.show()
            self.years_btn.show()

        self.apply_btn.show()

    def create_charts(self):
        self.scroll_profit = QScrollArea(self)
        self.scroll_profit.setGeometry(360, 330, 1200, 280)
        self.scroll_profit.setWidgetResizable(False)
        self.scroll_profit.setStyleSheet("""
            QScrollArea {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
            }
        """)
        self.scroll_profit.horizontalScrollBar().setStyleSheet(
            SCROLLBAR_STYLE
        )
        self.scroll_profit.verticalScrollBar().setStyleSheet(
            SCROLLBAR_STYLE
        )

        self.chart_profit = BarChart(
            color="#639A78", title="Прибыль, ₽"
        )
        self.chart_profit.setFixedHeight(250)
        self.scroll_profit.setWidget(self.chart_profit)

        self.scroll_sales = QScrollArea(self)
        self.scroll_sales.setGeometry(360, 630, 1200, 280)
        self.scroll_sales.setWidgetResizable(False)
        self.scroll_sales.setStyleSheet("""
            QScrollArea {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
            }
        """)
        self.scroll_sales.horizontalScrollBar().setStyleSheet(
            SCROLLBAR_STYLE
        )
        self.scroll_sales.verticalScrollBar().setStyleSheet(
            SCROLLBAR_STYLE
        )

        self.chart_sales = BarChart(
            color="#90B29E", title="Продано букетов, шт."
        )
        self.chart_sales.setFixedHeight(250)
        self.scroll_sales.setWidget(self.chart_sales)

    def create_exit_button(self):
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
            QPushButton:hover { background-color: #AFD2B1; }
        """)
        self.add_shadow(self.exit_button)
        self.exit_button.clicked.connect(self.close)

    def create_minimize_button(self):
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
            QPushButton:hover { background-color: #AFD2B1; }
        """)
        self.add_shadow(self.min_button)
        self.min_button.clicked.connect(self.showMinimized)

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        widget.setGraphicsEffect(shadow)

    #  ЛОГИКА
    def set_period(self, period):
        self.current_period = period

        today = date.today()

        if period == "day":
            self.date_from.setDate(QDate.currentDate().addDays(-6))
            self.date_to.setDate(QDate.currentDate())
        elif period == "month":
            self.month_combo.setCurrentIndex(today.month - 1)
            self.year_combo_month.setCurrentText(str(today.year))
            self.selected_months = set()
        elif period == "year":
            self.year_combo.setCurrentText(str(today.year))
            self.selected_years = set()

        self.show_period_widgets(period)
        self.apply_button_styles()

    def update_charts(self):
        if self.current_period == "day":
            df = self.date_from.date().toPyDate()
            dt = self.date_to.date().toPyDate()

            if dt < df:
                df, dt = dt, df

            d_from = df.strftime("%Y-%m-%d")
            d_to = dt.strftime("%Y-%m-%d")
            days_count = (dt - df).days + 1

            profit_by_day = db.get_orders_profit_by_day(d_from, d_to)
            sold_by_day = db.get_orders_sold_by_day(d_from, d_to)

            profit_data = []
            sold_data = []

            if days_count <= 31:
                for i in range(days_count):
                    d = df + timedelta(days=i)
                    key = d.strftime("%Y-%m-%d")
                    label = d.strftime("%d.%m")
                    profit_data.append((label, profit_by_day.get(key, 0)))
                    sold_data.append((label, sold_by_day.get(key, 0)))
            else:
                weeks_profit = {}
                weeks_sold = {}
                order = []

                for i in range(days_count):
                    d = df + timedelta(days=i)
                    key = d.strftime("%Y-%m-%d")
                    monday = d - timedelta(days=d.weekday())
                    wk = monday.strftime("%d.%m")

                    if wk not in weeks_profit:
                        weeks_profit[wk] = 0
                        weeks_sold[wk] = 0
                        order.append(wk)

                    weeks_profit[wk] += profit_by_day.get(key, 0)
                    weeks_sold[wk] += sold_by_day.get(key, 0)

                for wk in order:
                    profit_data.append((wk, weeks_profit[wk]))
                    sold_data.append((wk, weeks_sold[wk]))

            self.chart_profit.set_data(profit_data)
            self.chart_sales.set_data(sold_data)
            self.scroll_profit.horizontalScrollBar().setValue(0)
            self.scroll_sales.horizontalScrollBar().setValue(0)

        elif self.current_period == "month":
            year = self.year_combo_month.currentData()

            if self.selected_months:
                months = sorted(self.selected_months)
                profit_data = []
                sold_data = []

                for m in months:
                    m_from = date(year, m, 1)
                    if m == 12:
                        m_to = date(year, 12, 31)
                    else:
                        m_to = date(year, m + 1, 1) - timedelta(days=1)

                    stats = db.get_orders_stats(
                        m_from.strftime("%Y-%m-%d"),
                        m_to.strftime("%Y-%m-%d")
                    )
                    profit_data.append(
                        (MONTH_SHORT_RU[m], stats["profit"])
                    )
                    sold_data.append(
                        (MONTH_SHORT_RU[m], stats["sold"])
                    )

                self.chart_profit.set_data(profit_data)
                self.chart_sales.set_data(sold_data)
                self.scroll_profit.horizontalScrollBar().setValue(0)
                self.scroll_sales.horizontalScrollBar().setValue(0)
                return

            month = self.month_combo.currentData()

            if month == 12:
                next_month = date(year + 1, 1, 1)
            else:
                next_month = date(year, month + 1, 1)
            days_in_month = (next_month - date(year, month, 1)).days

            d_from = date(year, month, 1).strftime("%Y-%m-%d")
            d_to = date(year, month, days_in_month).strftime("%Y-%m-%d")

            profit_by_day = db.get_orders_profit_by_day(d_from, d_to)
            sold_by_day = db.get_orders_sold_by_day(d_from, d_to)

            profit_data = []
            sold_data = []
            for i in range(days_in_month):
                day = date(year, month, i + 1)
                key = day.strftime("%Y-%m-%d")
                label = day.strftime("%d")
                profit_data.append((label, profit_by_day.get(key, 0)))
                sold_data.append((label, sold_by_day.get(key, 0)))

            self.chart_profit.set_data(profit_data)
            self.chart_sales.set_data(sold_data)
            self.scroll_profit.horizontalScrollBar().setValue(0)
            self.scroll_sales.horizontalScrollBar().setValue(0)

        elif self.current_period == "year":
            if self.selected_years:
                years = sorted(self.selected_years)
                profit_data = []
                sold_data = []

                for y in years:
                    stats = db.get_orders_stats(
                        f"{y}-01-01", f"{y}-12-31"
                    )
                    profit_data.append((str(y), stats["profit"]))
                    sold_data.append((str(y), stats["sold"]))

                self.chart_profit.set_data(profit_data)
                self.chart_sales.set_data(sold_data)
                self.scroll_profit.horizontalScrollBar().setValue(0)
                self.scroll_sales.horizontalScrollBar().setValue(0)
                return

            year = self.year_combo.currentData()

            profit_data = []
            sold_data = []
            for month in range(1, 13):
                m_from = date(year, month, 1)
                if month == 12:
                    m_to = date(year, 12, 31)
                else:
                    m_to = date(year, month + 1, 1) - timedelta(days=1)
                stats = db.get_orders_stats(
                    m_from.strftime("%Y-%m-%d"), m_to.strftime("%Y-%m-%d")
                )
                profit_data.append((str(month), stats["profit"]))
                sold_data.append((str(month), stats["sold"]))

            self.chart_profit.set_data(profit_data)
            self.chart_sales.set_data(sold_data)
            self.scroll_profit.horizontalScrollBar().setValue(0)
            self.scroll_sales.horizontalScrollBar().setValue(0)