from django.urls import path
from . import views

urlpatterns = [
    path('parts/', views.PartViewset.as_view()),
]