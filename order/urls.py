from django.urls import path
from .views      import OrderItemView

urlpatterns = [
    path('/cart', OrderItemView.as_view()),
]