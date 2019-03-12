from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'

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
        return super().form_valid(form)

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

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'confirm_delete.html'

    def get_recipe(self, queryset=None):
        obj = super(TagDeleteView, self).get_object()
        self.recipe = Tag.objects.get(id=obj.recipe.id)
        return obj

    def get_success_url(self):
        return reverse('shop:product_list',)