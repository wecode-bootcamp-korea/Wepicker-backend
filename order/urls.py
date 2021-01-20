from django.urls import path
from .views      import OrderItemView, OrderItemUpdateView

urlpatterns = [
    path('/cart', OrderItemView.as_view()),
    path('/cartUpdate', OrderItemUpdateView.as_view()),
]