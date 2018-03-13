from django.urls import path

import api.views as api

urlpatterns = [
    path('positions/', api.get_positions, name='get_positions'),
]
