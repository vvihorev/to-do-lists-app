from django.urls import include, re_path, path

from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    re_path(r'^$', list_views.home_page, name='home'),
    path('lists/', include(list_urls)),
]
