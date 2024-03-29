from django.urls import path
from tournaments import views

urlpatterns = [
    path('create_tournament/', views.create_tournament, name='create_tournament'),
    path('join_tournament/<int:tournament_id>/', views.join_tournament, name='join_tournament'),

]