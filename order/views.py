import jwt
import json
import bcrypt

from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse, HttpResponse

from .models          import Order, OrderItem, OrderState
from user.models      import User, Address
from product.models   import Product, Option
from decorator        import login_check


class OrderItemView(View):
    @login_check
    @transaction.atomic
    def post(self, request): 
        try:
            data        = json.loads(request.body)
            option_list = data.get('option_list')
            """
            data = {
                "product_id":2,
                "quantity":1,
                "price":4000,
                "option_list" = [
                    {
                        "option_id"       : 1,
                        "option_quantity" : 3
                    }
                    {
                        "option_id"       : 2,
                        "option_quantity" : 1
                    }
                ],
                "delivery_cost_id":1
            }
            """

            #기존 ORDER 존재 / 상품 업데이트(수량, 갸격)
            for i in range(len(option_list)): # 들어있는 모든 옵션id가 일치해야 if문 통과. 지금 조건문은 하나만 일치하면 일단 통과   
                if Order.objects.filter(user=request.user.id, state_id=1, orderItem__product_id=data['product'], \
                    orderItem__delivery_cost_id=data['delivery_cost'], orderItem__option=[option_list[i]]).exists():
                    
                    order = Order.objects.get(user=request.user.id, state_id=1, orderItem__product_id=data['product'], \
                        orderItem__delivery_cost_id=data['delivery_cost'], orderItem__option=[option_list[i]])

                    order_item = order.orderItem.get(option=[option_list[i]])

                    order_item.product_id                   = data['product']
                    order_item.quantity                     = order_item.quantity + data['quantity']
                    order_item.delivery_cost_id             = data['delivery_cost']
                    order_item.option                       = option_list
                    order_item.option[0]['option_quantity'] = order_item.option[0]['option_quantity'] +  order_item.option[i]['option_quantity']
                    order_item.price                        = order_item.price + data['price'] # 옵션에 가격이 있다면 걔도 더해야됨
                    order_item.save()
                    
                    return JsonResponse({'message':'SUCCESS'}, status=201)

            # GET 0R CREATE로 바꾸기
            # 기존 ORDER 존재 / 다른 상품 추가
            if Order.objects.filter(user=request.user.id, state_id=1).exists():

                OrderItem(
                    product_id       = data['product'],
                    order            = Order.objects.get(user=request.user.id, state_id=1),
                    quantity         = data['quantity'],
                    delivery_cost_id = data['delivery_cost'],
                    option           = option_list,
                    price            = data['price']
                ).save()

                return JsonResponse({'message':'SUCCESS'}, status=201)

            # 처음 장바구니에 담을 경우
            if Address.objects.filter(user=request.user.id).filter(default=True).exists():
                address = Address.objects.filter(user=request.user.id).get(default=True)
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
                delivery_cost_id = data['delivery_cost']
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
                'option'        : order_item.option.id,
                'delivery_cost' : order_item.delivery_cost.id
            }for order_item in order.orderItem.all()]

            return JsonResponse({'cart_list':order_item_list}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)