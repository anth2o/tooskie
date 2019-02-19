from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipe/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/update/<int:pk>/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/update_steps/<int:pk>/', views.RecipeUpdateStepsView.as_view(), name='recipe_update_steps'),
    path('recipe/update_ingredients/<int:pk>/', views.RecipeUpdateIngredientsView.as_view(), name='recipe_update_ingredients'),
    path('recipe/update_nutri/<int:pk>/', views.RecipeUpdateNutritionalPropertiesView.as_view(), name='recipe_update_nutri'),
    path('recipe/delete/<int:pk>/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('tag/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tag/add/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/update/<int:pk>/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tag/update_recipes/<int:pk>/', views.TagUpdateRecipesView.as_view(), name='tag_update_recipes'),
    path('tag/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
]
