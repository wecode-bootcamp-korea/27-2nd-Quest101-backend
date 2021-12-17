import json, jwt

from django.test        import TestCase, Client

from .models            import Course, SubCategory, Like, Media, Stat, CourseStat, Category , Level
from  users.models      import User
from  quest101.settings import SECRET_KEY, ALGORITHM

class ProductTest(TestCase):
    
    def setUp(self):
        
        User.objects.create(
            id   = 1,
            name = "bear",
            kakao_id = 484248,
            profile_image = "myimage123.com"
        )
        
        User.objects.create(
            id= 2,
            name = "tiger",
            kakao_id = 879845,
            profile_image = "myprofile123.com"
        )
        
        Category.objects.create(
            id =1,
            name = "category1"
        )

        Category.objects.create(
            id = 2,
            name = "category2"
        )

        SubCategory.objects.create(
            id=1,
            name = "sports",
            category_id = 2
        )

        SubCategory.objects.create(
            id=2,
            name = "cook",
            category_id = 1
        )

        Level.objects.create(
            id =1,
            level = "초급"
        )

        Level.objects.create(
            id =2,
            level = "중급"
        )

        Course.objects.create(
            id = 1,
            thumbnail_image_url='ewrrwaa.com',
            name = "Enjoy korean food",
            price = 30000,
            start_date = "2021-12-16",
            end_date = "2021-12-16",
            payment_period = 5,
            level_id = 1,
            user_id = 2,
            sub_category_id = 1,
            discount_rate = 30,
            description = "abcd"
        )

        Course.objects.create(
            id = 2,
            thumbnail_image_url="sjflafj.com",
            name = "Enjoy Sports",
            price = 50000,
            start_date = "2021-12-16",
            end_date = "2021-12-16",
            payment_period = 3,
            level_id=2,
            user_id=1,
            sub_category_id = 2,
            discount_rate = 20,
            description = "efgh"
        )

        Media.objects.create(
            id = 1,
            url = "abc.com",
            course_id = 2
        )

        Media.objects.create(
            id = 2,
            url = "def.com",
            course_id = 1
        )

        Like.objects.create(
            id = 1,
            course_id = 1,
            user_id = 2
        )

        Like.objects.create(
            id = 2,
            course_id = 2,
            user_id = 1
        )

        Stat.objects.create(
            id = 1,
            name = "wisdom"
        )

        Stat.objects.create(
            id = 2,
            name = "strength"
        )

        CourseStat.objects.create(
            id = 1,
            stat_id = 1,
            course_id = 2,
            score = 50
        )        
        
        CourseStat.objects.create(
            id = 2,
            stat_id = 2,
            course_id = 1,
            score = 70
        )
        global headers
        token = jwt.encode({'user': 2}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization" : token}

    def tearDown(self):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Media.objects.all().delete()
        Like.objects.all().delete()
        Stat.objects.all().delete()
        CourseStat.objects.all().delete()
    
    def test_productview_get_suceess(self):
        client=Client()
        response = client.get('/products/detail/1', **headers)
        self.maxDiff = None
        
        self.assertEqual(response.json(),
            {'results' : {
                "course_id"      : 1,
                "sub_category"   : "sports",
                "course_name"    : "Enjoy korean food",
                "thumbnail_url"  : "ewrrwaa.com",
                "page_image"     : "def.com",
                "course_level"   : "초급",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : 30,
                "discount_price" : "9000.00",
                "course_like"    : 1,
                "course_stat"    : [{"stat_name" : "strength", "score" : 70}],
                "is_like_True"   : True,
                "user_name"      : "tiger",
                "profile_image"  : "myprofile123.com",
                "description"    : "abcd"
                }
            }    
        )
      
        self.assertEqual(response.status_code,200) 
       
    def test_productview_get_doesnotexist(self):
        client=Client()
        response = client.get('/products/detail/3')

        self.assertEqual(response.json(),
            {"message" : "INVALID_COURSE"})
        
        self.assertEqual(response.status_code, 401)     

