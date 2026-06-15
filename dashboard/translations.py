TRANSLATIONS = {
    # Common
    'welcome': {'ru': 'Добро пожаловать!'},
    'new_year_gifts': {'ru': 'Жаркое лето с Mariyam Cosmetics'},
    'language': {'ru': 'Русский'},

    # Admin Login
    'admin_panel': {'ru': 'Панель администратора'},
    'admin_login': {'ru': 'Панель администратора - вход'},
    'login': {'ru': 'Логин'},
    'password': {'ru': 'Пароль'},
    'enter_login': {'ru': 'Введите логин'},
    'enter_password': {'ru': 'Введите пароль'},
    'enter': {'ru': 'Войти'},
    'new_year_system': {'ru': 'Система летней акции Mariyam Cosmetics'},

    # Dashboard
    'management_panel': {'ru': 'Панель управления'},
    'logout': {'ru': 'Выйти'},
    'total_gifts': {'ru': 'Всего подарков'},
    'available_gifts': {'ru': 'Подарков в наличии'},
    'all_orders': {'ru': 'Все заказы'},
    'qr_codes': {'ru': 'QR-коды'},

    # Add Gift Section
    'add_new_gift': {'ru': 'Добавить новый подарок'},
    'gift_name': {'ru': 'Название подарка'},
    'example_iphone': {'ru': 'Например: Набор косметики'},
    'order_number_limit': {'ru': 'Номер заказа (лимит)'},
    'add': {'ru': 'Добавить'},

    # Gifts List
    'gifts_list': {'ru': 'Список подарков'},
    'name': {'ru': 'Название'},
    'price': {'ru': 'Цена'},
    'count': {'ru': 'Количество'},
    'sum': {'ru': 'сум'},
    'order_number': {'ru': 'Номер заказа'},
    'status': {'ru': 'Статус'},
    'actions': {'ru': 'Действия'},
    'available': {'ru': 'Доступен'},
    'given': {'ru': 'Выдан'},
    'cancel': {'ru': 'Отмена'},
    'restore': {'ru': 'Вернуть'},
    'delete': {'ru': 'Удалить'},
    'are_you_sure': {'ru': 'Вы уверены?'},
    'no_gifts_yet': {'ru': 'Подарков пока нет. Добавьте новый подарок выше!'},

    # Recent Orders
    'recent_orders': {'ru': 'Последние заказы'},
    'customer_name': {'ru': 'Имя клиента'},
    'phone': {'ru': 'Телефон'},
    'gift': {'ru': 'Подарок'},
    'date': {'ru': 'Дата'},
    'no_orders_yet': {'ru': 'Заказов пока нет'},
    'new': {'ru': 'Новый'},

    # QR Codes Section
    'generate_qr': {'ru': 'Создать QR-коды'},
    'how_many_qr': {'ru': 'Сколько QR-кодов создать?'},
    'generate': {'ru': 'Создать QR-коды'},
    'available_qr_codes': {'ru': 'Доступные QR-коды'},
    'qr_code': {'ru': 'QR-код'},
    'token': {'ru': 'Токен'},
    'link': {'ru': 'Ссылка'},
    'no_image': {'ru': 'Нет изображения'},
    'used': {'ru': 'Использован'},
    'download': {'ru': 'Скачать'},
    'no_qr_yet': {'ru': 'QR-кодов пока нет. Создайте их выше!'},

    # Gift Reveal
    'new_year_gift': {'ru': 'Летний подарок'},
    'click_to_open': {'ru': 'Нажмите, чтобы открыть подарок!'},
    'happy_new_year': {'ru': 'Жаркое лето с Mariyam Cosmetics'},
    'your_name': {'ru': 'Ваше имя'},
    'your_phone': {'ru': 'Ваш номер телефона'},
    'claim_gift': {'ru': 'Получить подарок!'},

    # Success Page
    'success': {'ru': 'Готово!'},
    'congratulations': {'ru': 'Поздравляем!'},
    'order_id': {'ru': 'Номер заказа:'},
    'name_label': {'ru': 'Имя:'},
    'phone_label': {'ru': 'Телефон:'},
    'note': {'ru': 'Важно:'},
    'will_contact': {'ru': 'Мы скоро свяжемся с вами, чтобы вы могли получить подарок!'},

    # Error Pages
    'unfortunately': {'ru': 'К сожалению!'},
    'qr_used': {'ru': 'QR-код уже использован'},
    'sorry': {'ru': 'Извините!'},
    'gifts_finished': {'ru': 'Подарки закончились'},
    'try_later': {'ru': 'Попробуйте позже.'},

    # Home Page
    'scan_qr_instruction': {
        'ru': 'В знак благодарности нашим покупателям Mariyam Cosmetics запускает летнюю акцию с подарками!'
    },
    'how_it_works': {'ru': 'Как это работает?'},
    'step1': {'ru': 'Отсканируйте QR-код'},
    'step2': {'ru': 'Откройте свой подарок'},
    'step3': {'ru': 'Оставьте данные'},
    'step4': {'ru': 'Получите подарок!'},
}


def get_translation(key, language='ru'):
    """Get translation for a specific key and language."""
    return TRANSLATIONS.get(key, {}).get(language, key)


def get_all_translations(language='ru'):
    """Get all translations for a specific language."""
    return {key: value.get(language, key) for key, value in TRANSLATIONS.items()}
