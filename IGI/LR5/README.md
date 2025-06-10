# BookStore

Веб-приложение книжного магазина на Django с функциями управления товарами, заказами и пользователями.

## Функциональность

- Управление пользователями (администраторы, сотрудники, покупатели)
- Каталог товаров с категориями
- Система заказов
- Промо-акции и скидки
- Административная панель для управления всеми аспектами магазина

## Требования

- Python 3.8+
- Django 5.2+
- django-crispy-forms
- Pillow

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd BookStore
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `store/models.py` - модели данных (User, Category, Product, Customer, Order, OrderItem, Promotion)
- `store/admin.py` - настройки административной панели
- `static/` - статические файлы (CSS, JavaScript, изображения)
- `media/` - загружаемые пользователями файлы
- `templates/` - шаблоны HTML

## Лицензия

MIT 
