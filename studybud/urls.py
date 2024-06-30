"""
URL configuration for studybud project.

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

# this urls file is for whole project

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# include is importing function which tells jango that there is a other url file in other app(here base)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('base.urls')),
    # when there is a empty string, send user to base app's urls file
    # path("", home),
    # path("room/", room)
    # parameters of path: the route and the function that we want to call

    path('api/', include('base.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
