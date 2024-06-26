from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('snippets/', views.snippet_detail),
    path('snippets/<int:id>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)