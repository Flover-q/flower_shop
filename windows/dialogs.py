from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QGraphicsDropShadowEffect, QWidget
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt


# палитра
BG_DIALOG     = "#F5FAF5"
BG_HEADER     = "#EAF3EB"
BG_INPUT      = "#EBF5EB"
BG_BTN_OK     = "#B5DCC5"
BG_BTN_OK_H   = "#9BCCAF"
BG_BTN_CANCEL = "#C8E6C9"
BG_BTN_CANC_H = "#AFD2B1"
COLOR_TEXT    = "#1D321C"
COLOR_ACCENT  = "#124612"
COLOR_LINE    = "#AFC9B9"
COLOR_SHADOW  = "#D0DDD5"


class _BaseDialog(QDialog):
    """Базовая карточка-диалог в стиле «Флора-учёт»."""

    def __init__(self, parent, title, text, buttons):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("images/flower.ico"))
        self.setModal(True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #внешний контейнер (для тени)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 30, 30, 30)

        card = QWidget(self)
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QWidget#card {{
                background-color: {BG_DIALOG};
                border: 2px solid {COLOR_TEXT};
                border-radius: 25px;
            }}
        """)
        outer.addWidget(card)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setXOffset(18)
        shadow.setYOffset(18)
        shadow.setColor(QColor(COLOR_SHADOW))
        card.setGraphicsEffect(shadow)

        # содержимое карточки
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ▸ шапка
        header = QWidget(card)
        header.setObjectName("header")
        header.setStyleSheet(f"""
            QWidget#header {{
                background-color: {BG_HEADER};
                border-top-left-radius: 23px;
                border-top-right-radius: 23px;
                border-bottom: 2px solid {COLOR_LINE};
            }}
        """)
        header.setFixedHeight(90)

        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(28, 0, 28, 0)

        self.title_label = QLabel(title, header)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_ACCENT};
                font-size: 42px;
                font-family: 'Cormorant Infant';
                font-weight: 500;
                background: transparent;
            }}
        """)
        h_layout.addWidget(self.title_label)

        layout.addWidget(header)

        # ▸ тело
        body = QWidget(card)
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(40, 28, 40, 28)
        body_layout.setSpacing(22)

        if text:
            text_label = QLabel(text, body)
            text_label.setWordWrap(True)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLOR_TEXT};
                    font-size: 30px;
                    font-family: 'Cormorant Infant';
                    background: transparent;
                }}
            """)
            body_layout.addWidget(text_label)

        self.build_content(body_layout)

        # ▸ кнопки
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(18)
        btn_layout.addStretch()

        for btn_text, btn_color, btn_hover, btn_result in buttons:
            btn = QPushButton(btn_text, body)
            btn.setFixedSize(170, 60)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {btn_color};
                    color: {COLOR_TEXT};
                    border-radius: 25px;
                    font-size: 30px;
                    font-family: 'Cormorant Infant';
                    font-weight: 500;
                    border: 1px solid {COLOR_TEXT};
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                }}
                QPushButton:pressed {{
                    background-color: {BG_BTN_OK};
                }}
            """)
            btn.clicked.connect(
                lambda checked=False, r=btn_result: self.finish(r)
            )
            btn_layout.addWidget(btn)

        btn_layout.addStretch()
        body_layout.addLayout(btn_layout)

        layout.addWidget(body)

        self.setMinimumWidth(560)

    def build_content(self, layout):
        pass

    def finish(self, result):
        if result:
            self.accept()
        else:
            self.reject()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.accept()
        elif event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)


class _InfoDialog(_BaseDialog):
    def __init__(self, parent, title, text):
        super().__init__(
            parent, title, text,
            [("ОК", BG_BTN_OK, BG_BTN_OK_H, True)]
        )


class _ConfirmDialog(_BaseDialog):
    def __init__(self, parent, title, text):
        super().__init__(
            parent, title, text,
            [
                ("Да",  BG_BTN_OK,     BG_BTN_OK_H,   True),
                ("Нет", BG_BTN_CANCEL, BG_BTN_CANC_H, False),
            ]
        )


class _GetTextDialog(_BaseDialog):
    def __init__(self, parent, title, label, validator=None):
        self.input = None
        self.validator = validator
        super().__init__(
            parent, title, label,
            [
                ("ОК",     BG_BTN_OK,     BG_BTN_OK_H,   True),
                ("Отмена", BG_BTN_CANCEL, BG_BTN_CANC_H, False),
            ]
        )

    def build_content(self, layout):
        self.input = QLineEdit(self)
        self.input.setFixedHeight(60)
        if self.validator is not None:
            self.input.setValidator(self.validator)
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_INPUT};
                color: {COLOR_TEXT};
                font-size: 28px;
                font-family: 'Cormorant Infant';
                border: 1px solid {COLOR_TEXT};
                border-radius: 15px;
                padding-left: 16px;
                padding-right: 16px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_ACCENT};
            }}
        """)
        layout.addWidget(self.input)
        self.input.setFocus()

    def keyPressEvent(self, event):
        """Enter не подтверждает пустое поле."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.input is not None and self.input.text().strip():
                self.accept()
            return
        if event.key() == Qt.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)


class _GetItemDialog(_BaseDialog):
    def __init__(self, parent, title, label, items, editable=False):
        self.items = items
        self.editable = editable
        self.combo = None
        super().__init__(
            parent, title, label,
            [
                ("ОК",     BG_BTN_OK,     BG_BTN_OK_H,   True),
                ("Отмена", BG_BTN_CANCEL, BG_BTN_CANC_H, False),
            ]
        )

    def build_content(self, layout):
        self.combo = QComboBox(self)
        self.combo.setFixedHeight(60)
        self.combo.addItems(self.items)
        self.combo.setEditable(self.editable)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {BG_INPUT};
                color: {COLOR_TEXT};
                font-size: 28px;
                font-family: 'Cormorant Infant';
                border: 1px solid {COLOR_TEXT};
                border-radius: 15px;
                padding-left: 16px;
            }}
            QComboBox:focus {{
                border: 2px solid {COLOR_ACCENT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 50px;
            }}
            QComboBox::down-arrow {{
                image: url(images/vniz.png);
                width: 32px;
                height: 32px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_DIALOG};
                color: {COLOR_TEXT};
                selection-background-color: {BG_BTN_OK};
                selection-color: {COLOR_TEXT};
                font-size: 26px;
                font-family: 'Cormorant Infant';
                border: 1px solid {COLOR_TEXT};
                outline: none;
            }}
        """)
        layout.addWidget(self.combo)


# публичные функции
def info(parent, title, text):
    dlg = _InfoDialog(parent, title, text)
    dlg.exec_()


def warn(parent, title, text):
    dlg = _InfoDialog(parent, title, text)
    dlg.exec_()


def confirm(parent, title, text):
    dlg = _ConfirmDialog(parent, title, text)
    return dlg.exec_() == QDialog.Accepted


def get_text(parent, title, label, validator=None):
    dlg = _GetTextDialog(parent, title, label, validator)
    if dlg.exec_() == QDialog.Accepted:
        return dlg.input.text(), True
    return "", False


def get_item(parent, title, label, items, current=0, editable=False):
    dlg = _GetItemDialog(parent, title, label, items, editable=editable)
    if dlg.exec_() == QDialog.Accepted:
        return dlg.combo.currentText(), True
    return "", False