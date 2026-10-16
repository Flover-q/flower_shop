import calendar
from datetime import date

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QColor, QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize

from windows import dialogs
import db


class CalendarPage(QWidget):
    """Окно «Календарь заказов»."""

    MONTHS_RU = [
        "", "Январь", "Февраль", "Март", "Апрель", "Май", "Ию нь",
        "Ию ль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    MONTHS_RU_GEN = [
        "", "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

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

        today = date.today()
        self.view_year = today.year
        self.view_month = today.month
        self.selected_day = None

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_month_header()
        self.create_weekdays()
        self.create_days_grid()
        self.create_selected_label()
        self.create_orders_table()
        self.create_action_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.bg.lower()

        self.build_month()

    def create_top_bar(self):
        self.top_bar = QLabel(self)
        self.top_bar.setGeometry(240, 0, 1440, 139)
        self.top_bar.setStyleSheet("""
            QLabel { background-color: #EAF3EB; }
        """)
        self.top_bar.lower()

        self.top_line = QLabel(self)
        self.top_line.setGeometry(240, 135, 1440, 5)
        self.top_line.setStyleSheet("""
            QLabel { background-color: #5D6D5F; }
        """)

    def create_bottom_bar(self):
        self.bottom_bar = QLabel(self)
        self.bottom_bar.setGeometry(240, 1050, 1440, 139)
        self.bottom_bar.setStyleSheet("""
            QLabel { background-color: #EAF3EB; }
        """)
        self.bottom_bar.lower()

    def create_side_bars(self):
        self.left_bar = QLabel(self)
        self.left_bar.setGeometry(-9760, 0, 10000, 2000)
        self.left_bar.setStyleSheet("""
            QLabel { background-color: #8BA48B; }
        """)
        self.left_bar.lower()

        self.right_bar = QLabel(self)
        self.right_bar.setGeometry(1680, 0, 10000, 2000)
        self.right_bar.setStyleSheet("""
            QLabel { background-color: #8BA48B; }
        """)
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

        self.subtitle = QLabel("Календарь", self)
        self.subtitle.setGeometry(1140, 25, 423, 80)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

    def create_month_header(self):
        self.prev_btn = QPushButton(self)
        self.prev_btn.setGeometry(700, 160, 60, 50)
        self.prev_btn.setIcon(QIcon("images/nalevo.png"))
        self.prev_btn.setIconSize(QSize(36, 36))
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #EAF3EB;
                border-radius: 25px;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_month)

        self.month_label = QLabel("", self)
        self.month_label.setGeometry(745, 152, 450, 60)
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 44px;
                font-family: 'Comic Relief'; font-weight: 500;
                background: transparent;
            }
        """)

        self.next_btn = QPushButton(self)
        self.next_btn.setGeometry(1165, 160, 60, 50)
        self.next_btn.setIcon(QIcon("images/napravo.png"))
        self.next_btn.setIconSize(QSize(36, 36))
        self.next_btn.setStyleSheet(self.prev_btn.styleSheet())
        self.next_btn.clicked.connect(self.next_month)

    def create_weekdays(self):
        names = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
        self.weekday_labels = []
        for i, name in enumerate(names):
            lbl = QLabel(name, self)
            lbl.setGeometry(640 + i * 90, 220, 100, 40)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("""
                QLabel {
                    color: #1D321C; font-size: 30px;
                    font-family: 'Comic Relief'; font-weight: 500;
                    background: transparent;
                }
            """)
            self.weekday_labels.append(lbl)

    def create_days_grid(self):
        self.day_buttons = []
        self.day_stripes = []

        for row in range(6):
            row_btns = []
            row_stripes = []
            for col in range(7):
                btn = QPushButton("", self)
                btn.setGeometry(640 + col * 90 + 25, 260 + row * 65, 50, 50)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #1D321C;
                        font-size: 26px;
                        font-family: 'Comic Relief';
                        font-weight: 700;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #EAF3EB;
                        border-radius: 25px;
                    }
                """)
                btn.clicked.connect(
                    lambda checked=False, r=row, c=col: self.on_day_click(r, c)
                )

                stripe = QLabel(self)
                stripe.setGeometry(640 + col * 90 + 10, 315 + row * 65, 80, 4)
                stripe.setStyleSheet("""
                    QLabel {
                        background-color: transparent;
                    }
                """)

                row_btns.append(btn)
                row_stripes.append(stripe)

            self.day_buttons.append(row_btns)
            self.day_stripes.append(row_stripes)

    def create_selected_label(self):
        self.selected_label = QLabel("На —", self)
        self.selected_label.setGeometry(510, 630, 700, 50)
        self.selected_label.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 40px;
                font-family: 'Comic Relief'; background: transparent;
            }
        """)

        self.selected_line = QLabel(self)
        self.selected_line.setGeometry(510, 680, 700, 3)
        self.selected_line.setStyleSheet("""
            QLabel { background-color: #AFC9B9; }
        """)

    def create_orders_table(self):
        self.orders_table = QTableWidget(self)
        self.orders_table.setGeometry(510, 690, 720, 200)
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(
            ["Имя", "Номер", "Название букета", "Статус"]
        )
        self.orders_table.setStyleSheet("""
            QTableWidget {
                background-color: #EBF5EB;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 22px;
                border: 1px solid #1D3A1C;
                gridline-color: #AFC9B9;
            }
            QHeaderView::section {
                background-color: #B4D1C0;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 22px;
                font-weight: 500;
                border: 1px solid #1D3A1C;
                padding: 4px;
            }
            QHeaderView::section:hover,
            QHeaderView::section:pressed,
            QHeaderView::section:checked {
                background-color: #B4D1C0;
                border: 1px solid #1D3A1C;
            }
            QTableWidget::item:selected {
                background-color: #B4D1C0;
                color: #1D321C;
            }
        """)

        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)

        self.orders_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.orders_table.verticalHeader().setVisible(False)

        # двойной клик по заказу — отметить как «Продан» (вручную)
        self.orders_table.doubleClicked.connect(self.mark_sold)

        self.add_shadow(self.orders_table)

    def create_action_buttons(self):
        self.add_btn = QPushButton("Добавить заказ", self)
        self.add_btn.setGeometry(1250, 700, 300, 70)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #1D693C;
                border-radius: 25px;
                font-size: 32px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #8BBFA0;
            }
        """)
        self.add_shadow(self.add_btn)
        self.add_btn.clicked.connect(self.add_order)

        self.del_btn = QPushButton("Удалить заказ", self)
        self.del_btn.setGeometry(1250, 800, 300, 70)
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 25px;
                font-size: 32px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_btn)
        self.del_btn.clicked.connect(self.delete_order)

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
            QPushButton:hover {
                background-color: #AFD2B1;
            }
        """)
        self.add_shadow(self.exit_button)
        self.exit_button.clicked.connect(self.go_back)

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

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        widget.setGraphicsEffect(shadow)

    def showEvent(self, event):
        """При показе окна — синхронизируем все заказы с букетами."""
        super().showEvent(event)
        try:
            db.sync_all_orders()
        except Exception:
            pass
        # пересобираем текущий месяц
        try:
            self.build_month()
        except Exception:
            pass

    def build_month(self):
        self.month_label.setText(
            f"{self.MONTHS_RU[self.view_month]} {self.view_year}"
        )

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.view_year, self.view_month)

        today = date.today()

        for r in range(6):
            for c in range(7):
                self.day_buttons[r][c].setText("")
                self.day_buttons[r][c].setEnabled(False)
                self.day_buttons[r][c].setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #1D321C;
                        font-size: 26px;
                        font-family: 'Cormorant Infant';
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #EAF3EB;
                        border-radius: 25px;
                    }
                """)
                self.day_stripes[r][c].setStyleSheet("""
                    QLabel {
                        background-color: transparent;
                    }
                """)

        for r, week in enumerate(weeks):
            for c, day in enumerate(week):
                if day == 0:
                    continue

                btn = self.day_buttons[r][c]
                btn.setText(str(day))
                btn.setEnabled(True)

                if (self.view_year == today.year
                        and self.view_month == today.month
                        and day == today.day):
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #C8E6C9;
                            color: #1D321C;
                            font-size: 26px;
                            font-family: 'Cormorant Infant';
                            font-weight: 500;
                            border: 1px solid #1D3A1C;
                            border-radius: 25px;
                        }
                        QPushButton:hover {
                            background-color: #AFD2B1;
                        }
                    """)

                key = f"{self.view_year:04d}-{self.view_month:02d}-{day:02d}"
                orders = db.get_orders_by_date(key)

                if not orders:
                    color = "transparent"
                elif all(o["sold"] for o in orders):
                    color = "#E0B84C"      # все проданы — жёлтый
                elif all(o["ready"] for o in orders):
                    color = "#639A78"      # все готовы — зелёный
                else:
                    color = "#B04A4A"      # есть в сборке — красный

                self.day_stripes[r][c].setStyleSheet(
                    f"QLabel {{ background-color: {color}; }}"
                )

        self.selected_day = None
        self.selected_label.setText("На —")
        self.orders_table.setRowCount(0)

    def prev_month(self):
        if self.view_month == 1:
            self.view_month = 12
            self.view_year -= 1
        else:
            self.view_month -= 1
        self.build_month()

    def next_month(self):
        if self.view_month == 12:
            self.view_month = 1
            self.view_year += 1
        else:
            self.view_month += 1
        self.build_month()

    def on_day_click(self, row, col):
        btn = self.day_buttons[row][col]
        if not btn.text():
            return

        day = int(btn.text())
        key = f"{self.view_year:04d}-{self.view_month:02d}-{day:02d}"
        self.selected_day = key

        self.selected_label.setText(
            f"На {day} {self.MONTHS_RU_GEN[self.view_month]} {self.view_year}:"
        )

        self.fill_orders_table(key)

    def fill_orders_table(self, key):
        """Заполняет таблицу заказов по дате."""
        orders = db.get_orders_by_date(key)
        self.orders_table.setRowCount(len(orders))
        for i, o in enumerate(orders):
            if o["sold"]:
                status = "Продан"
            elif o["ready"]:
                status = "Готов"
            else:
                status = "В сборке"

            values = [o["name"], o["number"], o["bouquet"], status]
            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)
                self.orders_table.setItem(i, j, item)

    def add_order(self):
        if not self.selected_day:
            dialogs.warn(self, "Календарь", "Сначала выберите день.")
            return

        name, ok1 = dialogs.get_text(self, "Новый заказ", "Имя клиента:")
        if not ok1 or not name.strip():
            return

        number, ok2 = dialogs.get_text(
            self, "Новый заказ", "Номер заказа:",
            validator=QIntValidator(0, 999999, self)
        )
        if not ok2 or not number.strip():
            return

        bouquet, ok3 = dialogs.get_text(
            self, "Новый заказ", "Название букета:"
        )
        if not ok3 or not bouquet.strip():
            return

        # пробуем взять стоимость из уже собранного букета
        total = db.get_bouquet_total_by_name(bouquet.strip())

        db.add_order(
            self.selected_day,
            name.strip(),
            number.strip(),
            bouquet.strip(),
            False,
            total=total,
        )

        # синхронизируем статус нового заказа с наличием букета
        db.sync_orders_by_bouquet_name(bouquet.strip())

        self.refresh_day(self.selected_day)

    def delete_order(self):
        if not self.selected_day:
            dialogs.warn(self, "Календарь", "Сначала выберите день.")
            return

        row = self.orders_table.currentRow()
        if row < 0:
            dialogs.warn(self, "Календарь", "Выберите заказ в таблице.")
            return

        orders = db.get_orders_by_date(self.selected_day)
        if not (0 <= row < len(orders)):
            return

        order = orders[row]

        # проданный заказ удалить нельзя
        if order["sold"]:
            dialogs.warn(
                self, "Календарь",
                "Проданный заказ нельзя удалить."
            )
            return

        db.delete_order(order["id"])

        self.refresh_day(self.selected_day)

    def mark_sold(self):
        """
        Двойной клик по заказу — отметить его как «Продан».
        Работает только для заказов в статусе «Готов».
        Заказы «В сборке» и «Продан» — не трогаем.

        После отметки заказа списывает один букет с таким названием.
        """
        if not self.selected_day:
            return

        row = self.orders_table.currentRow()
        if row < 0:
            return

        orders = db.get_orders_by_date(self.selected_day)
        if not (0 <= row < len(orders)):
            return

        order = orders[row]

        # уже продан — не трогаем
        if order["sold"]:
            dialogs.warn(
                self, "Календарь",
                "Заказ уже продан."
            )
            return

        # ещё не готов — сначала нужен букет
        if not order["ready"]:
            dialogs.warn(
                self, "Календарь",
                "Нельзя продать заказ, пока он «В сборке».\n"
                "Сначала соберите букет в «Моих букетах»."
            )
            return

        # помечаем заказ как продан
        db.set_order_sold(order["id"])

        # списываем букет с таким названием (если есть в наличии)
        db.sell_bouquet_by_name(order["bouquet"])

        self.refresh_day(self.selected_day)

    def refresh_day(self, key):
        """Обновляет подсветку дня и таблицу заказов по ключу YYYY-MM-DD."""
        y, m, d = key.split("-")
        y = int(y)
        m = int(m)
        d = int(d)

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(y, m)

        for r, week in enumerate(weeks):
            for c, day in enumerate(week):
                if day == d:
                    # обновляем таблицу и метку
                    self.selected_day = key
                    self.selected_label.setText(
                        f"На {d} {self.MONTHS_RU_GEN[m]} {y}:"
                    )
                    self.fill_orders_table(key)

                    # обновляем цвет полоски под днём
                    orders = db.get_orders_by_date(key)
                    if not orders:
                        color = "transparent"
                    elif all(o["sold"] for o in orders):
                        color = "#E0B84C"
                    elif all(o["ready"] for o in orders):
                        color = "#639A78"
                    else:
                        color = "#B04A4A"
                    self.day_stripes[r][c].setStyleSheet(
                        f"QLabel {{ background-color: {color}; }}"
                    )
                    return

    def showMinimized(self):
        """Свернуть окно приложения."""
        win = self.window()
        if win is not None:
            win.showMinimized()