from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipe/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/update_steps/<int:pk>/', views.RecipeUpdateStepsView.as_view(), name='recipe_update_steps'),
    path('recipe/delete/<int:pk>/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('tag/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tag/add/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
]
