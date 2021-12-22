import json, boto3, uuid

from enum import Enum

from django.http                  import JsonResponse
from django.views                 import View
from django.db                    import transaction
from requests.sessions            import Request
from core.utils                   import Authorize

from products.models   import Course, CourseStat, CourseStatus, SubCategory, Level, Media
from users.models      import User, SocialAccount
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
            "healthStat"          : 0 if not CourseStat.objects.filter(course=course, stat__name="체력").exists() else CourseStat.objects.get(course=course, stat__name="체력").score,
            "intellectStat"       : 0 if not CourseStat.objects.filter(course=course, stat__name="지능").exists() else CourseStat.objects.get(course=course, stat__name="지능").score,
            "charmStat"           : 0 if not CourseStat.objects.filter(course=course, stat__name="매력").exists() else CourseStat.objects.get(course=course, stat__name="매력").score,
            "artStat"             : 0 if not CourseStat.objects.filter(course=course, stat__name="예술").exists() else CourseStat.objects.get(course=course, stat__name="예술").score,
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
            print(request.POST)
            print(request)
            formdata   = request.POST
            user                = request.user
            course              = Course.objects.get(id=request.POST['course_id'], user=user)
            course.name         = formdata['course_name']
            course.description  = formdata['course_description']
            
            course.sub_category  = SubCategory.objects.get(name=formdata['sub_category']) if formdata['sub_category'] != 'null' else None
            course.level        = Level.objects.get(level=formdata['level']) if formdata['level'] != "0" else None
            course.coursestatus = formdata['status']
            
            print(dir(course))
            
            user.profile_image  = User.objects.get(id=request.user.id).profile_image
            user.name           = formdata['user_name']
            user.description    = formdata['user_description']
            user.phone_number   = formdata['user_phone_number']

            social_account, created = SocialAccount.objects.get_or_create(channel = formdata['channel'], user = request.user)
            social_account.url      = formdata['url']

            course.save()
            user.save()
            
            stats_set = {
                "체력" : int(formdata.get('healthStat', 0)),
                "지능" : int(formdata.get('intellectStat', 0)),
                "매력" : int(formdata.get('charmStat', 0)),
                "예술" : int(formdata.get('artStat', 0))
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
    def put(self,request):
        course = Course.objects.create(user = request.user, 
                                        course_status=CourseStatus.objects.get(status=CourseStatusEnum.PENDING.value))
        
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
            'detail_media'        : [{'type' : image.type, 'url':image.url} for image in course.media_set.all()],
            'description'         : course.description,
            'sub_category'        : course.sub_category.name if course.sub_category != None else None,
            'category'            : course.sub_category.category.name if course.sub_category != None else None,
            'level'               : course.level.level if course.level != None else None ,
            'is_course_created'   : False,
            'user_name'           : course.user.name,
            'user_profile_image'  : course.user.profile_image,
            'user_phone_number'   : course.user.phone_number,
            'user_description'    : course.user.description,
            "healthStat"          : 0 if not CourseStat.objects.filter(course=course, stat__name="체력").exists() else CourseStat.objects.get(course=course, stat__name="체력").score,
            "intellectStat"       : 0 if not CourseStat.objects.filter(course=course, stat__name="지능").exists() else CourseStat.objects.get(course=course, stat__name="지능").score,
            "charmStat"           : 0 if not CourseStat.objects.filter(course=course, stat__name="매력").exists() else CourseStat.objects.get(course=course, stat__name="매력").score,
            "artStat"             : 0 if not CourseStat.objects.filter(course=course, stat__name="예술").exists() else CourseStat.objects.get(course=course, stat__name="예술").score,
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
            course = Course.objects.get(user=request.user, id=course_id)
            urls = image_handler.upload_files(request.FILES.getlist('detail_image_url'))
            
            course.thumbnail_image_url = image_handler.upload_file(request.FILES.__getitem__('thumbnail_image_url'))
            course.save()
        
            Media.objects.bulk_create([Media(type = 'image', course = course, url = url) for url in urls])
            return JsonResponse({"MESSAGE":"SUCCESS"},status=201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)