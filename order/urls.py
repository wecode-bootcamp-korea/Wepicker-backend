from django.urls import path
from .views      import OrderItemView

urlpatterns = [
    path('/createCart', OrderItemView.as_view()),
]