from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nfs/', views.list_nfs, name='notas_fiscais'),
    path('nf/<int:nf_id>/', views.detail_nf, name='nota_fiscal'),

]
