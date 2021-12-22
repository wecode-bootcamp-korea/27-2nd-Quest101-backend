import json, boto3, uuid

from enum import Enum

from django.db.models.query_utils import Q
from django.http                  import JsonResponse
from django.views                 import View
from django.db                    import transaction
from requests.sessions            import Request
from core.utils                   import Authorize

from products.models   import *
from users.models      import *
from quest101.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION

class CourseStatusEnum(Enum):
    PENDING   = "클래스 준비"
    RUNNING   = "클래스 운영"
    REVIEWING = "클래스 검토중"

class ImageHandler:
    def __init__(self, client, bucket, region):
        self.client = client
        self.bucket = bucket
        self.region = region

    def upload_file(self, file):
        unique_key = str(uuid.uuid4())

        self.client.put_object(
            Bucket      = self.bucket,
            Key         = unique_key,
            Body        = file.file.read(),
            ContentType = file.content_type
        )

        return '%s.s3.%s.amazonaws.com/%s' % (self.bucket, self.region, unique_key)

    def upload_files(self, files):
        return [self.upload_file(file) for file in files]
    
boto3_client = boto3.client(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)
    
image_handler = ImageHandler(boto3_client, AWS_STORAGE_BUCKET_NAME, AWS_REGION)

class CoursesView(View):
    @Authorize
    def get(self, request):
        courses = request.user.course_set.all()
        stat = CourseStat.objects.all()

        results = [{
            'id'                  : course.id,
            'name'                : course.name,
            'thumbnail_image_url' : course.thumbnail_image_url,
            'detail_media'        : [{'type' : image.type,
                                     'url':image.url} for image in course.media_set.all()],
            'description'         : course.description,
            'sub_category'        : course.sub_category.name if course.sub_category != None else None,
            'category'            : course.sub_category.category.name 
                                    if course.sub_category != None 
                                    else None,
            "healthStat"          : CourseStat.objects.get(course=course, stat__name="체력").score,
            "intellectStat"       : CourseStat.objects.get(course=course, stat__name="지능").score,
            "charmStat"           : CourseStat.objects.get(course=course, stat__name="매력").score,
            "artStat"             : CourseStat.objects.get(course=course, stat__name="예술").score,
            'status'              : course.course_status.status,
            'level'               : course.level.level if course.level != None else None ,
            'user_name'           : request.user.name,
            'user_profile_image'  : request.user.profile_image,
            'user_phone_number'   : request.user.phone_number,
            'user_description'    : request.user.description,
            'social_account'      : [{
                'channel' :social_account.channel, 
                'url' : social_account.url
            } for social_account in course.user.socialaccount_set.all()]
        } for course in courses]
        
        return JsonResponse({"results" : results}, status=200)
    
    @Authorize
    def post(self, request):
        try:
            formdata   = request.POST
            print(request.POST)
            print(formdata)
            user                = request.user
            course              = Course.objects.get(id=request.POST['course_id'], user=user)
            course.name         = formdata['course_name']
            course.description  = formdata['course_description']
            course.subcategory  = SubCategory.objects.get(name=formdata['sub_category'])
            course.category     = Category.objects.get(name=formdata['category'])
            course.level        = Level.objects.get(level=formdata['level'])
            course.coursestatus = formdata['status']
            user.profile_image  = User.objects.get(id=request.user.id).profile_image
            user.name           = formdata['user_name']
            user.description    = formdata['user_description']
            user.phone_number   = formdata['user_phone_number']

            social_account, created = SocialAccount.objects.get_or_create(channel = formdata['channel'], user = request.user)
            social_account.url      = formdata['url']

            course.save()
            user.save()
            
            stats_set = {
                "체력" : formdata.get('healthStat', 0),
                "지능" : formdata.get('intellectStat', 0),
                "매력" : formdata.get('charmStat', 0),
                "예술" : formdata.get('artStat', 0)
            }
            
            [course.coursestat_set.filter(stat__name=key) for key in stats_set]
            [course.coursestat_set.filter(stat__name=key).update(score=stats_set[key]) for key in stats_set]
            
            return JsonResponse({"message": "SUCCESS"}, status = 201)
        
        except Course.DoesNotExist:
            return JsonResponse({"message": "INVALID_COURSE"}, status = 404)
    
    @Authorize
    @transaction.atomic()
    def delete(self, request):
        try:
            user         = request.user
            data         = json.loads(request.body)
            course       = Course.objects.get(id = data['course_id'], user = user)
            course_stats = CourseStat.objects.filter(course=course)

            if not Course.objects.filter(id = data['course_id'], user = user).exists():
                return JsonResponse({"message" : "NOT_EXIST"}, status=400)
            
            course.delete()
            [course_stat.delete() for course_stat in course_stats]

            return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)
        
        except Course.DoesNotExist:
            return JsonResponse({"message" : "INVALID_COURSE"}, status=404)

    @Authorize
    @transaction.atomic()
    def put(self,request):
        course = Course.objects.create(user = request.user, 
                                        course_status=CourseStatus.objects.get(status=CourseStatusEnum.PENDING.value))
        stats  = Stat.objects.all()
        
        course_stats = [CourseStat(
            course = course,
            stat   = stat,
            score  = 0
        ) for stat in stats]
                
        CourseStat.objects.bulk_create(course_stats)
        
        if not request.user.is_creator:
            request.user.is_creator = True
            request.user.save()
            
        return JsonResponse({"courseId": course.id}, status = 201)

class CourseView(View):
    @Authorize
    def get(self, request, course_id):
        course = Course.objects.get(id = course_id, user_id = request.user.id)

        results = {
            'name'                : course.name,
            'thumbnail_image_url' : course.thumbnail_image_url,
            'detail_media'        : [{'type' : image.type,
                                     'url':image.url} for image in course.media_set.all()],
            'description'         : course.description,
            'sub_category'        : course.sub_category.name if course.sub_category != None else None,
            'category'            : course.sub_category.category.name 
                                    if course.sub_category != None 
                                    else None,
            'level'               : course.level.level if course.level != None else None ,
            'is_course_created'   : False,
            'user_name'           : course.user.name,
            'user_profile_image'  : course.user.profile_image,
            'user_phone_number'   : course.user.phone_number,
            'user_description'    : course.user.description,
            'social_account'      : [{
                'channel' : social_account.channel,
                'url'     : social_account.url
            } for social_account in course.user.socialaccount_set.all()]
        }
        
        return JsonResponse({"results" : results}, status=200)
    
    @Authorize
    @transaction.atomic()
    def post(self,request, course_id):
        try:
            print(request.FILES)
            course = Course.objects.create(
                user                = request.user,
                thumbnail_image_url = image_handler.upload_file(request.FILES.__getitem__('thumbnail_image')),
                course_status = CourseStatus.objects.get(status=CourseStatusEnum.PENDING.value)
            )
            urls = image_handler.upload_files(request.FILES.getlist('detail_image'))
            Media.objects.bulk_create([Media(type = 'image', course = course, url = url) for url in urls])
            return JsonResponse({"MESSAGE":"SUCCESS"},status=201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)