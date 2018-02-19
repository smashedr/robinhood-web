from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from django.views.generic.base import RedirectView

import auth.views as auth
import home.views as home

urlpatterns = [
    path('favicon\.ico', RedirectView.as_view(
        url=static('images/favicon.ico')
    )),
    path('', home.v_home, name='v_home'),
    path('share/<str:share_id>', home.v_share, name='v_share'),
    path('login/', auth.show_login, name='show_login'),
    path('auth/', auth.do_login, name='do_login'),
    path('logout/', auth.do_logout, name='do_logout'),
    path('admin/', admin.site.urls, name='django_admin'),
]
