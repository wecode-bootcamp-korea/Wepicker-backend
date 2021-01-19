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
                'descabc'   : '-name',
                'recent'    : 'pub_date'
            }

            if category is not None:
                if ordering == 'best':
                    products = Product.objects.filter(category_id=category).annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]
                elif ordering is not None and ordering != 'best':
                    products = Product.objects.filter(category_id=category).order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
                else:
                    products = Product.objects.filter(category_id=category).order_by('pub_date').prefetch_related('image_url')[offset:limit]

            if category is None:
                if ordering == 'best':
                    products = Product.objects.annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]
                elif ordering is not None and ordering != 'best':
                    products = Product.objects.order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
                else:
                    products = Product.objects.order_by('pub_date').prefetch_related('image_url')[offset:limit]
                    
            product_list = [{
                    'product_id'     : product.id,
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
            product = Product.objects.filter(id=product_id).prefetch_related('option', 'image_url')[0]

            product_dict = {
                'product_id'    : product_id,
                'product_name'  : product.name,
                'product_price' : product.price,
                'description'   : product.description,
                'image_list'    : list(product.image_url.values_list('image_url', flat=True)),
                'option_list'   :  [{
                                    'option_name'  : option.name,
                                    'option_price' : option.price
                                } for option in product.option.all()]
                }
                
            return JsonResponse({'product_dict':product_dict}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=404)
