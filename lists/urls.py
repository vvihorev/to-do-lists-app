from django.urls import include, re_path
from lists import views

urlpatterns = [
    re_path(r'^new$', views.new_list, name='new_list'),
    re_path(r'^(\d+)/$', views.view_list, name='view_list'),
    re_path(r'^remove_item(\d+)/$', views.remove_item, name='remove_item'),
]
