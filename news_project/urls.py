from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.HomePageView.as_view(), name='home'),
    path('news/<int:pk>/<slug:slug>/', views.SinglePageView.as_view(), name='single_page'), 
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('404/', views.error_page, name='404'),
]