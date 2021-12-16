import json

from django.views     import View
from django.http      import JsonResponse
from django.db        import IntegrityError
from django.db.models import Q, F, Count, Exists

from .models          import Category, Course, Like, CourseStat
from users.models     import *
from core.utils       import AuthorizeProduct

class ProductListView(View):
    @AuthorizeProduct
    def get(self,request):
            category       = request.GET.get('category', None)
            sub_category   = request.GET.get('sub_category', None)
            stat           = request.GET.getlist('stat', None)
            like           = request.user.id
            my_course      = request.user.id
            # UserCourseStat.objects.filter(user_id = request.user.id)
            
            q=Q()

            if category:
                q &=Q(sub_category__category__name=category)
                
            if sub_category:
                q &=Q(sub_category__name=sub_category)
                
            if stat:
                q &=Q(coursestat__stat__name__in=stat)

            if like:                 
                q &=Q(like__user_id=like)

            if my_course:
                q &=Q(usercoursestat__user_id=my_course)
                # q &=Q(user__usercoursestat__course_stat__course__user_id=running_course)
                
            products = Course.objects.filter(q).distinct()

                # q = UserCourseStat.objects.get(Q(user_id=request.user.id) | Q(course_stat__course_id=running_course))
            # prefetch_related('like_set')
            
            results=[{  "course_id"      : product.id,
                        "thumbnail"      : product.thumbnail_image_url,
                        "user_name"      : product.user.name,
                        "sub_category"   : product.sub_category.name,
                        "course_name"    : product.name,
                        "price"          : product.price,
                        "payment_period" : product.payment_period,
                        "discount_rate"  : "30%",
                        "discount_price" : product.price / 3,
                        "course_like"    : product.like_set.count(),
                        "is_like_True"   : product.like_set.filter(user_id=request.user).exists(),
                        
                        } for product in products]
                
            return JsonResponse({"results" : results}, status=200)