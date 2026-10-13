import os
import sys

# Указываем путь к плагинам PyQt5 ТОЛЬКО для Windows
if sys.platform == "win32":
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(sys.executable),
        'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins', 'platforms'
    )

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
from windows.main_menu import MainMenu
from windows.main_window import MainWindow
from db import init_db

app = QApplication(sys.argv)

# ─── иконка приложения (для таскбара Linux) ───
app.setWindowIcon(QIcon("images/flower.ico"))

# создаём таблицы в БД, если их ещё нет
init_db()

# отключаем системный стиль Breeze (KDE) — теперь Qt слушает QSS
app.setStyle("Fusion")

# убираем фиолетовый — ставим свои цвета для выделения
palette = app.palette()
palette.setColor(QPalette.Highlight, QColor("#C8E0C8"))
palette.setColor(QPalette.HighlightedText, QColor("#1D321C"))
app.setPalette(palette)

# глобальный стиль — таблицы, кнопки, системные окна
app.setStyleSheet("""
    QTableWidget {
        background-color: #E0EFE0;
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
        padding: 8px;
    }
    QHeaderView::section:hover,
    QHeaderView::section:pressed,
    QHeaderView::section:checked {
        background-color: #B4D1C0;
        border: 1px solid #1D3A1C;
    }
    QTableWidget::item:selected {
        background-color: #C8E0C8;
        color: #1D321C;
    }

    QMessageBox {
        background-color: #F5FAF5;
        border: 1px solid #1D3A1C;
        border-radius: 20px;
    }
    QMessageBox QLabel {
        color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 28px;
        background: transparent;
    }
    QMessageBox QPushButton {
        background-color: #B5DCC5;
        color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 28px;
        border-radius: 20px;
        border: 1px solid #1D3A1C;
        min-width: 160px;
        min-height: 60px;
        padding: 4px 20px;
    }
    QMessageBox QPushButton:hover {
        background-color: #9BCCAF;
    }

    QInputDialog {
        background-color: #F5FAF5;
        border: 1px solid #1D3A1C;
        border-radius: 20px;
    }
    QInputDialog QLabel {
        color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 26px;
        background: transparent;
    }
    QInputDialog QLineEdit,
    QInputDialog QComboBox {
        background-color: #EBF5EB;
        color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 26px;
        border: 1px solid #1D3A1C;
        padding: 6px;
    }
    QInputDialog QPushButton {
        background-color: #B5DCC5;
        color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 26px;
        border-radius: 20px;
        border: 1px solid #1D3A1C;
        min-width: 120px;
        min-height: 50px;
    }
    QInputDialog QPushButton:hover {
        background-color: #9BCCAF;
    }

    QComboBox QAbstractItemView {
        background-color: #F0F6F3;
        color: #1D321C;
        selection-background-color: #B5DCC5;
        selection-color: #1D321C;
        font-family: 'Cormorant Infant';
        font-size: 24px;
        border: 1px solid #1D3A1C;
        outline: none;
    }

    QComboBox QAbstractItemView QScrollBar:vertical {
        background-color: #EAF3EB;
        width: 14px;
        border: none;
        margin: 0px;
    }
    QComboBox QAbstractItemView QScrollBar::handle:vertical {
        background-color: #90B29E;
        min-height: 30px;
        border-radius: 7px;
    }
    QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
        background-color: #72917F;
    }
    QComboBox QAbstractItemView QScrollBar::add-line:vertical,
    QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
        height: 0px;
        border: none;
        background: transparent;
    }
    QComboBox QAbstractItemView QScrollBar::add-page:vertical,
    QComboBox QAbstractItemView QScrollBar::sub-page:vertical {
        background: transparent;
    }

    QScrollBar:vertical {
        background-color: #EAF3EB;
        width: 14px;
        border: none;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #90B29E;
        min-height: 40px;
        border-radius: 7px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #72917F;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        width: 0px;
        height: 0px;
        background: transparent;
        border: none;
    }
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: transparent;
    }
    QScrollBar:horizontal {
        background-color: #EAF3EB;
        height: 14px;
        border: none;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background-color: #90B29E;
        min-width: 40px;
        border-radius: 7px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #72917F;
    }
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0px;
        height: 0px;
        background: transparent;
        border: none;
    }
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: transparent;
    }
""")

# Загрузка шрифтов из папки проекта
QFontDatabase.addApplicationFont("fonts/CormorantInfant.ttf")
QFontDatabase.addApplicationFont("fonts/Pattaya-Regular.ttf")
QFontDatabase.addApplicationFont("fonts/Ysabeau.ttf")
QFontDatabase.addApplicationFont("fonts/ComicRelief.ttf")
QFontDatabase.addApplicationFont("fonts/ComicRelief-Bold.ttf")

# прячем системный «занято»-курсор на время построения окон
app.setOverrideCursor(Qt.ArrowCursor)

window = MainMenu()
window.show()
app.processEvents()

# предсоздаём главное окно в фоне — чтобы клик был мгновенным
window.main_window = MainWindow()
window.main_window.hide()
app.processEvents()

app.restoreOverrideCursor()

sys.exit(app.exec_())