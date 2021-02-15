from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="homepage"),
    path('user_signup/',views.user_signup, name="signup"),
    path('gallery/',views.gallery, name="gallery"),
    path('view/<int:pk>',views.ViewPhoto, name="view"),
    path('add/',views.AddPhoto, name="add"),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:pk>/', views.photo_delete, name='delete'),
]
