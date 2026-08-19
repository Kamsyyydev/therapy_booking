from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('offer/<slug:slug>/', views.offer_detail_view, name='offer_detail'),
]
