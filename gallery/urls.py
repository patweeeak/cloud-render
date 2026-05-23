from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryHomeView.as_view(), name='gallery_home'),
    path('recipe/create/', views.RecipePhotoCreateView.as_view(), name='create_recipe'),
    path('recipe/<int:pk>/edit/', views.RecipePhotoUpdateView.as_view(), name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.RecipePhotoDeleteView.as_view(), name='delete_recipe'),
]

