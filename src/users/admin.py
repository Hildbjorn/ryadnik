from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.templatetags.static import static
from django.utils.html import format_html
from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    """
    Класс ProfileAdmin наследуется от UserAdmin и используется для настройки административного интерфейса Django для модели Profile.
    """
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile

    def get_form(self, request, obj=None, **kwargs):
        """
        Метод get_form возвращает класс формы, который будет использоваться для создания или изменения объекта Profile.
        Если мы в режиме создания объекта (obj=None), добавляем request в kwargs.
        """
        # Получаем класс формы через super()
        form_class = super().get_form(request, obj, **kwargs)
        # Если мы в режиме создания объекта (obj=None), добавляем request
        if obj is None:
            class FormWithRequest(form_class):
                def __init__(self, *args, **kwargs):
                    kwargs['request'] = request
                    super().__init__(*args, **kwargs)
            return FormWithRequest
        return form_class

    def image_tag(self, obj):
        """
        Метод image_tag возвращает HTML-тег изображения для отображения в списке объектов Profile.
        Если у объекта есть изображение, возвращаем его URL, иначе возвращаем URL изображения по умолчанию.
        """
        if obj.image:
            return format_html('<img id="image_tag" src="{}" />', obj.image.url)
        else:
            default_image_url = static('img/elements/no_photo.webp')
            return format_html('<img id="image_tag" src="{}" />', default_image_url)

    image_tag.short_description = 'Аватар'

    def image_thumbnail(self, obj):
        """
        Метод image_thumbnail возвращает HTML-тег изображения для отображения в списке объектов Profile.
        Если у объекта есть изображение, возвращаем его URL, иначе возвращаем URL изображения по умолчанию.
        """
        if obj.image:
            return format_html('<img id="image_thumbnail" src="{}" />',
                               obj.image.url)
        else:
            default_image_url = static('img/elements/no_photo.webp')
            return format_html('<img id="image_thumbnail" src="{}" />',
                               default_image_url)
    image_thumbnail.short_description = 'Аватар'

    list_display = ('image_tag', 'nic_name', '__str__', 'position', 'company', 'email', 'phone',
                    'subscribe', 'is_staff', 'is_active', 'is_superuser',)
    list_display_links = ('__str__', 'nic_name', 'image_tag', 'email',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Учетная запись', {'fields': ('reg_number', 'email', 'password', )}),
        ('Персональные данные', {
         'fields': ('image_thumbnail', 'image', 'nic_name', 'last_name', 'first_name', 'middle_name', 'phone',)}),
        ('Место работы', {'fields': ('company', 'position',)}),
        ('Согласие на обработку персональных данных',
         {'fields': (('agreement', 'subscribe'),)}),
        ('Активность', {'fields': (('date_joined', 'last_login'),)}),
        ('Группы', {'fields': ('groups',)}),
        ('Разрешения', {'fields': (('is_active', 'is_staff',
         'is_superuser'), 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = (
        'nic_name', 'last_name', 'first_name', 'middle_name', 'company', 'email', 'phone',)
    ordering = ('last_name', 'first_name',
                'middle_name', 'email', 'nic_name', )
    readonly_fields = ('reg_number', 'image_thumbnail',)


admin.site.site_title = 'Система урядная для управления делами'
admin.site.site_header = 'Рядник - Панель администратора'
