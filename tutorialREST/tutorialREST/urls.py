
from django.contrib import admin
from django.urls import path, include
from snippets import views
from rest_framework.routers import DefaultRouter

"""
 Add router to see the REST style of obj.-list at browser
"""
router = DefaultRouter()
router.register(r'snippets', views.SnippetList, basename='snippet')
router.register(r'users', views.UserList, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('snippets.urls')),
]