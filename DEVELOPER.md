# Руководство разработчика «Флора-учёт»

Документ для разработчиков.

## Архитектура

- UI — windows/pages/
- Общее окно — windows/app_window.py
- Бизнес-логика — db.py
- БД — flower.db

Паттерн: MVC.

## Структура проекта

flower_shop/
├── main.py
├── db.py
├── flower.db
├── README.md
├── DEVELOPER.md
├── fonts/
├── images/
├── tests/
│   └── test_db.py
└── windows/
    ├── app_window.py
    ├── dialogs.py
    ├── green_calendar.py
    └── pages/
        ├── main_menu.py
        ├── main_window.py
        ├── bouquet.py
        ├── spisanie.py
        ├── report.py
        ├── calendar.py
        ├── clients.py
        ├── analytics.py
        ├── graph.py
        ├── my_bouquets.py
        └── flowers_edit.py

## Установка

git clone <ссылка>
cd flower_shop
python3 -m venv venv
source venv/bin/activate
pip install PyQt5 pyphen pytest pyinstaller
python main.py

## Тестирование

python3 -m pytest tests/ -v

## Сборка

Windows:
pyinstaller --noconfirm --windowed --add-data "images;images" --add-data "fonts;fonts" --add-data "flower.db;." --name "Flora" main.py

Linux:
python3 -m PyInstaller --noconfirm --windowed --add-data "images:images" --add-data "fonts:fonts" --add-data "flower.db:." --name "Flora" main.py

## Работа с БД

Все запросы через db.py. SQL параметризованный.

## Git

- main — стабильная ветка
- feature/имя — новая функция
- PR перед merge

## Автор

Ламанова А.А., группа ИСП-34, НЭК, 2026 г.
