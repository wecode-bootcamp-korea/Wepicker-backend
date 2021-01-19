import jwt
import json
import bcrypt

from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse, HttpResponse

from .models          import Order, OrderItem, OrderState, DeliveryCost
from user.models      import User, Address
from product.models   import Product, Option
from decorator        import login_check


class OrderItemView(View):
    @login_check
    @transaction.atomic
    def post(self, request): 
        try:
            data  = json.loads(request.body)
            user  = User.objects.filter(id=request.user.id)[0]

            if Address.objects.filter(user=user.id).filter(default=True).exists():
                address = Address.objects.filter(user=user.id).filter(default=True)
            else:
                address = data.get('address')

            Order(
                user           = request.user,
                address        = address,
                point          = data.get('point'),
                card           = data.get('card'),
                state          = OrderState.objects.get(state='결제 전'),
                memo           = data.get('memo'),
                payment_method = data.get('payment_method'),
                payment_type   = data.get('payment_type')
            ).save()

            OrderItem(
                product       = Product.objects.get(id=data['product']),
                order         = Order.objects.filter(user=user).last(),
                quantity      = data['quantity'],
                price         = data['price'],
                option        = Option.objects.get(id=data['option']),
                delivery_cost = DeliveryCost.objects.get(id=data['delivery_cost'])
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_check
    def get(self, request):
        try:
            user  = request.user

            if not Order.objects.filter(user=user).exists():
                return JsonResponse({'message':'CART_DOES_NOT_EXIST'}, status=400)

            order = Order.objects.filter(user=user).prefetch_related('orderItem')[0]

            order_item_list = [{
                'product'       : order_item.product.id,
                'quantity'      : order_item.quantity,
                'price'         : order_item.price,
                'option'        : order_item.option.id,
                'delivery_cost' : order_item.delivery_cost.id
            }for order_item in order.orderItem.all()]

            return JsonResponse({'cart_list':order_item_list}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class OrderItemUpdateView(View):
    @login_check
    def post(self, request):
        try:
            user       = request.user
            order_item = Order.objects.filter(user=user).prefetch_related('orderItem')[0].orderItem.all() 



            OrderItem(
                product       = Product.objects.get(id=data['product']),
                order         = Order.objects.filter(user=user).last(),
                quantity      = data['quantity'],
                price         = data['price'],
                option        = Option.objects.get(id=data['option']),
                delivery_cost = DeliveryCost.objects.get(id=data['delivery_cost'])
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

# class QuantityUpdateView(View):
#      @login_check
#      def post(self, request):
#          try:
#              # 장바구니에 같은 상품 있으면 수량 += 1, 없으면 Create
             
#             return JsonResponse({'message':'SUCCESS'}, status=200)
#         except KeyError:
#             return JsonResponse({'message':'KEY_ERROR'}, status=400)

  




