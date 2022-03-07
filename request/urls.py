from django.urls import path
from . import views


urlpatterns = [
    path('request/', views.RequestView.as_view()),
]