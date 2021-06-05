from django.conf.urls import url
from . import views
from .views import WordTranslation,TranslationWord

urlpatterns = [
    url(r'^api/materials$', views.material_list),
    url(r'^api/materials/(?P<pk>[0-9]+)$', views.material_detail),
    url(r'^api/dict$', views.dict_list),
    url(r'^api/dict_one_word$', views.dict_one_word),
    url(r'^api/dict_one_word_save$', views.dict_one_word_save),
    url(r'^api/dict/(?P<pk>[0-9]+)$', views.dict),
    url(r'^api/questions$',TranslationWord.as_view()),
    url(r'^api/questions_inverted$',WordTranslation.as_view()),
    url(r'^api/search$', views.search),
    url(r'^api/change$', views.change),
    url(r'^api/change_inverted$', views.change_inverted),
]

#url(r'^api/dict_i/(?P<pk>[0-9]+)$', views.dict_increment),
#url(r'^api/dict_d/(?P<pk>[0-9]+)$', views.dict_decrement),
#url(r'^api/dict_i_inverted/(?P<pk>[0-9]+)$', views.dict_increment_inverted),
#url(r'^api/dict_d_inverted/(?P<pk>[0-9]+)$', views.dict_decrement_inverted),