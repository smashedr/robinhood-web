from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from django.views.generic.base import RedirectView

import connect.views as connect
import home.views as home
import stock.views as stock

urlpatterns = [
    path('favicon\.ico', RedirectView.as_view(
        url=static('images/favicon.ico')
    )),
    path('', home.home_view, name='home_view'),
    path('share/<str:share_id>', home.share_view, name='share_view'),
    path('save/', home.save_share, name='save_share'),
    path('stock/', stock.home_view, name='stock_home'),
    path('stock/<str:symbol>/', stock.stock_view, name='stock_view'),
    path('search/', stock.stock_search, name='stock_search'),
    path('login/', connect.show_login, name='show_login'),
    path('auth/', connect.do_login, name='do_login'),
    path('logout/', connect.do_logout, name='do_logout'),
    path('admin/', admin.site.urls, name='django_admin'),
]
