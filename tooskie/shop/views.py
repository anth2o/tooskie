from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from .models import Product
from .forms import ProductModelForm, ProductPriceFormset
from tooskie.recipe.models import Unit, Ingredient

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create.html'
    form_class = ProductModelForm

    def get(self, request, pk, *args, **kwargs):
        ingredient = Ingredient.objects.get(id=pk)
        initial_data = {}   
        initial_data['ingredient'] = ingredient
        form = ProductModelForm(initial=initial_data)
        return self.render_to_response({'form': form, 'ingredient': ingredient})

    def form_valid(self, form):
        form.save()
        self.object = form.instance
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The product was added.'
        )    
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        unit_of_ingredient = self.object.unit_of_ingredient
        return reverse('recipe:ingredient_detail', kwargs={'pk': unit_of_ingredient.ingredient.id})

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update.html'
    form_class = ProductModelForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Product.objects.all())
        initial_data = self.object.__dict__
        unit_of_ingredient = self.object.unit_of_ingredient   
        initial_data['ingredient'] = unit_of_ingredient.ingredient
        initial_data['unit'] = unit_of_ingredient.unit
        initial_data['picture'] = self.object.picture
        try:
            initial_data['price'] = self.object.prices.all()[0].price
            initial_data['quantity'] = self.object.prices.all()[0].quantity
            initial_data['shop'] = self.object.prices.all()[0].shop
        except:
            pass
        form = ProductModelForm(initial=initial_data)
        return self.render_to_response({'form': form, 'ingredient': unit_of_ingredient.ingredient})

    def form_valid(self, form):
        form.save()
        self.object = form.instance
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        unit_of_ingredient = self.object.unit_of_ingredient
        return reverse('recipe:ingredient_detail', kwargs={'pk': unit_of_ingredient.ingredient.id})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'confirm_delete.html'

    def get_product(self, queryset=None):
        obj = super(ProductDeleteView, self).get_object()
        self.object = Product.objects.get(id=obj.product.id)
        return obj

    def get_success_url(self):
        unit_of_ingredient = self.object.unit_of_ingredient
        return reverse('recipe:ingredient_detail', kwargs={'pk': unit_of_ingredient.ingredient.id})