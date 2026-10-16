import sys
import os

# рабочая папка = папка, где лежит main.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

import db

from windows.app_window import AppWindow

from windows.pages.main_menu import MainMenuPage
from windows.pages.main_window import MainWindowPage
from windows.pages.bouquet import BouquetPage
from windows.pages.spisanie import SpisaniePage
from windows.pages.report import ReportPage
from windows.pages.calendar import CalendarPage
from windows.pages.clients import ClientsPage
from windows.pages.analytics import AnalyticsPage
from windows.pages.graph import GraphPage
from windows.pages.my_bouquets import BouquetsPage
from windows.pages.flowers_edit import FlowersEditPage


def load_fonts():
    """Загружает все .ttf из папки fonts/ в Qt."""
    folder = "fonts"
    if not os.path.isdir(folder):
        return
    for fname in os.listdir(folder):
        if fname.lower().endswith((".ttf", ".otf")):
            path = os.path.join(folder, fname)
            QFontDatabase.addApplicationFont(path)


def main():
    app = QApplication(sys.argv)

    load_fonts()
    db.init_db()

    window = AppWindow()

    window.add_page("main_menu",    MainMenuPage(window))
    window.add_page("main",         MainWindowPage(window))
    window.add_page("bouquet",      BouquetPage(window))
    window.add_page("spisanie",     SpisaniePage(window))
    window.add_page("report",       ReportPage(window))
    window.add_page("calendar",     CalendarPage(window))
    window.add_page("clients",      ClientsPage(window))
    window.add_page("analytics",    AnalyticsPage(window))
    window.add_page("graph",        GraphPage(window))
    window.add_page("my_bouquets",  BouquetsPage(window))
    window.add_page("flowers_edit", FlowersEditPage(window))

    window.go_to("main_menu")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()