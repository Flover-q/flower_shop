from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QLineEdit
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize

import pyphen

from windows import dialogs
import db


class BouquetsPage(QWidget):
    """Окно «Мои букеты»."""

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.hyphenator = pyphen.Pyphen(lang='ru_RU')
        self.checkbox_mode = False

        # фон
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

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_status_label()
        self.create_search()
        self.create_table()
        self.create_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.bg.lower()

        self.load_bouquets()

    def create_top_bar(self):
        self.top_bar = QLabel(self)
        self.top_bar.setGeometry(240, 0, 1440, 139)
        self.top_bar.setStyleSheet("QLabel { background-color: #EAF3EB; }")
        self.top_bar.lower()

        self.top_line = QLabel(self)
        self.top_line.setGeometry(240, 135, 1440, 5)
        self.top_line.setStyleSheet("QLabel { background-color: #5D6D5F; }")

    def create_bottom_bar(self):
        self.bottom_bar = QLabel(self)
        self.bottom_bar.setGeometry(240, 1050, 1440, 139)
        self.bottom_bar.setStyleSheet("QLabel { background-color: #EAF3EB; }")
        self.bottom_bar.lower()

    def create_side_bars(self):
        self.left_bar = QLabel(self)
        self.left_bar.setGeometry(-9760, 0, 10000, 2000)
        self.left_bar.setStyleSheet("QLabel { background-color: #8BA48B; }")
        self.left_bar.lower()

        self.right_bar = QLabel(self)
        self.right_bar.setGeometry(1680, 0, 10000, 2000)
        self.right_bar.setStyleSheet("QLabel { background-color: #8BA48B; }")
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

        self.subtitle = QLabel("Мои букеты", self)
        self.subtitle.setGeometry(1140, 25, 540, 80)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

    def create_status_label(self):
        self.status_label = QLabel("В наличии: — шт.", self)
        self.status_label.setGeometry(300, 165, 900, 50)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 34px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

    def create_search(self):
        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(950, 165, 420, 45)
        self.search_input.setPlaceholderText("Поиск по названию букета...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #EBF5EB;
                color: #1D321C;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                border-radius: 15px;
                padding-left: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #639A78;
            }
        """)

        self.search_btn = QPushButton(self)
        self.search_btn.setGeometry(1385, 165, 45, 45)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border: 1px solid #1D3A1C;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
            QPushButton:pressed {
                background-color: #72917F;
            }
        """)
        self.search_btn.setIcon(QIcon("images/lupa.png"))
        self.search_btn.setIconSize(QSize(30, 30))
        self.search_btn.clicked.connect(self.filter_bouquets)
        self.add_shadow(self.search_btn)

    def create_table(self):
        self.table = QTableWidget(self)
        self.table.setGeometry(280, 220, 1350, 660)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Дата", "Название", "Цветы",
            "Упаковка", "Размер", "Работа",
            "Итого", "Себестоим.", "Статус", "Было всего", "В наличии", "id"
        ])

        self.table.setColumnHidden(11, True)

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
            QTableWidget::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #1D3A1C;
                border-radius: 8px;
                background-color: #F0F6F3;
            }
            QTableWidget::indicator:hover {
                border: 2px solid #72917F;
                background-color: #EAF3EB;
            }
            QTableWidget::indicator:checked {
                background-color: #639A78;
                border: 2px solid #1D3A1C;
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)

        self.table.setWordWrap(True)
        self.table.verticalHeader().setDefaultSectionSize(60)

        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.verticalHeader().setVisible(False)

        self.table.itemChanged.connect(self.on_item_changed)
        self.table.doubleClicked.connect(self.on_double_click)

        self.add_shadow(self.table)

    def create_buttons(self):
        self.del_btn = QPushButton("Удалить выбранные", self)
        self.del_btn.setGeometry(1280, 910, 350, 80)
        self.del_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 25px;
                font-size: 36px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_btn)
        self.del_btn.clicked.connect(self.delete_bouquet)

        self.cancel_btn = QPushButton("Отмена", self)
        self.cancel_btn.setGeometry(1090, 910, 170, 80)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8E6C9;
                color: #4A7C59;
                border-radius: 25px;
                font-size: 36px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #AFD2B1;
            }
        """)
        self.add_shadow(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.cancel_checkbox_mode)
        self.cancel_btn.hide()

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

        self.min_button.clicked.connect(self._minimize)

    def _minimize(self):
        win = self.window()
        if win is not None:
            win.showMinimized()

    def go_back(self):
        self.app.go_to("main")

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        widget.setGraphicsEffect(shadow)

    def add_soft_hyphens(self, text):
        result = []
        for word in text.split(" "):
            if len(word) <= 5:
                result.append(word)
                continue
            if "×" in word:
                name, sep, num = word.partition("×")
                if len(name) > 5:
                    hyphenated = self.hyphenator.inserted(
                        name, hyphen="\u00ad"
                    )
                    result.append(hyphenated + "×" + num)
                else:
                    result.append(word)
            else:
                hyphenated = self.hyphenator.inserted(word, hyphen="\u00ad")
                result.append(hyphenated)
        return " ".join(result)

    def load_bouquets(self):
        self.table.blockSignals(True)
        col_shift = 1 if self.checkbox_mode else 0

        bouquets = db.get_bouquets()
        self.table.setRowCount(len(bouquets))
        for i, b in enumerate(bouquets):
            name = b.get("name", "")
            name_display = self.add_soft_hyphens(name)
            sold = b.get("sold", False)
            cnt = b.get("count", 1)
            initial = b.get("initial_count", cnt)
            in_stock = db.count_unsold_by_name(name)

            work_val = b.get("work", "")
            total_val = b.get("total", "")
            cost_val = b.get("cost", "")

            flowers_text = self.add_soft_hyphens(
                b.get("flowers", "")
                .replace(",", ", ")
                .replace("×", " × ")
            )

            values = [
                b.get("date", ""),
                name_display,
                flowers_text,
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

            if self.checkbox_mode:
                cb = QTableWidgetItem("")
                cb.setFlags(
                    Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
                    | Qt.ItemIsSelectable
                )
                cb.setCheckState(Qt.Unchecked)
                cb.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 0, cb)

            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)

                if j == 8:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                elif j == 9:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table.setItem(i, j + col_shift, item)

        self.table.resizeRowsToContents()
        self.update_status_label()
        self.table.blockSignals(False)

    def filter_bouquets(self):
        text = self.search_input.text().strip().lower()

        if not text:
            self.load_bouquets()
            return

        self.table.blockSignals(True)
        col_shift = 1 if self.checkbox_mode else 0

        bouquets = db.get_bouquets()
        filtered = [b for b in bouquets if text in b.get("name", "").lower()]
        self.table.setRowCount(len(filtered))

        for i, b in enumerate(filtered):
            name = b.get("name", "")
            name_display = self.add_soft_hyphens(name)
            sold = b.get("sold", False)
            cnt = b.get("count", 1)
            initial = b.get("initial_count", cnt)
            in_stock = db.count_unsold_by_name(name)

            work_val = b.get("work", "")
            total_val = b.get("total", "")
            cost_val = b.get("cost", "")

            flowers_text = self.add_soft_hyphens(
                b.get("flowers", "")
                .replace(",", ", ")
                .replace("×", " × ")
            )

            values = [
                b.get("date", ""),
                name_display,
                flowers_text,
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

            if self.checkbox_mode:
                cb = QTableWidgetItem("")
                cb.setFlags(
                    Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
                    | Qt.ItemIsSelectable
                )
                cb.setCheckState(Qt.Unchecked)
                cb.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 0, cb)

            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)

                if j == 8:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                elif j == 9:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table.setItem(i, j + col_shift, item)

        self.table.resizeRowsToContents()
        self.table.blockSignals(False)

    def update_status_label(self):
        in_stock = db.count_unsold_bouquets()
        total = db.count_bouquets_total()
        self.status_label.setText(
            f"В наличии: {in_stock} шт.   (всего собрано: {total})"
        )

    def _col(self, base):
        return base + 1 if self.checkbox_mode else base

    def get_id_by_row(self, row):
        id_item = self.table.item(row, self._col(11))
        if id_item is None:
            return None
        try:
            return int(id_item.text())
        except ValueError:
            return None

    def get_name_by_row(self, row):
        name_item = self.table.item(row, self._col(1))
        return name_item.text() if name_item else ""

    def get_date_by_row(self, row):
        date_item = self.table.item(row, self._col(0))
        return date_item.text() if date_item else ""

    def on_double_click(self, index):
        row = index.row()
        col = index.column()
        if col != self._col(8):
            return
        bouquet_id = self.get_id_by_row(row)
        if bouquet_id is None:
            return
        name = self.get_name_by_row(row).replace("\u00ad", "")
        db.toggle_bouquet_sold(bouquet_id)
        if name:
            db.sync_orders_by_bouquet_name(name)
        self.load_bouquets()

    def on_item_changed(self, item):
        col = item.column()
        row = item.row()
        if col != self._col(9):
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
        name = self.get_name_by_row(row).replace("\u00ad", "")
        db.update_bouquet_initial_count(bouquet_id, new_count)
        if name:
            db.sync_orders_by_bouquet_name(name)
        self.load_bouquets()

    def delete_bouquet(self):
        if not self.checkbox_mode:
            self._enable_checkbox_mode()
            return

        rows = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item is not None and item.checkState() == Qt.Checked:
                rows.append(i)

        if not rows:
            dialogs.warn(self, "Мои букеты", "Отметьте букеты галочками.")
            return

        # Собираем id и имя (имя — только для вопроса)
        targets = []
        for row in rows:
            bouquet_id = self.get_id_by_row(row)
            name = self.get_name_by_row(row).replace("\u00ad", "")
            if bouquet_id is not None:
                targets.append((bouquet_id, name))

        if not targets:
            dialogs.warn(self, "Мои букеты", "Не удалось определить букеты.")
            return

        if len(targets) == 1:
            text = f"Удалить букет «{targets[0][1]}»?"
        else:
            text = f"Удалить {len(targets)} букетов?"

        if not dialogs.confirm(self, "Удаление", text):
            return

        for bouquet_id, name in targets:
            db.delete_bouquet_by_id(bouquet_id)
            if name and name != "—":
                db.sync_orders_by_bouquet_name(name)

        self._disable_checkbox_mode()
        self.load_bouquets()

    def cancel_checkbox_mode(self):
        """Отмена режима галочек."""
        self._disable_checkbox_mode()
        self.load_bouquets()

    def _enable_checkbox_mode(self):
        self.checkbox_mode = True
        self.del_btn.setText("Удалить отмеченные")
        self.cancel_btn.show()
        self.cancel_btn.raise_()

        self.table.insertColumn(0)

        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Fixed
        )

        header_item = QTableWidgetItem("✓")
        header_item.setTextAlignment(Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(0, header_item)

        self.table.setColumnWidth(0, 35)
        self.table.setColumnHidden(12, True)

        self.load_bouquets()

    def _disable_checkbox_mode(self):
        self.checkbox_mode = False
        self.del_btn.setText("Удалить выбранные")
        self.cancel_btn.hide()

        self.table.clear()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Дата", "Название", "Цветы",
            "Упаковка", "Размер", "Работа",
            "Итого", "Себестоим.", "Статус", "Было всего", "В наличии", "id"
        ])
        self.table.setColumnHidden(11, True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    def showMinimized(self):
        win = self.window()
        if win is not None:
            win.showMinimized()