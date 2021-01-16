from django.urls import path
from .views      import ProductAllView#, ProductView

urlpatterns = [
   path('/all', ProductAllView.as_view()),
   #path('/<int:product_id>', ProductView.as_view()),

]