from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nfs/', views.list_nfs, name='list_nfs'),
    path('nf/<int:id>/', views.detail_nf, name='detail_nf'),
    path('nf/<int:id>/delete/', views.delete_nf, name='delete_nf'),
    path('fornecedores/', views.list_fornecedores, name='list_fornecedores'),
    path('fornecedor/<int:id>/delete/', views.delete_fornecedor, name='delete_fornecedor'),
    path('clientes/', views.list_clientes, name='list_clientes'),
    path('cliente/<int:id>/delete/', views.delete_cliente, name='delete_cliente'),
]
