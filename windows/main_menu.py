from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt
from windows.main_window import MainWindow


class MainMenu(QMainWindow):
    """Главное меню с кнопкой «Начать работу»."""

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
                background-image: url(images/Fon_1.png);
                background-position: center;
                background-repeat: no-repeat;
            }
        """)

        # здесь будет предзагруженное главное окно
        self.main_window = None

        self.create_title()
        QApplication.processEvents()

        self.create_top_bar()
        self.create_bottom_bar()
        self.create_button()
        QApplication.processEvents()

        self.create_exit_button()
        self.create_minimize_button()
        QApplication.processEvents()

    def create_top_bar(self):
        """Верхняя полоска."""
        self.top_bar = QLabel(self)
        self.top_bar.setGeometry(240, -108, 1440, 139)
        self.top_bar.setStyleSheet("""
            QLabel {
                background-color: #EDF8EE;
            }
        """)
        self.top_bar.lower()

    def create_bottom_bar(self):
        """Нижняя полоска."""
        self.bottom_bar = QLabel(self)
        self.bottom_bar.setGeometry(240, 1050, 1440, 139)
        self.bottom_bar.setStyleSheet("""
            QLabel {
                background-color: #EDF8EE;
            }
        """)
        self.bottom_bar.lower()

    def create_title(self):
        """Создаёт заголовок «Флора-учёт» и подзаголовок."""
        self.title = QLabel("Флора-учёт", self)
        self.title.setGeometry(650, 100, 640, 150)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #1D321C;
                font-size: 96px;
                font-family: 'Pattaya';
                font-weight: 700;
                background: transparent;
            }
        """)

        self.subtitle = QLabel("Помощник флориста: от букета до заказа", self)
        self.subtitle.setGeometry(500, 218, 862, 100)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #4E7655;
                font-size: 48px;
                font-family: 'Cormorant Infant';
                font-weight: 300;
                background: transparent;
            }
        """)

        self.subtitle_line = QLabel(self)
        self.subtitle_line.setGeometry(500, 305, 862, 5)
        self.subtitle_line.setStyleSheet("""
            QLabel {
                background-color: #AFC9B9;
            }
        """)

    def create_button(self):
        """Создаёт кнопку «Начать работу»."""
        self.button = QPushButton("Начать работу", self)
        self.button.setGeometry(700, 650, 509, 121)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #B5DCC5;
                color: #1D693C;
                border-radius: 25px;
                font-size: 64px;
                font-family: 'Ysabeau';
                padding-bottom: 20px;
                font-weight: 300;
                border: 1px solid #1D3A1C;
            }
            QPushButton:hover {
                background-color: #9BCCAF;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(23)
        shadow.setYOffset(23)
        shadow.setColor(QColor("#D0DDD5"))
        self.button.setGraphicsEffect(shadow)

        self.button.clicked.connect(self.open_main_window)

    def create_exit_button(self):
        """Создаёт кнопку «Выход»."""
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

        self.exit_button.clicked.connect(self.close)

    def create_minimize_button(self):
        """Создаёт кнопку «Свернуть»."""
        self.min_button = QPushButton("—", self)
        self.min_button.setGeometry(1590, 50, 50, 50)
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

    def open_main_window(self):
        """Открывает главное окно с карточками."""
        QApplication.setOverrideCursor(Qt.ArrowCursor)

        if self.main_window is None:
            self.main_window = MainWindow()
            self.main_window.main_menu = self

        self.main_window.show()
        QApplication.processEvents()

        QApplication.restoreOverrideCursor()

        self.hide()