from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import visited_links

urlpatterns = [
    path('', visited_links, name='visited_links'),
    path('', visited_links, name='visited_links'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
