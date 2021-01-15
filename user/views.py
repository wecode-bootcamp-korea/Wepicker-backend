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
            profile_photo   = data.get('profile_photo')
            email_reg       = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            regex           = re.compile(email_reg)

            if len(account) < 5 or len(name) < 1 or len(password) < 8 or len(phone) < 11 or not regex.match(data['email']):
                return JsonResponse({'message':'INVALID_FORMAT'}, status=400)
            if User.objects.filter(account=data['account']).exists() or User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=400)
            if len(profile_photo) == 0:
                profile_photo = None

            User(
                account       = account,
                password      = hashed_password,
                name          = name,
                phone         = phone,
                email         = data['email'],
                profile_photo = profile_photo
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
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password'] 

            if not User.objects.filter(account=account).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=400)

            user           = User.objects.get(account=account)
            password_check = user.password

            if bcrypt.checkpw(password.encode('utf-8'), password_check.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                return JsonResponse({'token':token}, status=200)
            else:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KET_ERROR'}, status=400)