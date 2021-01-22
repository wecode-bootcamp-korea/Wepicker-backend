import jwt
import json
import bcrypt

from django.views     import View
from django.http      import JsonResponse, HttpResponse

from .models          import Order, OrderItem, OrderState
from user.models      import User, Address
from product.models   import Product, Option
from decorator        import login_check


class OrderItemView(View):
    @login_check
    def post(self, request): 
        try:
            data          = json.loads(request.body)
            option_list   = data.get('option_list')
            delivery_cost = data['delivery_cost']
            
            if delivery_cost[0] == 2:
                  delivery_cost = 3
            else:
                if delivery_cost[1] == 1:
                    delivery_cost = 1
                else:
                    delivery_cost = 2

            if Order.objects.filter(user=request.user.id, state_id=1, orderItem__delivery_cost_id=delivery_cost).exists():

                order_item, created = OrderItem.objects.get_or_create(
                        order__user_id=request.user.id, 
                        order__state_id=1, 
                        product_id=data['product'], 
                        delivery_cost_id=delivery_cost
                )
               
                if created:   # 기존 ORDER 존재 / 다른 상품 추가
                    print(order_item.order_id)
                    order_item.order_id   = order_item.order_id
                    order_item.product_id = data["product"]
                    order_item.option     = option_list
                    order_item.quantity   = data["qantity"]
                    order_item.price      = data["price"]
                    delivery_cost_id      = delivery_cost
                    order_item.save()
                    return JsonResponse({'message':'SUCCESS'}, status=201)

                for input_option in option_list: #기존 ORDER 존재 / 상품 업데이트(수량, 갸격)
                    for option in order_item.option: # 옵션까지 일치할 경우 수량, 가격 더해주기
                        if input_option['option_id'] == option["option_id"]:
                            order_item.quantity                     = order_item.quantity + data['quantity']
                            order_item.price                        = order_item.price + int(data['price'])
                            order_item.option[0]['option_quantity'] = order_item.option[0]['option_quantity'] + input_option['option_quantity']
                            order_item.save()
                        else: # 새로운 옵션 추가
                            order_item.quantity = order_item.quantity + data['quantity']
                            order_item.price    = order_item.price + int(data['price'])
                            order_item.option.append(input_option)
                            order_item.save()
                            return JsonResponse({'message':'SUCCESS'}, status=201)
                return JsonResponse({'message':'SUCCESS'}, status=201)

            # 처음 장바구니에 담을 경우
            if Address.objects.filter(user=request.user, default=True).exists():
                address = Address.objects.filter(user=request.user).get(default=True)
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
                product_id       = data['product'],
                order            = Order.objects.filter(user=request.user, state_id=1).last(),
                quantity         = data['quantity'],
                price            = data['price'],
                option           = option_list,
                delivery_cost_id = delivery_cost
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

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
                'option'        : order_item.option,
                'delivery_cost' : order_item.delivery_cost.id
            }for order_item in order.orderItem.all()]

            return JsonResponse({'cart_list':order_item_list}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)