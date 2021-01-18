import jwt
import json
import bcrypt

from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse, HttpResponse

from .models          import Order. OrderItem, OrderState, PaymentType, DeliveryCost, DeliveryType
from decorator        import login_check


# 장바구니에 담기
class OrderItemView(View):
    @login_check
    def post(self, request):


# 결제하기
class OrderView(View):
    @login_check
    def post(self, request)
