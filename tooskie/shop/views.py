from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, DeleteView, UpdateView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'