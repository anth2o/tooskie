from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipe/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', views.RecipeCreateView.as_view(), name='recipe_create'),
    # path('recipe/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_update'),
]
