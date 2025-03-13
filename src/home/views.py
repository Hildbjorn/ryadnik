from django.views.generic import TemplateView

__all__ = (
    'IndexView',
)


class IndexView(TemplateView):
    """
    Класс вывода главной страницы.

    Атрибуты:
        template_name (str): Имя шаблона, который будет использоваться для отображения главной страницы.
    """
    template_name = 'home/index.html'

