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
            data = json.loads(request.body)
            user = User.objects.filter(id=request.user.id)[0]

            if Order.objects.filter(user=user.id).exists() : # order테이블이 없는 경우는 빈 쿼리셋 옴
                order_item = Order.objects.filter(user=user.id).prefetch_related('orderItem')[0].orderItem.all()
                order      = Order.objects.filter(user=user, state_id=1)

                for new_order_item in order_item: # 이미 존재하는 상품이 들어올 경우
                    if new_order_item.product == Product.objects.get(id=data['product']) and new_order_item.delivery_cost.id == Product.objects.get(id=data['delivery_cost']).id and new_order_item.option.id == Product.objects.get(id=data['option']).id:
                        OrderItem(
                        id            = OrderItem.objects.get(id=new_order_item.id).id,
                        product       = Product.objects.get(id=data['product']),
                        order         = Order.objects.filter(user=user, state_id=1).last(),
                        quantity      = new_order_item.quantity + data['quantity'],
                        price         = data['price'],
                        option        = Option.objects.get(id=data['option']),
                        delivery_cost = DeliveryCost.objects.get(id=data['delivery_cost'])
                    ).save()
                        return JsonResponse({'message':'SUCCESS'}, status=201)

                if order.exists(): # 상품은 다르지만 이미 order 테이블이 있는 user일 경우 (orderItem만 create)
                    order =  Order.objects.filter(id=order[0].id)[0]
                    OrderItem(
                    product       = Product.objects.get(id=data['product']),
                    order         = order,
                    quantity      = data['quantity'],
                    price         = data['price'],
                    option        = Option.objects.get(id=data['option']),
                    delivery_cost = DeliveryCost.objects.get(id=data['delivery_cost'])
                    ).save()
                    return JsonResponse({'message':'SUCCESS'}, status=201)

            # 처음 장바구니에 담을 경우
            if Address.objects.filter(user=user.id).filter(default=True).exists():
                address = Address.objects.filter(user=user.id).get(default=True)
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
                order         = Order.objects.filter(user=user, state_id=1).last(),
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



  




