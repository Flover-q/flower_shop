import os
import sys

# Настройка пути: поднимаемся на один уровень вверх из папки docs в корень проекта
sys.path.insert(0, os.path.abspath('..'))

project = 'Флора-учёт'
copyright = '2026, Ламанова А.А.'
author = 'Ламанова А.А.'
release = '1.0'

# Включаем автоматическое чтение docstrings из твоего Python-кода
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'
html_theme = 'alabaster'
html_static_path = ['_static']

