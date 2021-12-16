import json, jwt

from django.test       import TestCase, Client
from django.db.models  import Q

from .models           import Course, Category, SubCategory, Like, Level, CourseStat, Stat
from users.models      import User
from quest101.settings import SECRET_KEY,ALGORITHM 

class ProductListTest(TestCase):
    def setUp(self):

        User.objects.bulk_create([
            User(
                id   = 1,
                name = "user1",
                kakao_id = 484248),
            User(
                id= 2,
                name = "user2",
                kakao_id = 879845
            )    
        ])
        
        Category.objects.bulk_create([
            Category(
                id =1,
                name = "category1"),
            Category(
                id = 2,
                name = "category2"
            )    
        ])

        SubCategory.objects.bulk_create([
            SubCategory(
                id=1,
                name = "sub1",
                category_id = 2),
            SubCategory(
                id=2,
                name = "sub2",
                category_id = 1),
            SubCategory(
                id=3,
                name = "sub3",
                category_id= 1)        
        ])


        Level.objects.bulk_create([
            Level(
                id =1,
                level = "초급"),
            Level(
                id =2,
                level = "중급")     
        ])

        Course.objects.bulk_create([
            Course(
                id = 1,
                thumbnail_image_url='ewrrwaa.com',
                name = "Enjoy korean food",
                price = 30000,
                start_date = "2021-12-16",
                end_date = "2022-12-16",
                payment_period = 5,
                level_id = 1,
                user_id = 2,
                sub_category_id = 2),
            Course(
                id = 2,
                thumbnail_image_url="sjflafj.com",
                name = "Enjoy Sports",
                price = 30000,
                start_date = "2021-12-16",
                end_date = "2022-12-16",
                payment_period = 3,
                level_id=2,
                user_id=1,
                sub_category_id = 2),
            Course(
                id = 3,
                thumbnail_image_url="unsplash123,com",
                name = "Enjoy drawing",
                price = 30000,
                start_date = "2021-12-16",
                end_date = "2022-12-16",
                payment_period = 3,
                level_id=2,
                user_id=1,
                sub_category_id = 1),
            Course(
                id = 4,
                    thumbnail_image_url="unsplash567,com",
                name = "Enjoy best_seller",
                price = 30000,
                start_date = "2021-12-16",
                end_date = "2022-12-16",
                payment_period = 5,
                level_id=2,
                user_id=2,
                sub_category_id = 1)    
            ])


        Like.objects.bulk_create([
            Like(
                id = 1,
                course_id = 1,
                user_id = 2),
            Like(
                id = 2,
                course_id = 3,
                user_id = 1),    
            ])

        Stat.objects.bulk_create([
            Stat(
                id = 1,
                name = "wisdom"),
            Stat(
                 id =2,
                name = "strength"),
            Stat(
                id = 3,
                name = "charm"),
            Stat(
                id = 4,
                name = "artistry")    
            ])

        CourseStat.objects.bulk_create([
            CourseStat(
                id = 1,
                course_id = 1,
                stat_id = 1,
                score = 50),
            CourseStat(
                id = 2,
                course_id = 2,
                stat_id = 2,
                score = 70),
            CourseStat(
                id = 3,
                course_id = 3,
                stat_id = 3,
                score = 80),
            CourseStat(
                id = 4,
                course_id = 4,
                stat_id = 4,
                score = 70)            
            ])  
 
        global headers
        token = jwt.encode({'user': 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization" : token}

    def tearDown(self):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Like.objects.all().delete()
        Stat.objects.all().delete()
        Level.objects.all().delete()
        CourseStat.objects.all().delete()

    
    def test_productlist_get_filter_category(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?category=category2', **headers)
        
        self.assertEqual(response.json(),
            {'results' : [{
                "course_id"      : 3,
                "thumbnail"      : "unsplash123,com",
                "user_name"      : "user1",
                "sub_category"   : "sub1",
                "course_name"    : "Enjoy drawing",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : True
                },
                {
                "course_id"      : 4,
                "thumbnail"      : "unsplash567,com",
                "user_name"      : "user2",
                "sub_category"   : "sub1",
                "course_name"    : "Enjoy best_seller",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
                }]
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_sub_category(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?sub_category=sub2', **headers)

        self.assertEqual(response.json(),
            {'results' : [{
                "course_id"      : 1,
                "thumbnail"      : "ewrrwaa.com",
                "user_name"      : "user2",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy korean food",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : False
                },
                {
                "course_id"      : 2,
                "thumbnail"      : "sjflafj.com",
                "user_name"      : "user1",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy Sports",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
                }]
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat_one(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?stat=wisdom', **headers)

        self.assertEqual(response.json(),
            {"results" : [
                    {
                    "course_id"      : 1,
                    "thumbnail"      : "ewrrwaa.com",
                    "user_name"      : "user2",
                    "sub_category"   : "sub2",
                    "course_name"    : "Enjoy korean food",
                    "price"          : "30000.00",
                    "payment_period" : 5,
                    "discount_rate"  : "30%",
                    "discount_price" : "10000.00",
                    "course_like"    : 1,
                    "is_like_True"   : False
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat1_2(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?stat=wisdom&stat=strength', **headers)

        self.assertEqual(response.json(),
            {'results' : [
                {
                "course_id"      : 2,
                "thumbnail"      : "sjflafj.com",
                "user_name"      : "user1",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy Sports",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
                },
                {
                "course_id"      : 1,
                "thumbnail"      : "ewrrwaa.com",
                "user_name"      : "user2",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy korean food",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : False
                }
              ]
            }
          )     

        self.assertEqual(response.status_code, 200)      

    def test_productlist_get_filter_stat1_2_3(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?stat=wisdom&stat=strength&stat=charm', **headers)

        self.assertEqual(response.json(),
            {'results' : [
                {
                "course_id"      : 3,
                "thumbnail"      : "unsplash123,com",
                "user_name"      : "user1",
                "sub_category"   : "sub1",
                "course_name"    : "Enjoy drawing",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : True
                },
                {
                "course_id"      : 2,
                "thumbnail"      : "sjflafj.com",
                "user_name"      : "user1",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy Sports",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
                },
                {
                "course_id"      : 1,
                "thumbnail"      : "ewrrwaa.com",
                "user_name"      : "user2",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy korean food",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : False
              }
            ]
          }
        )     

        self.assertEqual(response.status_code, 200)    

    def test_productlist_get_filter_stat_all(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?stat=wisdom&stat=strength&stat=charm&stat=artistry', **headers)

        self.assertEqual(response.json(),
            {'results' : [
                {
                "course_id"      : 1,
                "thumbnail"      : "ewrrwaa.com",
                "user_name"      : "user2",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy korean food",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : False
                },
                {
                "course_id"      : 2,
                "thumbnail"      : "sjflafj.com",
                "user_name"      : "user1",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy Sports",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
                },
                {
                "course_id"      : 3,
                "thumbnail"      : "unsplash123,com",
                "user_name"      : "user1",
                "sub_category"   : "sub1",
                "course_name"    : "Enjoy drawing",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 1,
                "is_like_True"   : True
                },
                {
                "course_id"      : 4,
                "thumbnail"      : "unsplash567,com",
                "user_name"      : "user2",
                "sub_category"   : "sub1",
                "course_name"    : "Enjoy best_seller",
                "price"          : "30000.00",
                "payment_period" : 5,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False
                }
              ]
            }
          )     

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_all(self):
        client=Client()
        self.maxDiff=None
        response = client.get('/products?category=category1&sub_category=sub2&stat=strength', **headers)     

        self.assertEqual(response.json(),
            {"results" : [{
                "course_id"      : 2,
                "thumbnail"      : "sjflafj.com",
                "user_name"      : "user1",
                "sub_category"   : "sub2",
                "course_name"    : "Enjoy Sports",
                "price"          : "30000.00",
                "payment_period" : 3,
                "discount_rate"  : "30%",
                "discount_price" : "10000.00",
                "course_like"    : 0,
                "is_like_True"   : False  
            }
          ]  
        }
      )

        self.assertEqual(response.status_code, 200)