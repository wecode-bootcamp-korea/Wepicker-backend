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
            max_page     = math.ceil(Product.objects.all().count()/9)

            if page > max_page:
                page = 2
            if page < 1:
                page = 1

            limit        = 9 * page
            offset       = limit - 9
            categories   = Category.objects.all()
            ordering     = request.GET.get('ordering')
            category     = request.GET.get('category')
            product_list = []

            sort_type = {
                'min_price' : 'price',
                'max_price' : '-price',
                'abc'       : 'name',
                'descabc'   : '-name' 
            }
            category_type = {
                'living' : 1,
                'kitchen': 2
            }

            if category is not None:
                if ordering is not None:
                    products = Product.objects.filter(category_type[category]).order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
                else:
                    products = Product.objects.filter(category_type[category]).order_by('pub_date').prefetch_related('image_url')[offset:limit]
                if ordering == 'best':
                    products = Product.objects.filter(category_type[category]).annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]

            if ordering is not None and ordering != 'best':
                products = Product.objects.order_by(sort_type[ordering]).prefetch_related('image_url')[offset:limit]
            else:
                products = Product.objects.order_by('pub_date').prefetch_related('image_url')[offset:limit]
                
            if ordering == 'best':
                products = Product.objects.annotate(Count('review')).order_by('-review__count').prefetch_related('image_url')[offset:limit]
            
            for product in products:
                image = product.image_url
                product_dict = {
                    'category'       : product.category.category,
                    'name'           : product.name,
                    'price'          : product.price,
                    'description'    : product.description,
                    'thumnail_image' : image.first().image_url,
                    'sub_image'      : image.all()[1].image_url,
                    'pub_date'       : product.pub_date
                }
                product_list.append(product_dict)

            return JsonResponse({'product_list':product_list}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=404)
