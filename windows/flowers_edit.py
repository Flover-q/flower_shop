from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from windows import dialogs
import db


class FlowersEditWindow(QMainWindow):
    """Окно редактирования справочников: цветы и упаковки."""

    def __init__(self, start_tab="flowers"):
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

        self.current_tab = start_tab   # flowers / packs

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_tabs()
        self.create_table()
        self.create_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.refresh()

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

    def create_title(self):
        """Заголовок «Флора-учёт» и «Справочник»."""
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

        self.subtitle = QLabel("Справочник", self)
        self.subtitle.setGeometry(1140, 30, 423, 70)
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

    def create_tabs(self):
        """Две кнопки-вкладки — по центру окна."""
        self.tab_flowers = QPushButton("Цветы", self)
        self.tab_flowers.setGeometry(650, 190, 300, 70)
        self.tab_flowers.clicked.connect(lambda: self.set_tab("flowers"))

        self.tab_packs = QPushButton("Упаковки", self)
        self.tab_packs.setGeometry(970, 190, 300, 70)
        self.tab_packs.clicked.connect(lambda: self.set_tab("packs"))

        self.add_shadow(self.tab_flowers)
        self.add_shadow(self.tab_packs)
        self.apply_tab_styles()

    def apply_tab_styles(self):
        """Активная вкладка тёмная, неактивная светлая."""
        active = """
            QPushButton {
                background-color: #639A78;
                color: #F0F6F3;
                border-radius: 20px;
                font-size: 34px;
                font-weight: 500;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
        """
        inactive = """
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 20px;
                font-size: 34px;
                font-weight: 500;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """
        self.tab_flowers.setStyleSheet(
            active if self.current_tab == "flowers" else inactive
        )
        self.tab_packs.setStyleSheet(
            active if self.current_tab == "packs" else inactive
        )

    def set_tab(self, tab):
        """Переключает вкладку."""
        self.current_tab = tab
        self.apply_tab_styles()
        self.refresh()

    def create_table(self):
        """Таблица для отображения справочника."""
        self.table = QTableWidget(self)
        self.table.setGeometry(420, 290, 1080, 470)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #EBF5EB;
                alternate-background-color: #F5FAF5;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 26px;
                border: 1px solid #1D3A1C;
                gridline-color: #C8DCC9;
            }
            QHeaderView::section {
                background-color: #B4D1C0;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 26px;
                font-weight: 500;
                border: 1px solid #1D3A1C;
                padding: 12px;
            }
            QTableWidget::item {
                padding: 10px 14px;
            }
            QTableWidget::item:selected {
                background-color: #B4D1C0;
                color: #1D321C;
            }
        """)

        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.add_shadow(self.table)

    def refresh(self):
        """Перерисовывает таблицу под текущую вкладку."""
        if self.current_tab == "flowers":
            self.refresh_flowers()
        else:
            self.refresh_packs()

    def refresh_flowers(self):
        """Заполняет таблицу цветами."""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Цветок", "Цена за 1 шт"])

        flowers = db.get_flowers()
        self.table.setRowCount(len(flowers))
        for i, (name, price) in enumerate(flowers.items()):
            item_name = QTableWidgetItem(name)
            item_name.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item_name)

            item_price = QTableWidgetItem(f"{price:.0f} руб.")
            item_price.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, item_price)

    def refresh_packs(self):
        """Заполняет таблицу упаковками."""
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Упаковка", "Размер", "Цена"])

        packs = db.get_packs()
        self.table.setRowCount(len(packs))
        for i, ((name, size), price) in enumerate(packs.items()):
            values = [name, size, f"{price:.0f} руб."]
            for j, v in enumerate(values):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def create_buttons(self):
        """Кнопки действий."""
        self.add_btn = QPushButton("Добавить", self)
        self.add_btn.setGeometry(420, 790, 340, 75)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #1D693C;
                border-radius: 25px;
                font-size: 38px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #8BBFA0;
            }
        """)
        self.add_shadow(self.add_btn)
        self.add_btn.clicked.connect(self.add_entry)

        self.edit_btn = QPushButton("Изменить цену", self)
        self.edit_btn.setGeometry(790, 790, 340, 75)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 25px;
                font-size: 36px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.edit_btn)
        self.edit_btn.clicked.connect(self.edit_price)

        self.del_btn = QPushButton("Удалить", self)
        self.del_btn.setGeometry(1160, 790, 340, 75)
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 25px;
                font-size: 38px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_btn)
        self.del_btn.clicked.connect(self.delete_entry)

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
        self.exit_button.clicked.connect(self.close)

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
        self.add_shadow(self.min_button)
        self.min_button.clicked.connect(self.showMinimized)

    def add_shadow(self, widget):
        """Добавляет тень под элементом."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        widget.setGraphicsEffect(shadow)

    def add_entry(self):
        """Добавляет цветок или упаковку."""
        if self.current_tab == "flowers":
            self.add_flower()
        else:
            self.add_pack()

    def add_flower(self):
        """Добавляет цветок в БД."""
        name, ok = dialogs.get_text(self, "Новый цветок", "Название:")
        if not ok or not name.strip():
            return

        price, ok = dialogs.get_text(self, "Новый цветок", "Цена за 1 шт:")
        if not ok:
            return

        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            dialogs.warn(self, "Ошибка", "Цена — положительное число.")
            return

        flowers = db.get_flowers()
        if name.strip() in flowers:
            dialogs.warn(self, "Ошибка", "Такой цветок уже есть.")
            return

        db.add_flower(name.strip(), price)
        self.refresh()

    def add_pack(self):
        """Добавляет упаковку — название, размер и цена.

        Название и размер можно выбрать из списка или вписать своё.
        """
        # список существующих названий + возможность вписать своё
        names = db.get_pack_names()
        if not names:
            names = ["Плёнка", "Бумага", "Коробка", "Лента"]

        name, ok = dialogs.get_item(
            self,
            "Новая упаковка",
            "Название упаковки (можно вписать своё):",
            names,
            editable=True
        )
        if not ok or not name.strip():
            return
        name = name.strip()

        # список существующих размеров + возможность вписать своё
        sizes = db.get_pack_sizes()
        if not sizes:
            sizes = ["Маленький", "Средний", "Большой", "Стандарт"]

        size, ok = dialogs.get_item(
            self,
            "Новая упаковка",
            "Размер (можно вписать свой):",
            sizes,
            editable=True
        )
        if not ok or not size.strip():
            return
        size = size.strip()

        # проверка на дубликат
        packs = db.get_packs()
        if (name, size) in packs:
            dialogs.warn(self, "Ошибка", "Такая упаковка уже есть.")
            return

        # цена
        price, ok = dialogs.get_text(self, "Новая упаковка", "Цена, ₽:")
        if not ok:
            return

        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            dialogs.warn(self, "Ошибка", "Цена — положительное число.")
            return

        db.add_pack(name, size, price)
        self.refresh()

    def edit_price(self):
        """Меняет цену выбранной записи."""
        row = self.table.currentRow()
        if row < 0:
            dialogs.warn(self, "Справочник", "Выберите строку в таблице.")
            return

        if self.current_tab == "flowers":
            name = self.table.item(row, 0).text()
            new_price, ok = dialogs.get_text(
                self, "Изменить цену", f"Новая цена для «{name}»:"
            )
            if not ok:
                return
            try:
                new_price = float(new_price)
                if new_price <= 0:
                    raise ValueError
            except ValueError:
                dialogs.warn(self, "Ошибка", "Цена — положительное число.")
                return
            db.update_flower_price(name, new_price)
        else:
            name = self.table.item(row, 0).text()
            size = self.table.item(row, 1).text()
            new_price, ok = dialogs.get_text(
                self, "Изменить цену",
                f"Новая цена для «{name} / {size}»:"
            )
            if not ok:
                return
            try:
                new_price = float(new_price)
                if new_price <= 0:
                    raise ValueError
            except ValueError:
                dialogs.warn(self, "Ошибка", "Цена — положительное число.")
                return
            db.update_pack_price(name, size, new_price)

        self.refresh()

    def delete_entry(self):
        """Удаляет выбранную запись."""
        row = self.table.currentRow()
        if row < 0:
            dialogs.warn(self, "Справочник", "Выберите строку в таблице.")
            return

        if self.current_tab == "flowers":
            name = self.table.item(row, 0).text()
            if not dialogs.confirm(
                self, "Удаление", f"Удалить цветок «{name}»?"
            ):
                return
            db.delete_flower(name)
        else:
            name = self.table.item(row, 0).text()
            size = self.table.item(row, 1).text()
            if not dialogs.confirm(
                self, "Удаление",
                f"Удалить упаковку «{name} / {size}»?"
            ):
                return
            db.delete_pack(name, size)

        self.refresh()