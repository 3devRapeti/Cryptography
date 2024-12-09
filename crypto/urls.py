from django.urls import path
from . import views

urlpatterns = [
    path('',views.land,name='land'),
    path('alice1/',views.alice1,name='alice1'),
    path('bob1/',views.bob1,name="bob1"),
    path('eve1/',views.eve1,name="eve1"),
    path('alice2/',views.alice2,name="alice2"),
    path('rsab0/',views.rsab0,name='rsab0'),
    path('rsab/',views.rsab,name='rsab'),
    path('rsaa/',views.rsaa,name='rsaa'),
    path('rsae/',views.rsae,name='rsae'),
]