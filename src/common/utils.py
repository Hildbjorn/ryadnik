import os
import re
from datetime import datetime

from uuid import uuid4
from django.apps import apps
from django.core.mail import send_mail
import telepot
import pytils as pytils
from PIL import Image
from slugify import slugify

from django.conf import settings

# Диапазон лет плюс-минус 100 лет от текущего года
YEARS = [(r, r) for r in range(datetime.now().year -
                               100, datetime.now().year + 101)]

# Диапазон чисел от 1 до 20
PERIOD = [(r, r) for r in range(1, 21)]


class TextUtils:
    """ Утилиты для обработки строк """

    @staticmethod
    def replace_n(value):
        """Заменяет переносы строк тегом <br />"""
        if value is not None and isinstance(value, str):
            return value.replace('\n', '<br />')
        else:
            return value

    @staticmethod
    def format_number(number):
        """
        Форматирует число, добавляя пробелы между каждой тысячной группой цифр.
        """
        return '{:,}'.format(number).replace(',', ' ')

    @staticmethod
    def pluralize_russian(number=None, singular=None, dual=None, plural=None):
        """ Склоняет слова в зависимости от числительного в русском языке. """
        if number is None or number < 0:
            raise ValueError("Число должно быть положительным.")

        if number % 10 == 1 and number % 100 != 11:
            return (number, singular)
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return (number, dual)
        else:
            return (number, plural)

    @staticmethod
    def generate_slug(instance, slug_field_name='slug'):
        """ Создает уникальный slug для объекта модели. """
        transliterated_instance = pytils.translit.translify(str(instance))
        model_name = slugify(instance.__class__.__name__).lower()
        slug = f'{model_name}-{slugify(transliterated_instance)}-{uuid4().hex[:8]}'

        # Проверяем уникальность slug в модели
        try:
            while instance.__class__.objects.filter(**{slug_field_name: slug}).exists():
                slug = f'{model_name}-{slugify(transliterated_instance)}-{uuid4().hex[:8]}'
        except AttributeError:
            raise ValueError(
                "Переданный объект не имеет атрибута 'objects'. Убедитесь, что это модель Django.")
        return slug

    @staticmethod
    def clean_phone(phone_number):
        """ Очиска номера телефона от скобок и пробелов """
        clean_number = phone_number.replace(
            ' ', '').replace('(', '').replace(')', '')
        return clean_number


class FileUtils:
    """ Утилиты для работы с файлами """

    @staticmethod
    def set_correct_file_path(instance, filename):
        """
        Создает путь к файлу, используя имя класса объекта, именную папку (slug, nic_name или id) и каталог.
        
        Аргументы:
        - instance: объект модели, для которого сохраняется файл.
        - filename: имя загружаемого файла.
        
        Возвращает:
        - Строку с путем для сохранения файла.
        """
        # Транслитерация имени файла с использованием pytils.translit
        value = pytils.translit.translify(u"%s" % filename)
        # Разделение имени файла и его расширения
        name, ext = os.path.splitext(value)
        # Удаление недопустимых символов из имени файла и замена их на "_"
        name = re.sub(r"[\W]", "_", name.strip())
        # Создание финального имени файла в нижнем регистре
        file_name = f'{name}{ext}'.lower()
        # Получение имени класса объекта в нижнем регистре
        class_name = instance.__class__.__name__.lower()
        # Получение имени каталога из атрибута класса (если не задан, используется 'files')
        dir_name = getattr(instance.__class__, 'dir_name', 'files').lower()
        # Определение именной папки (именуемого каталога):
        # Если у объекта есть атрибут slug, используется его значение.
        # Если slug отсутствует, но есть nic_name, используется nic_name.
        # Если ни slug, ни nic_name не заданы, используется id объекта.
        # Если id отсутствует (например, объект еще не сохранен в БД), используется "no_id".
        named_folder = (
            getattr(instance, 'slug', None)  # Проверяем наличие slug
            or getattr(instance, 'nic_name', None)  # Если slug отсутствует, проверяем nic_name
            or str(getattr(instance, 'id', 'no_id'))  # Если ни slug, ни nic_name, используем id
        )
        # Удаление недопустимых символов из имени папки и замена их на "_"
        named_folder = re.sub(r"[\W]", "_", named_folder.strip()) if named_folder else 'no_id'
        # Формирование пути для файла: <имя_класса>/<именная_папка>/<каталог>/имя_файла
        path = f'{class_name}/{named_folder}/{dir_name}/'
        file_path = path + file_name
        # Возвращение полного пути к файлу
        return file_path

    @staticmethod
    def resize_and_crop_image(image_path, max_size=(150, 150)):
        img = Image.open(image_path)
        width, height = img.size
        # Определите, какая сторона изображения меньше
        if width < height:
            # Установите ширину в max_size[0], сохраняя пропорции
            new_width = max_size[0]
            new_height = int((new_width / width) * height)
        else:
            # Установите высоту в max_size[1], сохраняя пропорции
            new_height = max_size[1]
            new_width = int((new_height / height) * width)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        # Обрезка изображения
        left = (new_width - max_size[0]) / 2
        right = (new_width + max_size[0]) / 2
        top = (new_height - max_size[1]) / 2
        bottom = (new_height + max_size[1]) / 2
        img = img.crop((left, top, right, bottom))
        img.save(image_path)

    @staticmethod
    def resize_and_add_transparent_background(image_path, max_size=(150, 150)):
        img = Image.open(image_path)
        width, height = img.size
        # Определите коэффициент масштабирования для большей стороны
        if width > height:
            scale_factor = max_size[0] / width
        else:
            scale_factor = max_size[0] / height
        # Вычисляем новые размеры
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        # Изменяем размер изображения
        img = img.resize((new_width, new_height), Image.LANCZOS)
        # Создаем новое изображение с прозрачным фоном
        new_img = Image.new(
            "RGBA", max_size, (255, 255, 255, 0))  # Прозрачный фон
        # Вычисляем координаты для размещения измененного изображения по центру
        left = (max_size[0] - new_width) // 2
        top = (max_size[1] - new_height) // 2
        # Размещаем измененное изображение на новом фоне
        new_img.paste(img, (left, top))
        # Сохраняем результат
        new_img.save(image_path)

    @staticmethod
    def remove_empty_dirs(path):
        """ Удаляет пустые папки в заданной директории """
        # Проходим по всем подкаталогам в заданном пути
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    # Если директория пуста, удаляем её
                    os.rmdir(dir_path)
                    print(f'Удалена пустая папка: {dir_path}')
                except OSError:
                    # Если не удалось удалить (например, папка не пустая), игнорируем
                    pass


