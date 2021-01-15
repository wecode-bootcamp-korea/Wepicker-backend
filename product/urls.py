from django.urls import path
from .views      import ProductAllView

urlpatterns = [
   path('/all', ProductAllView.as_view()),

]