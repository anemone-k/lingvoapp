from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/materials$', views.material_list),
    url(r'^api/materials/(?P<pk>[0-9]+)$', views.material_detail),
    url(r'^api/dict$', views.dict_list),
    url(r'^api/dict_one_word$', views.dict_one_word),
    url(r'^api/dict_one_word_save$', views.dict_one_word_save),
    url(r'^api/dict/(?P<pk>[0-9]+)$', views.dict_delete),
]