class DateUtils:
    """Класс утилит для обработки дат"""
    @staticmethod
    def get_current_year():
        return datetime.now().year

    @staticmethod
    def get_current_month():
        return datetime.now().month
    
    
    @staticmethod
    def get_period(experience_start):
        """Расчёт периода (в годах)."""
        current_year = DateUtils.get_current_year()
        experience_period = current_year - experience_start
        return experience_period

    @staticmethod
    def format_experience_string(years):
        """Форматирование строки с опытом в соответствии с правилами русского языка."""
        if 11 <= years % 100 <= 14:
            return f"{years} лет"
        else:
            last_digit = years % 10
            if last_digit == 1:
                return f"{years} год"
            elif 2 <= last_digit <= 4:
                return f"{years} года"
            else:
                return f"{years} лет"
    
    @staticmethod
    def calculate_age(birth_date):
        """Расчет возраста на основании фиксированной даты рождения"""
        
        # Получаем текущую дату
        today = datetime.today()
        # Вычисляем возраст
        age = today.year - birth_date.year
        # Учитываем месяц и день, чтобы избежать ошибки при расчете возраста
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        # Формируем строку с правильным окончанием
        if 11 <= age % 100 <= 19:
            age_string = f'{age} лет'
        else:
            last_digit = age % 10
            if last_digit == 1:
                age_string = f'{age} год'
            elif 2 <= last_digit <= 4:
                age_string = f'{age} года'
            else:
                age_string = f'{age} лет'
        return age_string


class Communications:
    """Класс коммуникаций"""

    @staticmethod
    def telegram_to_team(telegram_token=settings.TELEGRAM_TOKEN,
                        users_telegram_id=settings.USERS_TELEGRAM_ID,
                        message=None):
        """Отправка сообщения в Телеграм по списку."""
        # Проверка наличия настроек
        if not telegram_token or not users_telegram_id:
            print("nTelegram команде (настройки не заданы)")
            print("————")
            print(message)
            return

        # Отправка сообщений, если настройки заданы
        telegramBot = telepot.Bot(telegram_token)
        for user_id in users_telegram_id:
            # Проверка на наличие user_id
            if not user_id:
                print(f"Пропущен пустой user_id.")
                continue

            try:
                telegramBot.sendMessage(
                    user_id, message, parse_mode='html'
                )
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


    @staticmethod
    def email_settings_ready():
        """Проверяет, заданы ли необходимые настройки для отправки email."""
        return all([
            settings.EMAIL_HOST,
            settings.EMAIL_PORT,
            settings.EMAIL_HOST_USER,
            settings.EMAIL_HOST_PASSWORD,
            settings.DEFAULT_FROM_EMAIL
        ])

    @staticmethod
    def email_to_user(subject=None, html_message=None, email=None):
        """ Отправка письма пользователю или вывод в консоль, если настройки не указаны """
        if Communications.email_settings_ready():
            # Отправляем письмо, если настройки указаны
            send_mail(subject,
                      html_message,
                      settings.DEFAULT_FROM_EMAIL,
                      [email],
                      html_message=html_message)
        else:
            # Выводим сообщение в консоль, если настройки не указаны
            print("\nНастройки не заданы. Письмо пользователю:")
            print("————")
            print(f"Subject: {subject}")
            print(f"To: {email}")
            print(f"Message: {html_message}")

    @staticmethod
    def email_to_team(subject=None, html_message_to_team=None):
        """Отправка письма всем суперпользователям и пользователям со статусом staff."""
        try:
            Profile = apps.get_model('users', 'Profile')
            users = Profile.objects.filter(is_staff=True)
            recipients = [user.email for user in users if user.email]

            if recipients:
                if Communications.email_settings_ready():
                    send_mail(subject,
                              html_message_to_team,
                              settings.DEFAULT_FROM_EMAIL,
                              recipients,
                              html_message=html_message_to_team)
                else:
                    print("\nНастройки не заданы. Письмо команде:")
                    print("————")
                    print(f"Subject: {subject}")
                    print(f"To: {', '.join(recipients)}")
                    print(f"Message: {html_message_to_team}")
            else:
                print("В команде никого нет.")

        except LookupError:
            print("Модель 'Profile' не найдена.")
            print("В команде никого нет.")
