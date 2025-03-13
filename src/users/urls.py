from django.urls import path
from .views import *

# Регистрация и активация пользователя
urlpatterns = [
    # Путь для регистрации пользователя
    path('signup/', SignUpView.as_view(), name='profile_signup'),
    # Путь для модального окна регистрации пользователя
    path('signup-modal/', SignupModalView.as_view(), name='profile_signup_modal'),
    # Путь для подтверждения электронной почты
    path('email-confirm-done/', email_confirm_done, name='email_confirm_done'),
    # Путь для активации профиля пользователя
    path('profile-activate/<uidb64>/<token>/', profile_activate, name='profile_activate'),
]

# Вход и выход пользователя
urlpatterns += [
    # Путь для входа пользователя
    path('login/', CustomLoginView.as_view(), name='profile_login'),
    # Путь для модального окна входа пользователя
    path('login-modal/', LoginModalView.as_view(), name='profile_login_modal'),
    # Путь для выхода пользователя
    path('profile-logout/', CustomLogoutView.as_view(), name='profile_logout'),
]

# Удаление учетных записей пользователей
urlpatterns += [
    # Путь для подтверждения удаления профиля пользователя
    path('profile-delete_confirmation/', ProfileDeleteConfirmation.as_view(), name='profile_delete_confirmation'),
    # Путь для отображения страницы с запретом удаления суперпользователя
    path('superuser-delete_denied/', SuperuserDeleteDenied.as_view(), name='superuser_delete_denied'),
    # Путь для удаления профиля пользователя
    path('profile-delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    # Путь для удаления всех неактивных профилей пользователей
    path('delete-inactive_profiles/', DeleteAllInactiveUsersView.as_view(), name='delete_inactive_profiles'),
]

# Профиль пользователя
urlpatterns += [
    # Путь для обновления профиля пользователя
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]

# Все пользователи
urlpatterns += [
    # Путь для отображения всех пользователей
    path('all-users/', AllUsersView.as_view(), name='all_users'),
]
