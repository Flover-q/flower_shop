from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QComboBox
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QDateEdit, QSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QDate
from windows.green_calendar import GreenCalendar
import db


class ReportWindow(QMainWindow):
    """Окно «Отчёт по списаниям»."""

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
        self.create_period()
        self.create_period_fields()
        self.create_table()
        self.create_report_button()
        self.create_exit_button()
        self.create_minimize_button()

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
        """Заголовок «Флора-учёт» и «Отчёт по списаниям»."""
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

        self.subtitle = QLabel("Отчёт по списаниям", self)
        self.subtitle.setGeometry(1040, 25, 600, 80)
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

    #  ПЕРИОД (День / Неделя / Год)
    def create_period(self):
        """Выбор периода: день, неделя, год."""
        self.label_period = QLabel("Период:", self)
        self.label_period.setGeometry(520, 170, 300, 80)
        self.label_period.setStyleSheet("""
            QLabel {
                color: #124612;
                font-size: 42px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line_period = QLabel(self)
        self.line_period.setGeometry(520, 235, 380, 5)
        self.line_period.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.period = QComboBox(self)
        self.period.setGeometry(910, 185, 405, 55)
        self.period.setStyleSheet("""
            QComboBox {
                background-color: #B4D1C0;
                color: #000000;
                font-weight: 500;
                border-radius: 20px;
                font-size: 30px;
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
        """)
        self.period.addItems(["День", "Неделя", "Год"])
        self.period.currentIndexChanged.connect(self.update_period_fields)

        self.add_shadow(self.period)

    #  ПОЛЯ ДАТ
    def create_period_fields(self):
        """Поля даты / диапазона / года."""
        date_style = """
            QDateEdit {
                background-color: #EBF5EB;
                color: #000000;
                font-weight: 500;
                font-size: 28px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 50px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 50px;
                border: none;
                background: transparent;
            }
            QDateEdit::down-arrow {
                image: url(images/vniz.png);
                width: 40px;
                height: 40px;
            }
        """

        # День
        self.label_date = QLabel("Дата:", self)
        self.label_date.setGeometry(520, 260, 300, 80)
        self.label_date.setStyleSheet("""
            QLabel {
                color: #124612;
                font-size: 42px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line_date = QLabel(self)
        self.line_date.setGeometry(520, 325, 380, 5)
        self.line_date.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.date_edit = QDateEdit(self)
        self.date_edit.setGeometry(910, 275, 405, 55)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setCalendarWidget(GreenCalendar())
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setStyleSheet(date_style)
        self.add_shadow(self.date_edit)

        # Неделя
        self.label_from = QLabel("С:", self)
        self.label_from.setGeometry(520, 260, 80, 80)
        self.label_from.setStyleSheet(self.label_date.styleSheet())

        self.date_from = QDateEdit(self)
        self.date_from.setGeometry(610, 275, 300, 55)
        self.date_from.setCalendarPopup(True)
        self.date_from.setCalendarWidget(GreenCalendar())
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setDisplayFormat("dd.MM.yyyy")
        self.date_from.setStyleSheet(date_style)
        self.date_from.dateChanged.connect(self.update_week_to)
        self.add_shadow(self.date_from)

        self.label_to = QLabel("По:", self)
        self.label_to.setGeometry(930, 260, 100, 80)
        self.label_to.setStyleSheet(self.label_date.styleSheet())

        self.date_to = QDateEdit(self)
        self.date_to.setGeometry(1040, 275, 275, 55)
        self.date_to.setCalendarPopup(True)
        self.date_to.setCalendarWidget(GreenCalendar())
        self.date_to.setDate(QDate.currentDate().addDays(6))
        self.date_to.setDisplayFormat("dd.MM.yyyy")
        self.date_to.setStyleSheet(date_style)
        self.date_to.setReadOnly(True)
        self.add_shadow(self.date_to)

        # Год
        self.label_year = QLabel("Год:", self)
        self.label_year.setGeometry(520, 260, 300, 80)
        self.label_year.setStyleSheet(self.label_date.styleSheet())

        self.year_edit = QSpinBox(self)
        self.year_edit.setGeometry(910, 275, 405, 55)
        self.year_edit.setRange(2000, 2100)
        self.year_edit.setValue(QDate.currentDate().year())
        self.year_edit.setStyleSheet("""
            QSpinBox {
                background-color: #EBF5EB;
                color: #000000;
                font-weight: 500;
                font-size: 28px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
                padding-left: 10px;
                padding-right: 40px;
                selection-background-color: #EBF5EB;
                selection-color: #000000;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 40px;
                border: none;
                background: transparent;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 40px;
                border: none;
                background: transparent;
            }
            QSpinBox::up-arrow {
                image: url(images/naverx.png);
                width: 25px;
                height: 25px;
            }
            QSpinBox::down-arrow {
                image: url(images/vniz.png);
                width: 25px;
                height: 25px;
            }
        """)
        self.add_shadow(self.year_edit)

        # По умолчанию показываем «День»
        self.update_period_fields(0)
        # Сразу выравниваем «По» = «С» + 6
        self.update_week_to()

    def update_period_fields(self, index):
        """Показывает нужные поля в зависимости от периода."""
        for w in (self.label_date, self.line_date, self.date_edit,
                  self.label_from, self.date_from,
                  self.label_to, self.date_to,
                  self.label_year, self.year_edit):
            w.hide()

        if index == 0:      # День
            self.label_date.show()
            self.line_date.show()
            self.date_edit.show()
        elif index == 1:    # Неделя
            self.label_from.show()
            self.date_from.show()
            self.label_to.show()
            self.date_to.show()
        elif index == 2:    # Год
            self.label_year.show()
            self.year_edit.show()

    def update_week_to(self):
        """Автоматически ставит «По» = «С» + 6 дней (ровно неделя)."""
        if not hasattr(self, "date_to"):
            return
        start = self.date_from.date()
        self.date_to.setDate(start.addDays(6))

    #  ТАБЛИЦА
    def create_table(self):
        """Таблица для вывода отчёта."""
        self.table = QTableWidget(self)
        self.table.setGeometry(420, 370, 1080, 460)

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Цветок", "Количество", "Причина", "Убыток, ₽"]
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #EBF5EB;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 24px;
                border: 1px solid #1D3A1C;
                gridline-color: #AFC9B9;
            }
            QHeaderView::section {
                background-color: #B4D1C0;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 26px;
                font-weight: 500;
                border: 1px solid #1D3A1C;
                padding: 6px;
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
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)

        self.add_shadow(self.table)

    #  КНОПКА «СФОРМИРОВАТЬ»
    def create_report_button(self):
        """Кнопка «Сформировать»"""
        self.report_button = QPushButton("Сформировать", self)
        self.report_button.setGeometry(1180, 860, 320, 70)
        self.report_button.setStyleSheet("""
            QPushButton {
                background-color: #91C5A7;
                color: #1D693C;
                font-weight: 400;
                border-radius: 25px;
                font-size: 38px;
                font-family: 'Cormorant Infant';
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #76B18E;
            }
        """)
        self.add_shadow(self.report_button)
        self.report_button.clicked.connect(self.load_data)

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
                font-weight: 300;
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

    #  ЛОГИКА — только по кнопке
    def load_data(self):
        """Загрузка отчёта из БД по выбранному периоду."""
        if not hasattr(self, "table"):
            return

        period = self.period.currentText()

        if period == "День":
            d = self.date_edit.date()
            date_from = d.toString("yyyy-MM-dd")
            date_to = date_from
        elif period == "Неделя":
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().toString("yyyy-MM-dd")
        else:  # Год
            y = str(self.year_edit.value())
            date_from = f"{y}-01-01"
            date_to = f"{y}-12-31"

        rows = db.get_spisaniya(date_from, date_to)

        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            values = [
                r["date"],
                r["flower"],
                r["count"],
                r["reason"],
                f"{r['loss']} ₽",
            ]
            for j, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)