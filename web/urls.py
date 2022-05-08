from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nodes/', views.NodeListView.as_view(), name='node_list'),
    path('nodes/<int:pk>/', views.NodeDetailView.as_view(), name='node_detail'),
]
