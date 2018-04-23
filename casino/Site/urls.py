from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^signin/', views.login_register_page, name='signin' ),
    url(r'^index/', views.index, name='index' ),
    url(r'^signout/', views.logout, name='logout' ),
    url(r'^game/', views.game, name='game' ),
    url(r'^manage/', views.manage, name='manage' ),


]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)