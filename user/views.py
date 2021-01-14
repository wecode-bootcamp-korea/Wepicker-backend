import jwt
import json
import bcrypt

from django.shortcuts import render
from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse, HttpResponse

from django.core.validators import MinLengthValidator

from .models          import User, Point
from decorator        import login_check
from my_settings      import SECRET_KEY

# 회원가입
class SignUpView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data            = json.loads(request.body)
            password        = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            account         = data['account']
            name            = data['name']
            phone           = data['phone']
        

            if len(account) < 5 or len(name) < 1 or len(password) < 8 or len(phone) < 11:
                return HttpResponse('형식 오류', status=400) 
            if User.objects.filter(account=data['account']).exists() or User.objects.filter(email=data['email']).exists():
                return HttpResponse('이미 가입된 계정', status=400)
            if '@' and '.com' not in data['email']:
                return HttpResponse('이메일 형식 오류', status=400)

            User(
                account       = account,
                password      = hashed_password,
                name          = name,
                phone         = phone,
                email         = data['email'],
                profile_photo = data.get('profile_photo')
            ).save()

            Point(
                user    = User.objects.get(account=data['account']),
                content = '신규회원 쇼핑 지원금',
                point   = 1000
            ).save()

            return HttpResponse('Success', status=201)
        except KeyError:
            return HttpResponse('Key_Error', status=400)
