import json, jwt

from django.views     import View
from django.http      import JsonResponse

from .models          import Course
from core.utils       import AuthorizeProduct

class ProductView(View):
    @AuthorizeProduct
    def get(self,request,course_id):
        try:
            course=Course.objects.get(id=course_id)
            stats=course.coursestat_set.all().select_related('stat')
            media = course.media_set.get()
            
            results={
                "course_id"      : course.id,
                "sub_category"   : course.sub_category.name,
                "course_name"    : course.name,
                "description"    : course.description,
                "thumbnail_url"  : course.thumbnail_image_url,
                "page_image"     : media.url,
                "course_level"   : course.level.level,
                "price"          : course.price,
                "payment_period" : course.payment_period,
                "discount_rate"  : course.discount_rate,
                "discount_price" : (course.price * course.discount_rate)/100,
                "course_like"    : course.like_set.count(),
                "course_stat"    : [{"stat_name" : c_stat.stat.name,"score" : c_stat.score} for c_stat in stats],
                "is_like_True"   : True if course.like_set.filter(user_id=request.user).exists() else False,
                "user_name"      : course.user.name,
                "profile_image"  : course.user.profile_image
               }
                

            return JsonResponse({"results" : results}, status=200)

        except Course.DoesNotExist:
            return JsonResponse({"message" : "INVALID_COURSE"},status=401)
