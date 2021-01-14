import re
import jwt
import json
import bcrypt

from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse, HttpResponse

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
            email_reg       = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            regex           = re.compile(email_reg)

            if len(account) < 5 or len(name) < 1 or len(password) < 8 or len(phone) < 11 or not regex.match(data['email']):
                return JsonResponse({'message':'형식 오류'}, status=400)
            if User.objects.filter(account=data['account']).exists() or User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'이미 존재하는 계정'}, status=400)

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

            return JsonResponse({'message':'Success'}, status=201)
        except KeyError:
            return JsonResponse({'message':'Key_Error'}, status=400)
