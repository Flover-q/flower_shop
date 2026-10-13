from PyQt5.QtWidgets import QCalendarWidget, QToolButton
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer


class GreenCalendar(QCalendarWidget):
    """Календарь зелёный"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGridVisible(False)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)

        font = QFont("Cormorant Infant", 16)
        self.setFont(font)

        self.setStyleSheet("""
            QCalendarWidget QWidget {
                background-color: #F0F6F3;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 20px;
                alternate-background-color: #EAF3EB;
            }

            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #B5DCC5;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                min-height: 44px;
            }
            QCalendarWidget QToolButton {
                background-color: transparent;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 22px;
                font-weight: 500;
                border: none;
                padding: 6px 10px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #9BCCAF;
                border-radius: 6px;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #72917F;
            }
            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }
            QCalendarWidget QSpinBox {
                background-color: #F0F6F3;
                color: #1D321C;
                font-family: 'Cormorant Infant';
                font-size: 20px;
                border: 1px solid #1D3A1C;
                border-radius: 6px;
                padding: 2px 6px;
            }

            QCalendarWidget QAbstractItemView {
                background-color: #F0F6F3;
                color: #1D321C;
                selection-background-color: #B5DCC5;
                selection-color: #1D321C;
                outline: none;
                font-family: 'Cormorant Infant';
                font-size: 20px;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #A0B3A4;
            }
        """)

        QTimer.singleShot(0, self._apply_side_arrows)

        fmt_today = QTextCharFormat()
        fmt_today.setBackground(QColor("#D0E2D7"))
        fmt_today.setForeground(QColor("#1D321C"))
        fmt_today.setFontWeight(QFont.Bold)
        self.setDateTextFormat(self.selectedDate(), fmt_today)

        fmt_selected = QTextCharFormat()
        fmt_selected.setBackground(QColor("#B5DCC5"))
        fmt_selected.setForeground(QColor("#1D321C"))
        fmt_selected.setFontWeight(QFont.Bold)
        self.setDateTextFormat(self.selectedDate(), fmt_selected)

        fmt_weekend = QTextCharFormat()
        fmt_weekend.setForeground(QColor("#8A5B5B"))
        for day in (Qt.Saturday, Qt.Sunday):
            self.setWeekdayTextFormat(day, fmt_weekend)

    def _apply_side_arrows(self):
        """Ставит nalevo.png и napravo.png на кнопки prev/next."""
        prev_btn = self.findChild(QToolButton, "qt_calendar_prevmonth")
        next_btn = self.findChild(QToolButton, "qt_calendar_nextmonth")

        if prev_btn is not None:
            prev_btn.setText("")
            prev_btn.setIcon(QIcon("images/nalevo.png"))
            prev_btn.setIconSize(QSize(22, 22))

        if next_btn is not None:
            next_btn.setText("")
            next_btn.setIcon(QIcon("images/napravo.png"))
            next_btn.setIconSize(QSize(22, 22))