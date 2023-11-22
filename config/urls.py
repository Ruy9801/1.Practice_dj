"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from rest_framework.routers import SimpleRouter 
from apps.accounts.views import AuthorViewSet, CustomerViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = SimpleRouter()
router.register('customer', CustomerViewSet)
router.register('author', AuthorViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Practice API',
        default_version='t1',
        description='pratice untill you rememberd'
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui("swagger")),
    path('api/', include(router.urls)),
    path('api/', include('apps.accounts.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
)