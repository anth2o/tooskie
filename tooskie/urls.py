"""tooskie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from tooskie.recipe import views as recipe_views
from tooskie.pantry import views as pantry_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^ingredient/$', recipe_views.all_ingredients),
    url(r'^ingredient/(?P<id>[0-9]+)$', recipe_views.ingredient_by_id),
    url(r'^ingredient/(?P<permaname>.+)$', recipe_views.ingredient_by_permaname),
    url(r'^pantry/$', pantry_views.pantry),
    url(r'^pantry/(?P<permaname>.+)$', pantry_views.pantry_by_permaname),
    url(r'^recipe/(?P<permaname>.+)$', recipe_views.recipe),
    url(r'^recipe-with-pantry/(?P<permaname>.+)$', recipe_views.recipe_with_pantry),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
