from django.urls import path
from . import views


urlpatterns = [
    path('',views.main_view, name='home'),
    path('products',views.products, name='products'),
    path('products/<int:id>/',views.details, name='details'),

]

