from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.HomePageView.as_view(), name='home'),
    path('news/<int:pk>/<slug:slug>/', views.SinglePageView.as_view(), name='single_page'), 
    path('news/<int:pk>/<slug:slug>/edit', views.NewsUpdateView.as_view(), name='news_update'),   
    path('news/<int:pk>/<slug:slug>/delete', views.NewsDeleteView.as_view(), name='news_delete'), 
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('404/', views.error_page, name='404'),
    path('admin-page/', views.admin_page, name='admin_page'),
]