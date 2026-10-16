from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QLineEdit, QRadioButton, QMenu, QWidgetAction,
    QListWidget
)
from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtCore import Qt, QPoint

from datetime import date
from windows import dialogs
import db


class FlowerDropdown(QPushButton):
    """Кнопка с выпадающим списком цветов (светлый, с ползунком)."""

    def __init__(self, flowers, parent=None):
        super().__init__(parent)
        self.flowers = list(flowers)
        self.selected = "Выберите цветок"

        self.setText(self.selected)
        self.setStyleSheet("""
            QPushButton {
                background-color: #90B29E;
                color: #000000;
                font-weight: 500;
                border-radius: 20px;
                font-size: 28px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 14px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #72917F;
            }
        """)

        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #F0F6F3;
                border: 1px solid #1D3A1C;
                padding: 0px;
            }
            QWidget {
                background-color: #F0F6F3;
            }
        """)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #F0F6F3;
                color: #1D321C;
                font-size: 24px;
                font-family: 'Cormorant Infant';
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 16px;
                background-color: #F0F6F3;
            }
            QListWidget::item:hover {
                background-color: #EAF3EB;
            }
            QListWidget::item:selected {
                background-color: #B5DCC5;
                color: #1D321C;
            }
            QScrollBar:vertical {
                background-color: #EAF3EB;
                width: 14px;
                border: none;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #90B29E;
                min-height: 30px;
                border-radius: 7px;
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
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        self.list_widget.addItem("Выберите цветок")
        for name in self.flowers:
            self.list_widget.addItem(name)

        self.list_widget.setFixedHeight(240)
        self.list_widget.setFixedWidth(360)
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        action = QWidgetAction(self.menu)
        action.setDefaultWidget(self.list_widget)
        self.menu.addAction(action)

        self.clicked.connect(self.show_menu_centered)

    def show_menu_centered(self):
        """Перечитывает цветы из БД и показывает меню под кнопкой."""
        # перечитываем цветы — новые появятся сразу
        self.refresh(db.get_flowers().keys())

        self.menu.adjustSize()
        menu_w = self.menu.sizeHint().width()
        btn_w = self.width()
        dx = (btn_w - menu_w) // 2
        pos = self.mapToGlobal(QPoint(dx, self.height()))
        self.menu.popup(pos)

    def on_item_clicked(self, item):
        self.selected = item.text()
        self.setText(self.selected)
        self.menu.close()

    def currentText(self):
        return self.selected

    def setCurrentIndex(self, index):
        """Совместимость с QComboBox — индекс 0 = сброс."""
        if index == 0:
            self.selected = "Выберите цветок"
            self.setText(self.selected)

    def refresh(self, flowers):
        """Перезаполнить список цветов."""
        self.flowers = list(flowers)
        self.list_widget.clear()
        self.list_widget.addItem("Выберите цветок")
        for name in self.flowers:
            self.list_widget.addItem(name)


class SpisaniePage(QWidget):
    """Окно «Списание»."""

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

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_fields()
        self.create_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.bg.lower()

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

        self.subtitle = QLabel("Списание", self)
        self.subtitle.setGeometry(1140, 30, 423, 70)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #1D321C; font-size: 64px;
                font-family: 'Cormorant Infant'; font-weight: 500;
                background: transparent;
            }
        """)

    def create_fields(self):
        # Цветы
        self.label_flowers = QLabel("Цветы:", self)
        self.label_flowers.setGeometry(540, 235, 180, 75)
        self.label_flowers.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 48px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_flowers = QLabel(self)
        self.line_flowers.setGeometry(540, 305, 380, 5)
        self.line_flowers.setStyleSheet(
            "QLabel { background-color: #AFC9B9; }"
        )

        self.flowers = FlowerDropdown(
            db.get_flowers().keys(), self
        )
        self.flowers.setGeometry(930, 250, 405, 55)
        self.add_shadow(self.flowers)

        # Количество
        self.label_count = QLabel("Количество:", self)
        self.label_count.setGeometry(540, 350, 300, 100)
        self.label_count.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 48px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_count = QLabel(self)
        self.line_count.setGeometry(540, 435, 380, 5)
        self.line_count.setStyleSheet(
            "QLabel { background-color: #AFC9B9; }"
        )

        self.count = QLineEdit(self)
        self.count.setGeometry(930, 375, 405, 55)
        self.count.setPlaceholderText("Введите количество")
        self.count.setStyleSheet("""
            QLineEdit {
                background-color: #F0F6F3;
                color: #000000;
                font-weight: 500;
                font-size: 30px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
            }
        """)
        self.count.setValidator(QIntValidator(1, 9999, self))

        # Причина
        self.label_reason = QLabel("Причина:", self)
        self.label_reason.setGeometry(540, 515, 300, 100)
        self.label_reason.setStyleSheet("""
            QLabel {
                color: #124612; font-size: 48px;
                font-family: 'Cormorant Infant'; background: transparent;
            }
        """)

        self.line_reason = QLabel(self)
        self.line_reason.setGeometry(540, 600, 380, 5)
        self.line_reason.setStyleSheet(
            "QLabel { background-color: #AFC9B9; }"
        )

        radio_style = """
            QRadioButton {
                color: #124612; font-size: 36px;
                font-family: 'Comic Relief';
                background: transparent; spacing: 14px;
            }
            QRadioButton::indicator {
                width: 16px; height: 16px;
                border-radius: 13px;
                border: 5px solid #C8E6C9;
                background-color: #C8E6C9;
            }
            QRadioButton::indicator:hover {
                border: 5px solid #AFD2B1;
                background-color: #AFD2B1;
            }
            QRadioButton::indicator:checked {
                background-color: #587966;
                border: 5px solid #C8E6C9;
            }
        """

        self.reason1 = QRadioButton("Увядание", self)
        self.reason1.setGeometry(665, 620, 300, 50)
        self.reason1.setStyleSheet(radio_style)

        self.reason2 = QRadioButton("Бой", self)
        self.reason2.setGeometry(665, 690, 300, 50)
        self.reason2.setStyleSheet(radio_style)

        self.reason3 = QRadioButton("Брак", self)
        self.reason3.setGeometry(665, 760, 300, 50)
        self.reason3.setStyleSheet(radio_style)

        self.reason4 = QRadioButton("Другое", self)
        self.reason4.setGeometry(665, 830, 300, 50)
        self.reason4.setStyleSheet(radio_style)

        self.add_shadow(self.count)

    def create_buttons(self):
        self.button = QPushButton("Списать", self)
        self.button.setGeometry(1150, 640, 275, 75)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 45px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover { background-color: #9BCCAF; }
        """)
        self.add_shadow(self.button)
        self.button.clicked.connect(self.spisat)

        self.report_button = QPushButton("Отчёт", self)
        self.report_button.setGeometry(1150, 780, 275, 75)
        self.report_button.setStyleSheet("""
            QPushButton {
                background-color: #91C5A7;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 45px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover { background-color: #76B18E; }
        """)
        self.add_shadow(self.report_button)
        self.report_button.clicked.connect(self.open_report)

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
            QPushButton:hover { background-color: #AFD2B1; }
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
        super().showEvent(event)
        if hasattr(self, "flowers"):
            self.flowers.refresh(db.get_flowers().keys())

    def spisat(self):
        flower = self.flowers.currentText().strip()
        cnt = self.count.text().strip()

        if flower == "Выберите цветок":
            dialogs.warn(self, "Списание", "Сначала выберите цветок.")
            return

        # защита: цветок мог быть удалён из справочника
        if flower not in db.get_flowers():
            dialogs.warn(
                self, "Списание",
                "Этого цветка больше нет в справочнике.\n"
                "Выберите другой."
            )
            self.flowers.refresh(db.get_flowers().keys())
            self.flowers.setCurrentIndex(0)
            return

        if not cnt.isdigit() or int(cnt) <= 0:
            dialogs.warn(self, "Списание", "Введите количество больше нуля.")
            return

        reason = ""
        for r in (self.reason1, self.reason2, self.reason3, self.reason4):
            if r.isChecked():
                reason = r.text()
                break

        if not reason:
            dialogs.warn(self, "Списание", "Выберите причину.")
            return

        db.add_spisanie(
            date.today().isoformat(),
            flower,
            int(cnt),
            reason,
        )

        dialogs.info(self, "Списание", "Списание сохранено.")

        self.flowers.setCurrentIndex(0)
        self.count.clear()
        for r in (self.reason1, self.reason2, self.reason3, self.reason4):
            r.setAutoExclusive(False)
            r.setChecked(False)
            r.setAutoExclusive(True)

    def open_report(self):
        """Открывает окно «Отчёт»."""
        self.app.go_to("report")
    def showMinimized(self):
        """Свернуть окно приложения."""
        win = self.window()
        if win is not None:
            win.showMinimized() 