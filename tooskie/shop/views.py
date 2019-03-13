from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from .models import Product

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = ['name', 'name_fr', 'picture',]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The product was added.'
        )    
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('recipe:ingredient_list',)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update.html'
    fields = ['name', 'name_fr', 'picture',]

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe:ingredient_list',)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'confirm_delete.html'

    def get_recipe(self, queryset=None):
        obj = super(ProductDeleteView, self).get_object()
        self.product = Product.objects.get(id=obj.product.id)
        return obj

    def get_success_url(self):
        return reverse('recipe:ingredient_list',)