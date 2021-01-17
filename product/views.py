import json
import math

from django.db.models      import Count
from django.views          import View
from django.http           import JsonResponse, HttpResponse

from .models               import Product, Category, Image, Option, Question, Review, Comment

# 상품 전체 보기
class ProductAllView(View):
    def get(self, request):
        try:
            page         = int(request.GET.get('page', 1))
            PAGE_SIZE    = 9
            max_page     = math.ceil(Product.objects.all().count()/PAGE_SIZE)

            if page > max_page:
                page = 2
            if page < 1:
                page = 1

            limit        = PAGE_SIZE * page
            offset       = limit - PAGE_SIZE
            categories   = Category.objects.all()
            ordering     = request.GET.get('ordering')
            category     = request.GET.get('category')

            sort_type = {
                'min_price' : 'price',
                'max_price' : '-price',
                'abc'       : 'name',
                'descabc'   : '-name' 
            }

            if category is not None:
                if ordering is not None:
                    products = Product.objects.filter(category_id=category).order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
                else:
                    products = Product.objects.filter(category_id=category).order_by('pub_date').prefetch_related('image_url')[offset:limit]
                if ordering == 'best':
                    products = Product.objects.filter(category_id=category).annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]

            if category is None:
                if ordering is not None and ordering != 'best':
                    products = Product.objects.order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
                else:
                    products = Product.objects.order_by('pub_date').prefetch_related('image_url')[offset:limit]
                    
                if ordering == 'best':
                    products = Product.objects.annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]
                
            product_list = [{
                    'category'       : product.category.category,
                    'name'           : product.name,
                    'price'          : product.price,
                    'description'    : product.description,
                    'thumnail_image' : product.image_url.first().image_url,
                    'sub_image'      : product.image_url.all()[1].image_url,
                    'pub_date'       : product.pub_date
                } for product in products ]

            return JsonResponse({'product_list':product_list}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=404)


# 상품 상세 보기
class ProductView(View):
    def get(self, request, product_id):
        try:
            product = product_id

            if not Option.objects.filter(product=product_id).exists():
                return JsonResponse({'message':'OPTION_DOES_NOT_EXOST'}, status=200)

            options     = Option.objects.filter(product=product_id)
            option_list = [{
                    'name'  : option.name,
                    'price' : option.price
                } for option in options]
            
            return JsonResponse({'option_list':option_list}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=404)
