from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from windows.bouquet import BouquetWindow
from windows.spisanie import SpisanieWindow
from windows.calendar import CalendarWindow
from windows.clients import ClientsWindow
from windows.analytics import AnalyticsWindow
from windows.my_bouquets import BouquetsWindow
from windows.flowers_edit import FlowersEditWindow
from windows import dialogs
import db


class MainWindow(QMainWindow):
    """Главное окно с карточками."""

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

        # кэш окон
        self.bouquet = None
        self.spisanie = None
        self.calendar = None
        self.clients = None
        self.analytics = None
        self.bouquets = None
        self.flowers_edit = None

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_side_bars()
        self.create_title()
        self.create_edit_button()
        self.create_card1()
        self.create_card2()
        self.create_card3()
        self.create_card4()
        self.create_card5()
        self.create_card6()
        self.create_exit_button()
        self.create_minimize_button()

        # фоновая предзагрузка «тяжёлого» окна «Собрать букет»
        QTimer.singleShot(500, self.preload_all)

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

        self.line5 = QLabel(self)
        self.line5.setGeometry(240, 135, 1440, 5)
        self.line5.setStyleSheet("""
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
        """Заголовок и подсказка."""
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

        self.hint = QLabel("Выберите, что хотите сделать:", self)
        self.hint.setGeometry(585, 195, 703, 77)
        self.hint.setAlignment(Qt.AlignCenter)
        self.hint.setStyleSheet("""
            QLabel {
                color: #124612;
                font-size: 48px;
                font-family: 'Cormorant Infant';
                font-weight: 300;
                background: transparent;
            }
        """)

        self.hint_line = QLabel(self)
        self.hint_line.setGeometry(585, 272, 703, 5)
        self.hint_line.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

    def create_edit_button(self):
        """Маленькая кнопка-шестерёнка слева вверху."""
        self.edit_btn = QPushButton("⚙", self)
        self.edit_btn.setGeometry(250, 45, 50, 50)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #C8E6C9;
                color: #4A7C59;
                border-radius: 10px;
                font-size: 26px;
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
        self.edit_btn.setGraphicsEffect(shadow)

        self.edit_btn.clicked.connect(self.open_edit)

    def create_card1(self):
        """Карточка «Собрать букет»."""
        self.card1 = QPushButton(self)
        self.card1.setGeometry(470, 385, 180, 170)
        self.card1.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card1.setIcon(QIcon("images/Kar_1.png"))
        self.card1.setIconSize(QSize(164, 164))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card1.setGraphicsEffect(shadow)

        self.label1 = QLabel("Собрать букет", self)
        self.label1.setGeometry(425, 545, 269, 58)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line1 = QLabel(self)
        self.line1.setGeometry(470, 610, 180, 5)
        self.line1.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card1.clicked.connect(self.open_bouquet)

    def create_card2(self):
        """Карточка «Списание»."""
        self.card2 = QPushButton(self)
        self.card2.setGeometry(1270, 385, 180, 170)
        self.card2.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card2.setIcon(QIcon("images/Kar_2.png"))
        self.card2.setIconSize(QSize(164, 164))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card2.setGraphicsEffect(shadow)

        self.label2 = QLabel("Списание", self)
        self.label2.setGeometry(1265, 550, 188, 47)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line2 = QLabel(self)
        self.line2.setGeometry(1270, 610, 180, 5)
        self.line2.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card2.clicked.connect(self.open_spisanie)

    def create_card3(self):
        """Карточка «Календарь»."""
        self.card3 = QPushButton(self)
        self.card3.setGeometry(1270, 690, 180, 170)
        self.card3.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card3.setIcon(QIcon("images/Kar_3.png"))
        self.card3.setIconSize(QSize(164, 164))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card3.setGraphicsEffect(shadow)

        self.label3 = QLabel("Календарь", self)
        self.label3.setGeometry(1260, 850, 203, 58)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line3 = QLabel(self)
        self.line3.setGeometry(1270, 910, 180, 5)
        self.line3.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card3.clicked.connect(self.open_calendar)

    def create_card4(self):
        """Карточка «Клиенты»."""
        self.card4 = QPushButton(self)
        self.card4.setGeometry(470, 690, 180, 170)
        self.card4.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card4.setIcon(QIcon("images/Kar_4.png"))
        self.card4.setIconSize(QSize(164, 164))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card4.setGraphicsEffect(shadow)

        self.label4 = QLabel("Клиенты", self)
        self.label4.setGeometry(470, 855, 190, 46)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line4 = QLabel(self)
        self.line4.setGeometry(480, 910, 180, 5)
        self.line4.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card4.clicked.connect(self.open_clients)

    def create_card5(self):
        """Карточка «Аналитика»."""
        self.card5 = QPushButton(self)
        self.card5.setGeometry(870, 690, 180, 170)
        self.card5.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card5.setIcon(QIcon("images/Kar_5.png"))
        self.card5.setIconSize(QSize(164, 164))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card5.setGraphicsEffect(shadow)

        self.label5 = QLabel("Аналитика", self)
        self.label5.setGeometry(835, 845, 255, 69)
        self.label5.setAlignment(Qt.AlignCenter)
        self.label5.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line5 = QLabel(self)
        self.line5.setGeometry(870, 910, 180, 5)
        self.line5.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card5.clicked.connect(self.open_analytics)

    def create_card6(self):
        """Карточка «Мои букеты»."""
        self.card6 = QPushButton(self)
        self.card6.setGeometry(870, 385, 180, 170)
        self.card6.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                border-radius: 25px;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)
        self.card6.setIcon(QIcon("images/Kar_6.png"))
        self.card6.setIconSize(QSize(174, 174))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(20)
        shadow.setYOffset(-20)
        shadow.setColor(QColor("#D0DDD5"))
        self.card6.setGraphicsEffect(shadow)

        self.label6 = QLabel("Мои букеты", self)
        self.label6.setGeometry(830, 550, 260, 46)
        self.label6.setAlignment(Qt.AlignCenter)
        self.label6.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 40px;
                font-family: 'Cormorant Infant';
                background: transparent;
            }
        """)

        self.line6 = QLabel(self)
        self.line6.setGeometry(870, 610, 180, 5)
        self.line6.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

        self.card6.clicked.connect(self.open_bouquets)

    def create_exit_button(self):
        """Кнопка «Выход»."""
        self.exit_button = QPushButton("Выход", self)
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

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(15)
        shadow.setYOffset(15)
        shadow.setColor(QColor("#D0DDD5"))
        self.exit_button.setGraphicsEffect(shadow)

        self.exit_button.clicked.connect(self.close_app)

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

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(8)
        shadow.setYOffset(8)
        shadow.setColor(QColor("#D0DDD5"))
        self.min_button.setGraphicsEffect(shadow)

        self.min_button.clicked.connect(self.showMinimized)

    def preload_all(self):
        """Тихо создаёт окно «Собрать букет» в фоне."""
        if self.bouquet is None:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.bouquet = BouquetWindow()
            self.bouquet.hide()
            QApplication.restoreOverrideCursor()

    def open_edit(self):
        """Открывает окно редактирования справочников."""
        QApplication.setOverrideCursor(Qt.ArrowCursor)

        choice, ok = dialogs.get_item(
            self, "Справочник",
            "Что редактировать:",
            ["Цветы", "Упаковки"]
        )

        QApplication.restoreOverrideCursor()

        if not ok:
            return

        if choice == "Цветы":
            tab = "flowers"
        else:
            tab = "packs"

        self.flowers_edit = FlowersEditWindow(start_tab=tab)
        self.flowers_edit.show()
        self.flowers_edit.raise_()
        self.flowers_edit.activateWindow()

    def open_bouquet(self):
        """Открывает окно «Собрать букет»."""
        if self.bouquet is None:
            self.bouquet = BouquetWindow()
        else:
            self.bouquet.reset()
        self.bouquet.show()
        self.bouquet.raise_()
        self.bouquet.activateWindow()

    def open_spisanie(self):
        """Открывает окно «Списание»."""
        if self.spisanie is None:
            self.spisanie = SpisanieWindow()
        self.spisanie.show()
        self.spisanie.raise_()
        self.spisanie.activateWindow()

    def open_calendar(self):
        """Открывает окно «Календарь»."""
        if self.calendar is None:
            self.calendar = CalendarWindow()
        self.calendar.show()
        self.calendar.raise_()
        self.calendar.activateWindow()

    def open_clients(self):
        """Открывает окно «Клиенты»."""
        if self.clients is None:
            self.clients = ClientsWindow()
        self.clients.show()
        self.clients.raise_()
        self.clients.activateWindow()

    def open_analytics(self):
        """Открывает окно «Аналитика»."""
        if self.analytics is None:
            self.analytics = AnalyticsWindow()
        self.analytics.show()
        self.analytics.raise_()
        self.analytics.activateWindow()

    def open_bouquets(self):
        """Открывает окно «Мои букеты»."""
        if self.bouquets is None:
            self.bouquets = BouquetsWindow()
        else:
            self.bouquets.load_bouquets()
        self.bouquets.show()
        self.bouquets.raise_()
        self.bouquets.activateWindow()

    def closeEvent(self, event):
        """При закрытии главного окна возвращаем меню."""
        if getattr(self, "main_menu", None) is not None:
            self.main_menu.show()
        super().closeEvent(event)

    def close_app(self):
        """Закрывает всю программу."""
        QApplication.quit()