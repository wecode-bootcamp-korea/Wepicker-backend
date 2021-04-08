import re
import jwt
import json
import bcrypt

from django.views     import View
from django.db        import transaction
from django.http      import JsonResponse

from .models          import User, Point
from decorator        import login_check
from my_settings      import SECRET_KEY, ALGORITHM


# 회원가입
class SignUpView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            regex     = re.compile(email_reg)

            if len(data['account']) < 5 or len(data['name']) < 1 or len(data['password']) < 8 or len(data['phone']) < 11 or not regex.match(data['email']):
                return JsonResponse({'message':'INVALID_FORMAT'}, status=400)
            if User.objects.filter(account=data['account']).exists() or User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=400)

            User(
                account       = data['account'],
                password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name          = data['name'],
                phone         = data['phone'],
                email         = data['email'],
                profile_photo = data.get('profile_photo')
            ).save()

            Point(
                user    = User.objects.get(account=data['account']),
                content = '신규회원 쇼핑 지원금',
                point   = 1000
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=201)            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

# 로그인
class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(account=data['account']).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)

            user = User.objects.get(account=data['account'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'token':token}, status=200)
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)