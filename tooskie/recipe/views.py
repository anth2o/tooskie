from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ingredient, Recipe, Tag, IngredientInRecipe, RecipeHasNutritionalProperty, DifficultyLevel, BudgetLevel, Ingredient
from .forms import RecipeStepsFormset, IngredientsFormset, NutritionalPropertiesFormset, TagRecipesFormset, RecipeModelForm
from tooskie.pantry.models import Pantry
from tooskie.pantry.generate_recipes import filter_recipes, get_ingredients, get_recipes_pickle,save_recipes_pickle
from .serializers import IngredientSerializerWithPicture, RecipeSerializer, TagWithRecipesSerializer

import logging

logger = logging.getLogger("django")

@api_view(['GET'])
def all_ingredients(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializerWithPicture(ingredients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def ingredient_by_id(request, id):
    try:
        ingredient = Ingredient.objects.get(id=id)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializerWithPicture(ingredient)
        return Response(serializer.data)

@api_view(['GET'])
def ingredient_by_permaname(request, permaname):
    try:
        ingredient = Ingredient.objects.get(permaname=permaname)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializerWithPicture(ingredient)
        return Response(serializer.data)

@api_view(['GET'])
def recipe_with_pantry(request, permaname):
    try:
        try:
            recipes = get_recipes_pickle()
        except:
            recipes = save_recipes_pickle()
        pantry = Pantry.objects.get(permaname=permaname)
        ingredients = get_ingredients(pantry)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            recipes = filter_recipes(recipe_list=recipes, ingredients=ingredients)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def recipe(request, permaname):
    if request.method == 'GET':
        try:
            recipe = Recipe.objects.get(permaname=permaname)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_tags(request):
    if request.method == 'GET':
        try:
            tags = Tag.objects.filter(to_display=True)
            serializer = TagWithRecipesSerializer(tags, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class HomeView(TemplateView):
    template_name = 'home.html'

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/list.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/detail.html'

class RecipeCreateView(CreateView):
    model = Recipe
    template_name = 'recipe/create.html'
    form_class = RecipeModelForm

    def form_valid(self, form):
        form.save()
        self.object = form.instance
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The recipe was added.'
        )
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class RecipeUpdateView(UpdateView):
    template_name = 'recipe/update.html'
    model = Recipe
    form_class = RecipeModelForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        initial_data = self.object.__dict__                
        initial_data['tags'] = Tag.objects.filter(recipes_not_filtered=self.object, to_display=True)
        logger.debug(initial_data)
        if initial_data['difficulty_level_id'] is not None:
            initial_data['difficulty_level'] = DifficultyLevel.objects.get(pk=initial_data['difficulty_level_id'])
        if initial_data['budget_level_id'] is not None:
            initial_data['budget_level'] = BudgetLevel.objects.get(pk=initial_data['budget_level_id'])
        logger.debug(initial_data)
        form = RecipeModelForm(initial=initial_data)
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        logger.debug(form.cleaned_data)
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

class RecipeUpdateStepsView(SingleObjectMixin, FormView):
    """
    For adding steps to a Recipe, or editing them.
    """
    model = Recipe
    template_name = 'recipe/update_steps.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return RecipeStepsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe:recipe_detail', kwargs={'pk': self.object.pk})

class RecipeUpdateIngredientsView(SingleObjectMixin, FormView):
    """
    For adding ingredients to a Recipe, or editing them.
    """
    model = Recipe
    template_name = 'recipe/update_ingredients.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        instance_list = IngredientInRecipe.objects.filter(recipe=self.object)
        initial_data = []
        for instance in instance_list:
            initial_data.append({'quantity': instance.quantity, 'unit': instance.unit_of_ingredient.unit, 'ingredient': instance.unit_of_ingredient.ingredient})
        formset = IngredientsFormset(initial=initial_data)
        return self.render_to_response({'form': formset, 'recipe': self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return IngredientsFormset(**self.get_form_kwargs())

    def form_valid(self, formset):
        if formset.is_valid():
            for form in formset:
                form.save(recipe=self.object)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Changes were saved.'
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe:recipe_detail', kwargs={'pk': self.object.pk})

class RecipeUpdateNutritionalPropertiesView(SingleObjectMixin, FormView):
    """
    For adding nutritional properties to a Recipe, or editing them.
    """
    model = Recipe
    template_name = 'recipe/update_nutri.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        instance_list = RecipeHasNutritionalProperty.objects.filter(recipe=self.object)
        initial_data = []
        for instance in instance_list:
            initial_data.append({'quantity': instance.quantity, 'unit': instance.unit_of_nutritional_property, 'nutritional_property': instance.nutritional_property})
        formset = NutritionalPropertiesFormset(initial=initial_data)
        return self.render_to_response({'form': formset, 'recipe': self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return NutritionalPropertiesFormset(**self.get_form_kwargs())

    def form_valid(self, formset):
        logger.debug(self.object)
        if formset.is_valid():
            for form in formset:
                form.save(recipe=self.object)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Changes were saved.'
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe:recipe_detail', kwargs={'pk': self.object.pk})

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'confirm_delete.html'

    def get_recipe(self, queryset=None):
        obj = super(RecipeDeleteView, self).get_object()
        self.recipe = Recipe.objects.get(id=obj.recipe.id)
        return obj

    def get_success_url(self):
        return reverse('recipe:recipe_list',)

class TagListView(ListView):
    model = Tag
    template_name = 'tag/list.html'

class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag/detail.html'

class TagCreateView(CreateView):
    model = Tag
    template_name = 'tag/create.html'
    fields = ['name', 'name_fr', 'picture', 'to_display', 'description', 'description_fr']

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The tag was added.'
        )
        return super().form_valid(form)

class TagUpdateView(UpdateView):
    model = Tag
    template_name = 'tag/update.html'
    fields = ['name', 'name_fr', 'picture', 'description', 'description_fr']

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

class TagUpdateRecipesView(SingleObjectMixin, FormView):
    """
    For adding recipes to a Tag, or editing them.
    """
    model = Tag
    template_name = 'tag/update_recipes.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        instance_list = Recipe.objects.filter(tag=self.object)
        initial_data = []
        for instance in instance_list:
            initial_data.append({'recipe': instance})
        formset = TagRecipesFormset(initial=initial_data)
        logger.debug(initial_data)
        return self.render_to_response({'form': formset, 'tag': self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return TagRecipesFormset(**self.get_form_kwargs())

    def form_valid(self, formset):
        if formset.is_valid():
            for form in formset:
                form.save(tag=self.object)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Changes were saved.'
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe:tag_detail', kwargs={'pk': self.object.pk})

class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'confirm_delete.html'

    def get_recipe(self, queryset=None):
        obj = super(TagDeleteView, self).get_object()
        self.recipe = Tag.objects.get(id=obj.recipe.id)
        return obj

    def get_success_url(self):
        return reverse('recipe:tag_list',)


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredient/list.html'