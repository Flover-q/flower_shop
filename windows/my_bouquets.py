from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from windows import dialogs
import db


class BouquetsWindow(QMainWindow):
    """Окно «Мои букеты»."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Флора-учёт")
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
        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_status_label()
        self.create_table()
        self.create_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.load_bouquets()

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
        """Заголовок «Флора-учёт» и «Мои букеты»."""
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

        self.subtitle = QLabel("Мои букеты", self)
        self.subtitle.setGeometry(1140, 25, 540, 80)
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

    #  СТРОКА «В наличии: X шт. (всего собрано: Y)»
    def create_status_label(self):
        """Надпись над таблицей."""
        self.status_label = QLabel("В наличии: — шт.", self)
        self.status_label.setGeometry(300, 165, 900, 50)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #124612;
                font-size: 34px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

    #  ТАБЛИЦА БУКЕТОВ
    def create_table(self):
        """Таблица со всеми букетами."""
        self.table = QTableWidget(self)
        self.table.setGeometry(280, 220, 1350, 660)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Дата", "Название", "Цветы",
            "Упаковка", "Размер", "Работа",
            "Итого", "Себестоим.", "Статус", "Было всего", "В наличии", "id"
        ])

        self.table.setColumnHidden(11, True)   # id — скрытая

        self.table.setStyleSheet("""
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
                padding: 6px;
            }
            QHeaderView::section:hover,
            QHeaderView::section:pressed,
            QHeaderView::section:checked {
                background-color: #B4D1C0;
                border: 1px solid #1D3A1C;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #B4D1C0;
                color: #1D321C;
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)

        self.table.setWordWrap(True)
        self.table.verticalHeader().setDefaultSectionSize(60)

        # разрешаем редактирование по клику / двойному клику / F2
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)

        # реагируем на изменение ячейки — для колонки «Было всего»
        self.table.itemChanged.connect(self.on_item_changed)

        # двойной клик по колонке «Статус» переключает sold
        self.table.doubleClicked.connect(self.on_double_click)

        self.add_shadow(self.table)

    #  КНОПКА «УДАЛИТЬ БУКЕТ»
    def create_buttons(self):
        """Кнопка «Удалить букет»."""
        self.del_btn = QPushButton("Удалить букет", self)
        self.del_btn.setGeometry(1320, 910, 310, 80)
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 25px;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_btn)
        self.del_btn.clicked.connect(self.delete_bouquet)

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
    def load_bouquets(self):
        """Заполняет таблицу всеми букетами из БД."""
        # отключаем сигнал, чтобы не срабатывал на каждую ячейку
        self.table.blockSignals(True)

        bouquets = db.get_bouquets()
        self.table.setRowCount(len(bouquets))
        for i, b in enumerate(bouquets):
            name = b.get("name", "")
            sold = b.get("sold", False)
            cnt = b.get("count", 1)
            initial = b.get("initial_count", cnt)

            in_stock = db.count_unsold_by_name(name)

            work_val = b.get("work", "")
            total_val = b.get("total", "")
            cost_val = b.get("cost", "")

            values = [
                b.get("date", ""),
                name,
                b.get("flowers", ""),
                b.get("pack", ""),
                b.get("size", ""),
                f"{work_val} ₽" if work_val not in ("", None) else "",
                f"{total_val} ₽" if total_val not in ("", None) else "",
                f"{cost_val} ₽" if cost_val not in ("", None) else "",
                "Продан" if sold else "В наличии",
                f"{initial} шт.",
                f"{in_stock} шт." if in_stock > 0 else "—",
                str(b.get("id", "")),
            ]
            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)

                # колонка «Статус» — редактируемая
                if j == 8:
                    item.setFlags(
                        item.flags() | Qt.ItemIsEditable
                    )
                # колонка «Было всего» — редактируемая
                elif j == 9:
                    item.setFlags(
                        item.flags() | Qt.ItemIsEditable
                    )
                else:
                    item.setFlags(
                        item.flags() & ~Qt.ItemIsEditable
                    )

                self.table.setItem(i, j, item)

        self.table.resizeRowsToContents()
        self.update_status_label()

        self.table.blockSignals(False)

    def update_status_label(self):
        """Обновляет строку над таблицей."""
        in_stock = db.count_unsold_bouquets()
        total = db.count_bouquets_total()
        self.status_label.setText(
            f"В наличии: {in_stock} шт.   (всего собрано: {total})"
        )

    def get_id_by_row(self, row):
        """Возвращает id букета из скрытой колонки (11) или None."""
        id_item = self.table.item(row, 11)
        if id_item is None:
            return None
        try:
            return int(id_item.text())
        except ValueError:
            return None

    def on_double_click(self, index):
        """Двойной клик по колонке «Статус» — переключает sold."""
        row = index.row()
        col = index.column()

        # интересует только колонка «Статус»
        if col != 8:
            return

        bouquet_id = self.get_id_by_row(row)
        if bouquet_id is None:
            return

        # запоминаем название до переключения
        name_item = self.table.item(row, 1)
        name = name_item.text() if name_item else ""

        db.toggle_bouquet_sold(bouquet_id)

        # синхронизируем заказы с этим названием
        if name:
            db.sync_orders_by_bouquet_name(name)

        self.load_bouquets()

    def on_item_changed(self, item):
        """Реагирует на изменение ячейки в колонке «Было всего»."""
        col = item.column()
        row = item.row()

        # только колонка «Было всего»
        if col != 9:
            # колонку «Статус» обрабатываем через on_double_click
            return

        bouquet_id = self.get_id_by_row(row)
        if bouquet_id is None:
            return

        text = item.text().replace("шт.", "").strip()
        if not text.isdigit() or int(text) <= 0:
            dialogs.warn(self, "Мои букеты", "Введите число больше нуля.")
            self.load_bouquets()
            return

        new_count = int(text)

        # запоминаем название
        name_item = self.table.item(row, 1)
        name = name_item.text() if name_item else ""

        db.update_bouquet_initial_count(bouquet_id, new_count)

        # синхронизируем заказы с этим названием
        if name:
            db.sync_orders_by_bouquet_name(name)

        self.load_bouquets()

    def delete_bouquet(self):
        """Удаляет выбранный букет из БД с подтверждением."""
        row = self.table.currentRow()
        if row < 0:
            dialogs.warn(self, "Мои букеты", "Выберите букет в таблице.")
            return

        name_item = self.table.item(row, 1)
        date_item = self.table.item(row, 0)
        name = name_item.text() if name_item else "—"
        date_str = date_item.text() if date_item else ""

        if not dialogs.confirm(self, "Удаление", f"Удалить букет «{name}»?"):
            return

        db.delete_bouquet_by_name(name, date_str)

        # синхронизируем заказы с этим названием
        if name and name != "—":
            db.sync_orders_by_bouquet_name(name)

        self.load_bouquets()