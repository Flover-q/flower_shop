from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QLineEdit, QComboBox, QListWidget
from PyQt5.QtWidgets import QMenu, QWidgetAction, QCheckBox
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor, QPalette, QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, QPoint

import re
from datetime import date
import db
from windows import dialogs


class CheckableButton(QPushButton):
    """Кнопка с выпадающим меню из чекбоксов с ценами и скроллом."""

    def __init__(self, prices, parent=None):
        super().__init__(parent)
        self.prices = dict(prices)
        self.checks = {}

        self.setText("Выберите цветок")
        self.setStyleSheet("""
            QPushButton {
                background-color: #90B29E;
                color: #000000;
                font-weight: 500;
                border-radius: 20px;
                font-size: 26px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 55px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #72917F;
            }
            QPushButton::menu-indicator {
                image: none;
                width: 0px;
                height: 0px;
            }
        """)

        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
                padding: 0px;
                color: #1D321C;
            }
            QWidget {
                background-color: #F0F6F3;
                color: #1D321C;
            }
        """)

        self.container = QWidget()
        self.container.setStyleSheet("background-color: #F0F6F3;")
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setContentsMargins(0, 6, 0, 6)
        self.vbox.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)
        self.scroll.setFixedWidth(320)
        self.scroll.setStyleSheet("""
            QScrollArea {
                background-color: #F0F6F3;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #F0F6F3;
            }
            QScrollBar:vertical {
                background-color: #EAF3EB;
                width: 12px;
                border: none;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #90B29E;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #72917F;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
                background: transparent;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        action = QWidgetAction(self.menu)
        action.setDefaultWidget(self.scroll)
        self.menu.addAction(action)

        self.clicked.connect(self.show_menu_centered)

    def rebuild(self, prices):
        """Пересобирает чекбоксы под новые цены из БД."""
        checked_names = [n for n, cb in self.checks.items() if cb.isChecked()]

        self.prices = dict(prices)
        self.checks = {}

        while self.vbox.count():
            item = self.vbox.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        for name, price in self.prices.items():
            text = f"{name}    {price:.0f} ₽"
            cb = QCheckBox(text)
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 24px;
                    font-family: 'Cormorant Infant';
                    color: #1D321C;
                    padding: 6px 18px;
                    spacing: 12px;
                    background-color: #F0F6F3;
                }
                QCheckBox:hover {
                    background-color: #EAF3EB;
                }
                QCheckBox::indicator {
                    width: 22px;
                    height: 22px;
                    border: 2px solid #5D6D5F;
                    border-radius: 5px;
                    background-color: #F0F6F3;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #72917F;
                    background-color: #EAF3EB;
                }
                QCheckBox::indicator:checked {
                    background-color: #639A78;
                    border: 2px solid #1D3A1C;
                }
            """)
            if name in checked_names:
                cb.setChecked(True)
            cb.stateChanged.connect(self.update_text)
            self.vbox.addWidget(cb)
            self.checks[name] = cb

        self.vbox.addStretch()
        self.update_text()

    def show_menu_centered(self):
        """Перечитывает цветы из БД, пересобирает список, показывает меню."""
        self.rebuild(db.get_flowers())

        self.menu.adjustSize()
        menu_w = self.menu.sizeHint().width()
        btn_w = self.width()
        dx = (btn_w - menu_w) // 2
        pos = self.mapToGlobal(QPoint(dx, self.height()))
        self.menu.popup(pos)

    def update_text(self):
        """Обновляет текст кнопки по отмеченным чекбоксам."""
        checked = [name for name, cb in self.checks.items() if cb.isChecked()]
        if checked:
            self.setText(", ".join(checked))
        else:
            self.setText("Выберите цветок")

        parent = self.parent()
        if hasattr(parent, "update_count_flowers"):
            parent.update_count_flowers(checked)

    def get_flowers(self):
        """Список отмеченных цветов."""
        return [name for name, cb in self.checks.items() if cb.isChecked()]


class BouquetWindow(QMainWindow):
    """Окно «Собрать букет»."""

    SIZES = ["Маленький", "Средний", "Большой"]

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

        self.FLOWER_PRICES = db.get_flowers()
        self.PACK_PRICES = db.get_packs()

        self.flowers_count = {}
        self.packs_count = []   # список (упаковка, размер, цена)
        self._shadows = []

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_fields()
        self.create_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.update_count_flowers([])

        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()

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

        self.subtitle = QLabel("Собрать букет", self)
        self.subtitle.setGeometry(1140, 25, 423, 80)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

    def create_fields(self):
        self.label_flowers = QLabel("Цветы:", self)
        self.label_flowers.setGeometry(520, 150, 180, 75)
        self.label_flowers.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 48px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_flowers = QLabel(self)
        self.line_flowers.setGeometry(520, 215, 380, 5)
        self.line_flowers.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.flowers = CheckableButton(self.FLOWER_PRICES, self)
        self.flowers.setGeometry(910, 165, 405, 55)
        self.add_shadow(self.flowers)

        self.flowers_arrow = QLabel(self)
        self.flowers_arrow.setGeometry(1270, 173, 40, 40)
        self.flowers_arrow.setStyleSheet("QLabel { background: transparent; }")
        self.flowers_arrow.setPixmap(
            QIcon("images/vniz.png").pixmap(40, 40)
        )
        self.flowers_arrow.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.flowers_arrow.raise_()

        self.label_count = QLabel("Количество:", self)
        self.label_count.setGeometry(520, 230, 300, 100)
        self.label_count.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 48px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_count = QLabel(self)
        self.line_count.setGeometry(520, 305, 380, 5)
        self.line_count.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.count_flower = QComboBox(self)
        self.count_flower.setGeometry(910, 250, 300, 55)
        self.count_flower.setStyleSheet("""
            QComboBox {
                background-color: #90B29E;
                color: #000000;
                font-weight: 500;
                border-radius: 20px;
                font-size: 26px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
            }
            QComboBox:hover {
                background-color: #72917F;
            }
            QComboBox::drop-down {
                border: none;
                width: 55px;
            }
            QComboBox::down-arrow {
                image: url(images/vniz.png);
                width: 40px;
                height: 40px;
            }
            QComboBox QAbstractItemView {
                background-color: #F0F6F3;
                color: #000000;
                selection-background-color: #B5DCC5;
                selection-color: #1D321C;
                font-size: 24px;
                font-family: 'Cormorant Infant';
            }
        """)
        self.add_shadow(self.count_flower)

        self.count = QLineEdit(self)
        self.count.setGeometry(1220, 250, 95, 55)
        self.count.setPlaceholderText("Кол-во")
        self.count.setStyleSheet("""
            QLineEdit {
                background-color: #F0F6F3;
                color: #000000;
                font-weight: 500;
                font-size: 20px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 8px;
            }
        """)
        self.count.setValidator(QIntValidator(1, 9999, self))
        self.add_shadow(self.count)

        self.add_count_btn = QPushButton("+", self)
        self.add_count_btn.setGeometry(1325, 255, 40, 40)
        self.add_count_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 20px;
                font-size: 30px;
                font-family: 'Cormorant Infant';
                font-weight: 500;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.add_count_btn)
        self.add_count_btn.clicked.connect(self.add_count)

        self.count_list = QListWidget(self)
        self.count_list.setGeometry(910, 330, 380, 80)
        self.count_list.setStyleSheet("""
            QListWidget {
                background-color: #F0F6F3;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 22px;
                border: 1px solid #1D3A1C;
            }
            QListWidget::item {
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: #B5DCC5;
                color: #1D321C;
            }
        """)
        self.add_shadow(self.count_list)

        self.del_count_btn = QPushButton("−", self)
        self.del_count_btn.setGeometry(1380, 255, 40, 40)
        self.del_count_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 20px;
                font-size: 30px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_count_btn)
        self.del_count_btn.clicked.connect(self.del_count)

        # ─── Упаковка ───
        self.label_pack = QLabel("Упаковка:", self)
        self.label_pack.setGeometry(410, 420, 300, 80)
        self.label_pack.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_pack = QLabel(self)
        self.line_pack.setGeometry(410, 490, 380, 5)
        self.line_pack.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.pack = QComboBox(self)
        self.pack.setGeometry(800, 435, 405, 55)
        self.pack.setStyleSheet(self.count_flower.styleSheet())
        pack_names = sorted({name for (name, size) in self.PACK_PRICES})
        self.pack.addItem("Выберите упаковку")
        self.pack.addItem("Без упаковки")
        self.pack.addItems(pack_names)
        self.pack.currentIndexChanged.connect(self.update_pack_price)
        self.pack.view().setMinimumWidth(300)

        # ─── Размер ───
        self.label_size = QLabel("Размер:", self)
        self.label_size.setGeometry(410, 510, 300, 80)
        self.label_size.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_size = QLabel(self)
        self.line_size.setGeometry(410, 580, 380, 5)
        self.line_size.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.size = QComboBox(self)
        self.size.setGeometry(800, 525, 405, 55)
        self.size.setStyleSheet(self.count_flower.styleSheet())

        # ─── Список упаковок справа ───
        self.packs_list = QListWidget(self)
        self.packs_list.setGeometry(1280, 435, 260, 150)
        self.packs_list.setStyleSheet("""
            QListWidget {
                background-color: #F0F6F3;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 20px;
                border: 1px solid #1D3A1C;
            }
            QListWidget::item {
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: #B5DCC5;
                color: #1D321C;
            }
        """)
        self.add_shadow(self.packs_list)

        self.add_pack_btn = QPushButton("+", self)
        self.add_pack_btn.setGeometry(1230, 470, 40, 40)
        self.add_pack_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 20px;
                font-size: 30px;
                font-family: 'Cormorant Infant';
                font-weight: 500;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.add_pack_btn)
        self.add_pack_btn.clicked.connect(self.add_pack_to_list)

        self.del_pack_btn = QPushButton("−", self)
        self.del_pack_btn.setGeometry(1230, 520, 40, 40)
        self.del_pack_btn.setStyleSheet("""
            QPushButton {
                background-color: #DACAD5;
                color: #995884;
                border-radius: 20px;
                font-size: 30px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #C9B2C2;
            }
        """)
        self.add_shadow(self.del_pack_btn)
        self.del_pack_btn.clicked.connect(self.del_pack_from_list)

        # ─── Работа ───
        self.label_work = QLabel("Работа:", self)
        self.label_work.setGeometry(520, 600, 300, 80)
        self.label_work.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_work = QLabel(self)
        self.line_work.setGeometry(520, 670, 380, 5)
        self.line_work.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.work = QLineEdit(self)
        self.work.setGeometry(910, 615, 405, 55)
        self.work.setPlaceholderText("Введите цену работы")
        self.work.setStyleSheet("""
            QLineEdit {
                background-color: #F0F6F3;
                color: #000000;
                font-weight: 500;
                font-size: 26px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 35px;
            }
        """)
        self.work.setValidator(QDoubleValidator(0, 999999, 2, self))

        self.work_rub = QLabel("₽", self)
        self.work_rub.setGeometry(910 + 405 - 35, 615 + 13, 30, 30)
        self.work_rub.setStyleSheet("""
            QLabel {
                color: #4A7C59;
                font-size: 26px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)
        self.work_rub.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.work_rub.raise_()

        # ─── Название ───
        self.label_name = QLabel("Название\nбукета:", self)
        self.label_name.setGeometry(410, 735, 300, 110)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_name = QLabel(self)
        self.line_name.setGeometry(475, 845, 150, 5)
        self.line_name.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.name = QLineEdit(self)
        self.name.setGeometry(685, 755, 404, 79)
        self.name.setPlaceholderText("Введите название букета")
        self.name.setStyleSheet(self.work.styleSheet())

        self.add_shadow(self.pack)
        self.add_shadow(self.size)
        self.add_shadow(self.work)
        self.add_shadow(self.name)

        self.update_pack_price()

    def update_pack_price(self):
        """Пересобирает список размеров с ценами для выбранной упаковки."""
        name = self.pack.currentText()

        self.size.blockSignals(True)
        self.size.clear()

        self.size.addItem("Выберите размер")

        if name in ("Выберите упаковку", "Без упаковки"):
            self.size.setCurrentIndex(0)
            self.size.blockSignals(False)
            return

        for s in self.SIZES:
            price = self.PACK_PRICES.get((name, s))
            if price is None:
                self.size.addItem(f"{s}    — ₽")
            else:
                self.size.addItem(f"{s}    {price:.0f} ₽")

        self.size.setCurrentIndex(0)
        self.size.blockSignals(False)

    def add_pack_to_list(self):
        """Добавляет пару «упаковка / размер» в список справа."""
        name = self.pack.currentText().strip()
        size = self.size.currentText().split("    ")[0].strip()

        if name in ("Выберите упаковку", "Без упаковки"):
            dialogs.warn(self, "Упаковка", "Сначала выберите упаковку.")
            return

        if size == "Выберите размер":
            dialogs.warn(self, "Упаковка", "Выберите размер упаковки.")
            return

        price = self.PACK_PRICES.get((name, size), 0) or 0

        self.packs_count.append((name, size, price))
        self.packs_list.addItem(f"{name} / {size} — {price:.0f} ₽")

    def del_pack_from_list(self):
        """Удаляет выбранную строку из списка упаковок."""
        row = self.packs_list.currentRow()
        if row < 0:
            dialogs.warn(self, "Упаковка", "Выберите строку в списке.")
            return

        self.packs_list.takeItem(row)
        self.packs_count.pop(row)

    def create_buttons(self):
        self.button = QPushButton("Рассчитать", self)
        self.button.setGeometry(1255, 710, 275, 75)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 42px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.button)
        self.button.clicked.connect(self.calculate)

        self.save_btn = QPushButton("Сохранить", self)
        self.save_btn.setGeometry(1255, 810, 275, 75)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 42px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.add_shadow(self.save_btn)
        self.save_btn.clicked.connect(self.save_bouquet)

        self.label_total = QLabel("Итого:", self)
        self.label_total.setGeometry(1150, 920, 150, 50)
        self.label_total.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_total = QLabel(self)
        self.line_total.setGeometry(1150, 965, 135, 5)
        self.line_total.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.total = QLineEdit(self)
        self.total.setGeometry(1330, 920, 200, 50)
        self.total.setStyleSheet("""
            QLineEdit {
                background-color: #D0E2D7;
                color: #1D321C;
                font-weight: 500;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 30px;
            }
        """)
        self.total.setReadOnly(True)

        self.total_rub = QLabel("₽", self)
        self.total_rub.setGeometry(1330 + 200 - 30, 920 + 12, 25, 25)
        self.total_rub.setStyleSheet("""
            QLabel {
                color: #4A7C59;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)
        self.total_rub.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.total_rub.raise_()

        self.label_cost = QLabel("Себестоимость:", self)
        self.label_cost.setGeometry(530, 920, 400, 50)
        self.label_cost.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 42px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_cost = QLabel(self)
        self.line_cost.setGeometry(530, 965, 330, 5)
        self.line_cost.setStyleSheet("QLabel { background-color: #AFC9B9; }")

        self.cost = QLineEdit(self)
        self.cost.setGeometry(890, 920, 200, 50)
        self.cost.setStyleSheet("""
            QLineEdit {
                background-color: #D0E2D7;
                color: #1D321C;
                font-weight: 500;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 30px;
            }
        """)
        self.cost.setReadOnly(True)

        self.cost_rub = QLabel("₽", self)
        self.cost_rub.setGeometry(890 + 200 - 30, 920 + 12, 25, 25)
        self.cost_rub.setStyleSheet("""
            QLabel {
                color: #4A7C59;
                font-size: 22px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)
        self.cost_rub.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.cost_rub.raise_()

        self.add_shadow(self.total)
        self.add_shadow(self.cost)

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
                font-weight: 400;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #AFD2B1;
            }
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
                font-weight: 300;
            }
            QPushButton:hover {
                background-color: #AFD2B1;
            }
        """)
        self.add_shadow(self.min_button)
        self.min_button.clicked.connect(self.showMinimized)

    def add_shadow(self, widget):
        """Псевдотень: серая плашка под элементом."""
        geo = widget.geometry()

        radius = 0
        style = widget.styleSheet() or ""
        m = re.search(r"border-radius\s*:\s*(\d+)", style)
        if m:
            radius = int(m.group(1))

        shadow = QLabel(self)
        shadow.setGeometry(geo.x() + 15, geo.y() + 15, geo.width(), geo.height())
        shadow.setStyleSheet(f"""
            QLabel {{
                background-color: #D0DDD5;
                border-radius: {radius}px;
            }}
        """)
        shadow.setAttribute(Qt.WA_TransparentForMouseEvents)
        shadow.lower()

        self._shadows.append(shadow)

    def update_count_flowers(self, checked):
        self.count_flower.blockSignals(True)
        self.count_flower.clear()

        self.count_flower.addItem("Выберите цветок")
        if checked:
            self.count_flower.addItems(checked)

        self.count_flower.setCurrentIndex(0)
        self.count_flower.blockSignals(False)

    def add_count(self):
        name = self.count_flower.currentText().strip()
        cnt = self.count.text().strip()

        if name == "Выберите цветок":
            dialogs.warn(self, "Количество", "Сначала выберите цветок.")
            return
        if not cnt.isdigit() or int(cnt) <= 0:
            dialogs.warn(self, "Количество", "Введите количество больше нуля.")
            return

        self.flowers_count[name] = int(cnt)
        self.count.clear()
        self.update_count_list()

    def del_count(self):
        row = self.count_list.currentRow()
        if row < 0:
            dialogs.warn(self, "Количество", "Выберите строку в списке.")
            return

        text = self.count_list.item(row).text()
        name = text.split(" — ")[0]
        self.flowers_count.pop(name, None)
        self.update_count_list()

    def update_count_list(self):
        self.count_list.clear()
        for name, cnt in self.flowers_count.items():
            self.count_list.addItem(f"{name} — {cnt} шт")

    def reset(self):
        """Сбрасывает окно и перезагружает справочники из БД."""
        self.FLOWER_PRICES = db.get_flowers()
        self.PACK_PRICES = db.get_packs()

        for name, cb in self.flowers.checks.items():
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        self.flowers.setText("Выберите цветок")

        self.flowers.rebuild(self.FLOWER_PRICES)

        self.pack.blockSignals(True)
        self.pack.clear()
        pack_names = sorted({name for (name, size) in self.PACK_PRICES})
        self.pack.addItem("Выберите упаковку")
        self.pack.addItem("Без упаковки")
        self.pack.addItems(pack_names)
        self.pack.blockSignals(False)

        self.flowers_count.clear()
        self.packs_count.clear()
        self.packs_list.clear()
        self.count_list.clear()
        self.count.clear()
        self.work.clear()
        self.name.clear()
        self.total.clear()
        self.cost.clear()

        self.update_count_flowers([])
        self.update_pack_price()

        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()

    def showEvent(self, event):
        """При показе окна обновляем упаковки."""
        super().showEvent(event)

        if not hasattr(self, "pack"):
            return

        self.PACK_PRICES = db.get_packs()

        current = self.pack.currentText()
        self.pack.blockSignals(True)
        self.pack.clear()
        pack_names = sorted({name for (name, size) in self.PACK_PRICES})
        self.pack.addItem("Выберите упаковку")
        self.pack.addItem("Без упаковки")
        self.pack.addItems(pack_names)
        idx = self.pack.findText(current)
        self.pack.setCurrentIndex(idx if idx >= 0 else 0)
        self.pack.blockSignals(False)

        self.update_pack_price()

    def calculate(self):
        if not self.flowers_count:
            dialogs.warn(self, "Расчёт", "Добавьте хотя бы один цветок.")
            return

        pack_price = sum(p for _, _, p in self.packs_count)

        work = self.work.text().strip()
        try:
            work = float(work or 0)
        except ValueError:
            dialogs.warn(self, "Расчёт", "Работа — число.")
            return

        cost_flowers = 0
        for f, c in self.flowers_count.items():
            if f not in self.FLOWER_PRICES:
                dialogs.warn(
                    self, "Расчёт",
                    f"Цветок «{f}» больше нет в справочнике.\n"
                    f"Уберите его из списка или добавьте заново."
                )
                return
            cost_flowers += self.FLOWER_PRICES[f] * c

        cost = cost_flowers + pack_price
        total = cost + work

        self.cost.setText(f"{cost:.0f}")
        self.total.setText(f"{total:.0f}")

    def save_bouquet(self):
        name = self.name.text().strip()
        total = self.total.text().strip()

        if not self.flowers_count:
            dialogs.warn(self, "Сохранение", "Добавьте хотя бы один цветок.")
            return
        if not name:
            dialogs.warn(self, "Сохранение", "Введите название букета.")
            return
        if not total:
            dialogs.warn(self, "Сохранение", "Сначала нажмите «Рассчитать».")
            return

        flowers_str = ", ".join(
            f"{f}×{c}" for f, c in self.flowers_count.items()
        )

        # упаковки без скобок, размеры в порядке упаковок
        if self.packs_count:
            pack_name = ", ".join(n for n, s, _ in self.packs_count)
            size = ", ".join(s for n, s, _ in self.packs_count)
        else:
            pack_name = ""
            size = ""

        db.add_bouquet(
            date.today().isoformat(),
            name,
            flowers_str,
            pack_name,
            size,
            self.work.text().strip(),
            total,
            self.cost.text().strip(),
            sold=0,
            count=1,
        )

        db.sync_orders_by_bouquet_name(name)

        dialogs.info(self, "Сохранение", f"Букет «{name}» сохранён.")