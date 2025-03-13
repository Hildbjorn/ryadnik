from common.utils import Communications
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from users.forms import ProfileCreationForm, ProfileUpdateForm
from users.models import Profile
from users.token import account_activation_token

__all__ = (
    'SignUpView',
    'SignupModalView',
    'CustomLoginView',
    'LoginModalView',
    'CustomLogoutView',
    'ProfileUpdateView',
    'ProfileDeleteConfirmation',
    'SuperuserDeleteDenied',
    'ProfileDeleteView',
    'AllUsersView',
    'DeleteAllInactiveUsersView',
    'profile_activate',
    'email_confirm_done'
)


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Класс регистрации нового пользователя
    """
    form_class = ProfileCreationForm
    template_name = 'registration/signup.html'

    # success_message = "Регистрация прошла успешно."

    def get_success_url(self):
        return reverse("email_confirm_done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        email = user.email
        user.save()
        # получаем адрес нашего сайта
        current_site = get_current_site(self.request)
        html_message = loader.render_to_string(
            'users/mail_layouts/email_confirm_mail.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        subject = "Подтверждение E-mail"
        # Отправка письма пользователю с кнопкой подтверждения email
        Communications.email_to_user(subject=subject,
                                     html_message=html_message,
                                     email=email)
        return super().form_valid(form)


class SignupModalView(SuccessMessageMixin, View):
    template_name = "users/components/signup_modal.html"
    success_message = "Регистрация прошла успешно. Проверьте вашу почту."

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос для загрузки формы"""
        form = ProfileCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для сохранения пользователя"""
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = user.email
            user.save()
            messages.success(request, self.success_message)
            # получаем адрес нашего сайта
            current_site = get_current_site(self.request)
            html_message = loader.render_to_string(
                'users/mail_layouts/email_confirm_mail.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            subject = "Подтверждение E-mail"
            # Отправка письма пользователю с кнопкой подтверждения email
            Communications.email_to_user(subject=subject,
                                        html_message=html_message,
                                        email=email)
            # Вернуть сообщение об успешной регистрации
            return render(request, 'users/components/email_confirm_done_modal.html')
        # Вернуть форму с ошибками
        return render(request, self.template_name, {"form": form})


def email_confirm_done(request):
    """
    Функция просмотра страницы об успешной отправке e-mail с подтверждением
    """
    return render(request, 'users/email_confirm_done.html')


def profile_activate(request, uidb64, token):
    """
    Функция активации пользователя после подтверждения e-mail
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        e_mail = user.email
        user_count = Profile.objects.all().count()
        user.save()
        # Отправка сообщения в Telegram
        message = "На сайте " + request.get_host() + " \nзарегистрирован новый пользователь." + "\n" + \
                  "..................................................." + "\n" + "\n" + \
                  "<b>e-mail:</b> " + "\n" + str(e_mail) + "\n" + "\n" + \
                  "..................................................." + "\n" + \
                  "Всего пользователей: " + "<b>" + str(user_count) + "</b>"
        # Отправка сообщение в Telegram
        Communications.telegram_to_team(message=message)
        # **********************************************************************
        return render(request, 'users/email_confirm_complete.html')
    else:
        return render(request, 'users/email_confirm_denied.html')


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Класс обновления данных пользователя
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_message = "Данные успешно обновлены."

    def get_object(self, **kwargs):
        self.user = get_object_or_404(Profile, id=self.request.user.id)
        return self.user

    def get_success_url(self):
        return reverse("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context


class CustomLoginView(LoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and 'logout' in next_url:
            return self.get_redirect_url() or self.get_default_redirect_url()
        return super().get_success_url()


class LoginModalView(SuccessMessageMixin, View):
    """ Класс входа в модальном окне """
    template_name = "users/components/login_modal.html"
    success_message = "Вход в систему выполнен успешно."
    
    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос для загрузки формы"""
        form = AuthenticationForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        """ Обработка POST-запроса для входа в систему """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, self.success_message)
            # Проверяем параметр next
            next_url = request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return JsonResponse({}, headers={"HX-Redirect": next_url})
            # Перенаправление на страницу профиля по умолчанию
            profile_url = reverse_lazy("profile")
            return JsonResponse({}, headers={"HX-Redirect": profile_url})
        else:
            messages.error(request, "Ошибка входа. Проверьте правильность данных.")
        return render(request, self.template_name, {"form": form})
    

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProfileDeleteConfirmation(TemplateView):
    """ Класс подтверждения удаления пользователя """
    
    def get_template_names(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return ['users/components/superuser_delete_denied_modal.html']
        return ['users/components/profile_delete_confirmation.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.pk
        profile = get_object_or_404(Profile, pk=user_id)
        context["profile"] = profile
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            # Получаем профиль пользователя
            user_id = request.user.pk
            profile = get_object_or_404(Profile, pk=user_id)
            # Формируем контекст для шаблона
            context = {'profile': profile}
            # Получаем имя шаблона
            template_name = self.get_template_names()
            # Рендерим и возвращаем HTML-шаблон
            return render(request, template_name[0], context)
        except Profile.DoesNotExist:
            return HttpResponse("Пользователь не обнаружен", status=404)


class SuperuserDeleteDenied(TemplateView):
    """ Класс вывода страницы о невозможности удаления суперпользователя """
    template_name = 'users/components/superuser_delete_denied.html'


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, View):
    model = Profile
    success_url = reverse_lazy('index')
    success_message = 'Профиль пользователя удален'

    def delete_profile(self, request, *args, **kwargs):
        """Удаление профиля пользователя с проверкой суперпользователя."""
        user_id = request.user.pk
        if request.user.is_superuser:
            return redirect('superuser_delete_denied')
        profile = get_object_or_404(Profile, pk=user_id)
        profile.delete()
        messages.success(request, self.success_message)
        logout(request)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        #     return redirect('superuser_delete_denied')
        return render(request, 'layout/access_denied.html')
    
    def post(self, request, *args, **kwargs):
        return self.delete_profile(request, *args, **kwargs)


class AllUsersView(LoginRequiredMixin, ListView):
    """
    Класс просмотра информации обо всех пользователях.
    Внимание! Просмотр доступен только Суперпользователям.
    """
    model = Profile

    def get_template_names(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            template_name = 'users/all_users.html'
        else:
            template_name = 'layout/access_denied.html'
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_users"] = Profile.objects.all()
        return context


class DeleteAllInactiveUsersView(LoginRequiredMixin, View):
    """
    Класс удаления неактивных пользователей
    """
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            # Удаляем всех неактивных пользователей
            self.inactive_users = Profile.objects.filter(is_active=False)
            self.count = self.inactive_users.count()
            if self.count > 0:
                self.inactive_users.delete()
                messages.success(request, f'Неактивные профили удалены.')
            else:
                messages.warning(
                    request, 'В сервисе нет неактивных пользователей.')
        else:
            messages.error(
                request, 'У вас нет прав для выполнения этого действия.')

        return redirect('all_users')
