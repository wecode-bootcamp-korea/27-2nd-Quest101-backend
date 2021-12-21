import jwt,requests

from quest101.settings import SECRET_KEY, ALGORITHM

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import F, Sum
from datetime          import datetime, timedelta
from core.utils        import Authorize, AuthorizeProduct

from users.models      import User, UserCourse

from django.views      import View
from django.http       import JsonResponse

from products.models   import Like

class KakaoAPI:
    def __init__(self, access_token):
        self.kakao_token = access_token
        self.kakao_url = 'https://kapi.kakao.com/v2/user/me'

    def get_kakao_user(self):
        kakao_headers = {'Authorization' : f'Bearer {self.kakao_token}'}
        response = requests.get(self.kakao_url, headers=kakao_headers, timeout = 5)
    
        if not response.status_code == 200:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=400)
        
        if response.status_code == -401:
                return JsonResponse({'message': 'INVALID KAKAO USER'}, status=400)
            
        return response.json()

class KakaoSignInView(View):
    def get(self, request):
        try:
            kakao_token = request.headers.get('Authorization', None)
            kakao_api   = KakaoAPI(kakao_token)
            kakao_user  = kakao_api.get_kakao_user()
            
            kakao_id      = kakao_user['id']
            name          = kakao_user['kakao_account']['profile']['nickname']
            email         = kakao_user['kakao_account']['email']
            profile_image = kakao_user['kakao_account']['profile']['thumbnail_image_url']
            
            user, created = User.objects.get_or_create(
                kakao_id = kakao_id,
                dafaults = {'name'          : name,
                            'email'         : email,
                            'profile_image' : profile_image
                        }
            )
            
            status_code  = 201 if created else 200
        
            access_token = jwt.encode({'user_id' : user.id, 'exp' : datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'message':'SUCCESS', 'access_token' : access_token}, status = status_code)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 404)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'TOKEN_EXPIRED'}, status = 400)


class MypageView(View):
    @AuthorizeProduct
    def get(self,request):
        try:
            print(request)
            user = request.user
            print(user)
            user_get = User.objects.get(id=2)
            user_id = User.objects.filter(id=user.id)
            stats_all = user_id.annotate(
                score     = F('usercoursestat__course_stat__score'),
                stat_name = F('usercoursestat__course_stat__stat__name')
                )
            stats         = stats_all.values('stat_name').annotate(stat = Sum('score'))
            
            mypage = [{ # 찜, 좋아요, 스탯
                'user_stat' :{
                    'stat' : list(stats)
                },
                'like_course'           : [{
                    'like_name'             : like.course.name,
                    'like_description'      : like.course.description,
                    'like_price'            : like.course.price,
                    'like_period'           : like.course.payment_period,
                    'like_thumbnail'        : like.course.thumbnail_image_url,
                    'like_user_name'        : like.course.user.name,
                    'like_like'             : Like.objects.filter(course_id=like.course.id).count(),
                }for like in user_get.like_set.all()
                ],
                'running_course'        : [{
                    'running_name'          : running.course.name,
                    'running_description'   : running.course.description,
                    'running_price'         : running.course.price,
                    'running_period'        : running.course.payment_period,
                    'running_thumbnail'     : running.course.thumbnail_image_url,
                    'running_user_name'     : running.course.user.name,
                    'running_like'          : UserCourse.objects.filter(course_id=running.course.id).count(),
                }for running in user_get.usercourse_set.all()
                ]
            }]

            return JsonResponse({'result':mypage},status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=401)