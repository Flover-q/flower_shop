from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class AppWindow(QMainWindow):
    """Одно окно приложения. Внутри — страницы (по одной на экран)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Флора-учёт")
        self.setWindowIcon(QIcon("images/flower.ico"))

        # без рамки, но не поверх всех — чтобы панель задач выезжала при Win
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("QMainWindow { background-color: #F5FAF5; }")

        self.pages = {}
        self.current_page = None

        # полный экран — панель скрыта, но Win покажет её поверх
        self.showFullScreen()

    def add_page(self, name, widget):
        """Добавляет страницу в окно (но не показывает её)."""
        widget.setParent(self)
        widget.setGeometry(0, 0, 1920, 1080)
        widget.hide()
        self.pages[name] = widget

    def go_to(self, name):
        """Показывает страницу по имени, скрывает остальные."""
        if self.current_page is not None:
            self.current_page.hide()

        page = self.pages.get(name)
        if page is None:
            return

        page.show()
        page.raise_()
        self.current_page = page

    def set_subtitle(self, text):
        """Ничего не делает — оставлен для совместимости."""
        pass