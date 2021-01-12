import jwt
import json

from django.http import JsonResponse, HttpResponse

from my_settings import SECRET_KEY


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)
    return wrapper