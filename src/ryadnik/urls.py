"""
Настройки маршрутов проекта
Copyright (c) 2025 Artem Fomin
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import PasswordResetView

from django.conf import settings
from .views import *


urlpatterns = [
    # маршрут для административной панели Django
    path('admin/', admin.site.urls),
    # маршрут для главной страницы
    path('', include('home.urls')),
    # маршрут для документов
    path('documents/<str:filename>', serve_documents, name='serve_documents'),
    # маршрут для учетной записи пользователя
    path('account/', include('users.urls')),
    # маршрут для задач
    path('tasks/', include('tasks.urls')),
]

# добавление маршрута для медиа файлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# добавление маршрута для медиа файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# добавление маршрутов аутентификации сайта Django (для входа, выхода, управления паролями)
urlpatterns += [
    # маршрут для сброса пароля
    path('accounts/password_reset/',
         PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html'),
         name='password_reset'),
    # маршрут для аутентификации Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# добавление маршрута для django-simple-captcha
urlpatterns += [
    # маршрут для captcha
    path('captcha/', include('captcha.urls')),
]

# обработчик ошибки 404
handler404 = "ryadnik.views.page_not_found_view"

