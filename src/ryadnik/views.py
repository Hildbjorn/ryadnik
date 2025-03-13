import os
from django.http import FileResponse
from django.shortcuts import render

from django.conf import settings


__all__ = (
    'page_not_found_view',
    'serve_documents',
)


def page_not_found_view(request, exception):
   """
   Функция обработки ошибки 404 (страница не найдена).
   """
   return render(request, '404.html', status=404)



def serve_documents(request, filename):
    """
    Функция, которая принимает имя файла в качестве аргумента и возвращает файл.
    """
    filepath = os.path.join(settings.MEDIA_ROOT, 'documents', filename)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
