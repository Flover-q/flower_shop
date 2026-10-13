from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QLineEdit
)
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QSize, QRegExp

from windows import dialogs
import db

#  Клиенты хранятся в БД (flower.db), таблица clients


class ClientsWindow(QMainWindow):
    """Окно «Клиенты»."""

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
        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_search()
        self.create_table()
        self.create_action_buttons()
        self.create_exit_button()
        self.create_minimize_button()

        self.load_clients()

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
        """Заголовок «Флора-учёт» и «Клиенты»."""
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

        self.subtitle = QLabel("Клиенты", self)
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

    #  ПОИСК + ПОЛОСКА ПОД СЛОВОМ + КРУГЛАЯ КНОПКА-ЛУПА
    def create_search(self):
        """Поле поиска, полоска под словом «Поиск:» и круглая кнопка-лупа."""
        self.search_label = QLabel("Поиск:", self)
        self.search_label.setGeometry(535, 210, 200, 60)
        self.search_label.setStyleSheet("""
            QLabel {
                color: #124612;
                font-size: 42px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        # полоска «Поиск:»
        self.search_line = QLabel(self)
        self.search_line.setGeometry(535, 265, 120, 5)
        self.search_line.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        # поле поиска
        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(690, 220, 620, 55)
        self.search_input.setPlaceholderText("Введите имя или телефон...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #BCD5C6;
                color: #1D321C;
                font-size: 26px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
            }
        """)
        #поиск только по лупе
        self.add_shadow(self.search_input)

        # круглая кнопка-лупа
        self.search_btn = QPushButton(self)
        self.search_btn.setGeometry(1335, 220, 55, 55)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border: 1px solid #1D3A1C;
                border-radius: 27px;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
            QPushButton:pressed {
                background-color: #72917F;
            }
        """)
        self.search_btn.setIcon(QIcon("images/lupa.png"))
        self.search_btn.setIconSize(QSize(35, 35))
        self.search_btn.clicked.connect(self.filter_clients)
        self.add_shadow(self.search_btn)

    #  ТАБЛИЦА
    def create_table(self):
        """Таблица клиентов."""
        self.table = QTableWidget(self)
        self.table.setGeometry(484, 315, 960, 450)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Имя", "Телефон", "Предпочтения"]
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #EBF5EB;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 24px;
                border: 2px solid #5D6D5F;
                gridline-color: #5D6D5F;
            }
            QTableWidget::item {
                background-color: #EBF5EB;
                padding: 8px;
                border: 1px solid #5D6D5F;
            }
            QTableWidget::item:selected {
                background-color: #B4D1C0;
                color: #1D321C;
            }
            QHeaderView::section {
                background-color: #B4D1C0;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 28px;
                font-weight: 500;
                border: 1px solid #5D6D5F;
                padding: 10px;
            }
            QHeaderView::section:hover,
            QHeaderView::section:pressed,
            QHeaderView::section:checked {
                background-color: #B4D1C0;
                border: 1px solid #5D6D5F;
            }
            QTableCornerButton::section {
                background-color: #B4D1C0;
                border: 1px solid #5D6D5F;
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)

        self.table.setSortingEnabled(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)

        self.add_shadow(self.table)

    #  КНОПКИ «ДОБАВИТЬ / УДАЛИТЬ»
    def create_action_buttons(self):
        """Кнопки «Добавить клиента» и «Удалить клиента»."""
        self.add_btn = QPushButton("Добавить клиента", self)
        self.add_btn.setGeometry(515, 815, 410, 70)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #B4D1C0;
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
        self.add_shadow(self.add_btn)
        self.add_btn.clicked.connect(self.add_client)

        self.del_btn = QPushButton("Удалить клиента", self)
        self.del_btn.setGeometry(1005, 815, 410, 70)
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
        self.del_btn.clicked.connect(self.delete_client)

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

    #  ЛОГИКА КЛИЕНТОВ
    def load_clients(self):
        """Заполняет таблицу всеми клиентами из БД."""
        self.fill_table(db.get_clients())

    def fill_table(self, data):
        """Заполняет таблицу переданным списком клиентов."""
        self.table.setRowCount(len(data))
        for i, c in enumerate(data):
            values = [c["name"], c["phone"], c["preferences"]]
            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def filter_clients(self):
        """Фильтр по имени или телефону — вызывается только по лупе."""
        text = self.search_input.text().strip().lower()
        clients = db.get_clients()

        if not text:
            self.fill_table(clients)
            return

        filtered = [
            c for c in clients
            if text in c["name"].lower() or text in c["phone"].lower()
        ]
        self.fill_table(filtered)

    def add_client(self):
        """Открывает 3 диалога и добавляет клиента в БД."""
        # имя — только буквы, пробел, дефис, минимум 2 символа
        name_validator = QRegExpValidator(
            QRegExp(r"^[А-Яа-яЁёA-Za-z\s\-]{2,50}$"), self
        )
        name, ok1 = dialogs.get_text(
            self, "Новый клиент", "Имя:",
            validator=name_validator
        )
        if not ok1 or not name.strip():
            return

        # телефон — только цифры, +, -, пробелы, скобки
        phone_validator = QRegExpValidator(
            QRegExp(r"^[0-9+\-\s()]{5,20}$"), self
        )
        phone, ok2 = dialogs.get_text(
            self, "Новый клиент", "Телефон:",
            validator=phone_validator
        )
        if not ok2 or not phone.strip():
            return

        prefs, ok3 = dialogs.get_text(
            self, "Новый клиент", "Предпочтения (через запятую):"
        )
        if not ok3:
            return

        db.add_client(
            name.strip(),
            phone.strip(),
            prefs.strip()
        )
        self.filter_clients()

    def delete_client(self):
        """Удаляет выбранного в таблице клиента из БД (с подтверждением)."""
        row = self.table.currentRow()
        if row < 0:
            dialogs.warn(self, "Клиенты", "Выберите клиента в таблице.")
            return

        name_item = self.table.item(row, 0)
        phone_item = self.table.item(row, 1)
        if name_item is None or phone_item is None:
            return

        name = name_item.text()
        phone = phone_item.text()

        if not dialogs.confirm(
            self, "Удаление",
            f"Удалить клиента «{name}» ({phone})?"
        ):
            return

        db.delete_client(name, phone)
        self.filter_clients()