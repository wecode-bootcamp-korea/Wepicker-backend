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
            user  = User.objects.filter(id=request.user.id).prefetch_related('order', 'address', 'point', 'card')[0]

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




