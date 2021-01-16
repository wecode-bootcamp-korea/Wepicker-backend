import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY
from user.models import User


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token      = request.headers.get('Authorization')
            user_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')

            setattr(request, 'user', User.objects.get(id=user_token['id']))
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
            
        return func(self, request, *args, **kwargs)
    return wrapper