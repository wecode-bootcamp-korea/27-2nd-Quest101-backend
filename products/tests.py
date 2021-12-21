<<<<<<< HEAD
<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
from django.http import response
import jwt,json

from datetime import datetime

from django.test import TestCase, Client
from requests.api import request
from quest101.settings import SECRET_KEY,ALGORITHM
from products.models import *
from users.models import *

class CommentTest(TestCase):
    def setUp(self):
        User.objects.create(
            id            = 1,
            name          = 'a', 
            profile_image = 'a',
            description   = 'a',
            kakao_id      = 1,
            is_creator    = False
        )
        User.objects.create(
            id          = 2,
            name        = 'b',
            description = 'b',
            kakao_id    = 2,
            is_creator  = True
        )
        Category.objects.create(
            id   = 1,
            name = 'a'
        )
        SubCategory.objects.create(
            id          = 1,
            name        = 'a1',
            category_id = 1
        )
        Level.objects.create(
            id    = 1,
            level = 'a'
        )
        Course.objects.create(
            id                  = 1,
            name                = 'a',
            thumbnail_image_url = 'a',
            description         = 'a',
            price               = 100,
            start_date          = datetime(2021,12,12,12,12,1),
            end_date            = datetime(2021,12,12,12,12,2),
            payment_period      = 1,
            user_id             = 2,
            sub_category_id     = 1,
            level_id            = 1
        )
        Course.objects.create(
            id                  = 2,
            name                = 'b',
            thumbnail_image_url = 'b',
            description         = 'b',
            price               = 100,
            start_date          = datetime(2021,12,12,12,12,1),
            end_date            = datetime(2021,12,12,12,12,2),
            payment_period      = 2,
            user_id             = 2,
            sub_category_id     = 1,
            level_id            = 1
        )
        Comment.objects.create(
            id         = 1,
            content    = 'a',
            user_id    = 1,
            course_id  = 1
        )
        Comment.objects.create(
            id         = 2,
            content    = 'b',
            user_id    = 1,
            course_id  = 1
        )
        self.token = jwt.encode({'user': 1}, SECRET_KEY,ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Level.objects.all().delete()
        Course.objects.all().delete()
        Comment.objects.all().delete()

    def test_comment_post_success(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        
        comment = {
            'course_id' : 2,
            'content'   : 'a'
        }
        result = [{
            'id'      : 3,
            'name'    : 'a',
            'content' : 'a',
        }]
        
        response = client.post('/products/comments/2',json.dumps(comment),**header, content_type='application/json')
        self.assertEqual(response.json(), {'message':result})
        self.assertEqual(response.status_code, 200)

    def test_comment_post_key_error(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        
        comment = {
        }
        
        response = client.post('/products/comments/1',json.dumps(comment),**header, content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
        self.assertEqual(response.status_code, 401)

    def test_comment_get_success(self): # comment get success
        client = Client()
        response = client.get('/products/comments/1')
        course_comments = [
            {
                'id'      : 1,
                'name'    : 'a',
                'content' : 'a'
            },
            {
                'id'      : 2,
                'name'    : 'a',
                'content' : 'b'
            }
            ]
        self.assertEqual(response.json(),{'result':course_comments})
        self.assertEqual(response.status_code, 200)

    def test_comment_delete_success(self): 
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        body = {
            'comment_id' : 1
        }

        response = client.delete('/products/comments/1',json.dumps(body),**header)
        self.assertEqual(response.json(),{'message':'SUCCESS_DELETE'})
        self.assertEqual(response.status_code, 200)

    def test_comment_delete_does_not_exist(self): 
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        body = {
            'comment_id' : 3
        }

        response = client.delete('/products/comments/1',json.dumps(body),**header)
        self.assertEqual(response.json(),{'message':'INVAILD_COMMENT'})
        self.assertEqual(response.status_code, 401)
>>>>>>> 02cdcd9 ([Modify] CommentView Add CommentView unittest)
=======
# import jwt,json

# from datetime import datetime

# from django.test import TestCase, Client
# from quest101.settings import SECRET_KEY,ALGORITHM
# from products.models import *
# from users.models import *

# class CommentTest(TestCase):
#     def setUp(self):
#         User.objects.create(
#             id            = 1,
#             name          = 'a', 
#             profile_image = 'a',
#             description   = 'a',
#             kakao_id      = 1,
#             is_creator    = False
#         )
#         User.objects.create(
#             id          = 2,
#             name        = 'b',
#             description = 'b',
#             kakao_id    = 2,
#             is_creator  = True
#         )
#         Category.objects.create(
#             id   = 1,
#             name = 'a'
#         )
#         SubCategory.objects.create(
#             id          = 1,
#             name        = 'a1',
#             category_id = 1
#         )
#         Level.objects.create(
#             id    = 1,
#             level = 'a'
#         )
#         Course.objects.create(
#             id                  = 1,
#             name                = 'a',
#             thumbnail_image_url = 'a',
#             description         = 'a',
#             price               = 100,
#             start_date          = datetime(2021,6,1),
#             end_date            = datetime(2021,12,1),
#             payment_period      = 1,
#             user_id             = 2,
#             sub_category_id     = 1,
#             level_id            = 1
#         )
#         Course.objects.create(
#             id                  = 2,
#             name                = 'b',
#             thumbnail_image_url = 'b',
#             description         = 'b',
#             price               = 100,
#             start_date          = datetime(2021,6,1),
#             end_date            = datetime(2021,12,1),
#             payment_period      = 2,
#             user_id             = 2,
#             sub_category_id     = 1,
#             level_id            = 1
#         )
#         Comment.objects.create(
#             id         = 1,
#             content    = 'a',
#             user_id    = 1,
#             course_id  = 1
#         )
#         Comment.objects.create(
#             id         = 2,
#             content    = 'b',
#             user_id    = 1,
#             course_id  = 1
#         )
#         self.token = jwt.encode({'user': 1}, SECRET_KEY,ALGORITHM)

#     def tearDown(self):
#         User.objects.all().delete()
#         Category.objects.all().delete()
#         SubCategory.objects.all().delete()
#         Level.objects.all().delete()
#         Course.objects.all().delete()
#         Comment.objects.all().delete()

#     def test_comment_post_success(self): # comment post success
#         client = Client()
#         header = {"HTTP_Authorization" : self.token}
        
#         comment = {
#             'user_id'   : 1,
#             'course_id' : 1,
#             'content'   : 'a'
#         }
        
#         response = client.post('/products/comments/1',json.dumps(comment),**header, content_type='application/json')
#         self.assertEqual(response.json(), {'message':'SUCCESS'})
#         self.assertEqual(response.status_code, 200)

#     # =============================================================================================================
#     def test_comment_get_success(self): # comment get success
#         client = Client()
#         response = client.get('/products/comments/1')
#         course_comments = [
#             {
#                 'name'   : 'a',
#                 'content' : 'a'
#             },
#             {
#                 'name'   : 'a',
#                 'content' : 'b'
#             }
#             ]
#         self.assertEqual(response.json(),{'result':course_comments})
#         self.assertEqual(response.status_code, 200)

# #     def test_comment_get_invaild_key(self): # comment get invaild key
# #         client = Client()
# #         response = client.get('/products/comments/1')
# #         course_comments = {[
# #             {
# #                 'name'   : 'client1',
# #                 'content' : '댓글1'
# #             },
# #             {
# #                 'name'   : 'client2',
# #                 'content' : '댓글2'
# #             }
# #             ]}
# #         self.assertEqual(response.json(),{course_comments})
# #         self.assertEqual(response.status_code, 401)
# #         # =============================================================================================================

# #     def test_comment_delete_success(self): # comment get invaild key
#         # client = Client()
#         # header = {"HTTP_Authorization" : self.token}
#         # token = header['HTTP_Authorization']
#         # payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
#         # user         = User.objects.get(id = payload['user'])#         response = client.delete('/products/comments/1')
# #         comment_id = client.comment_id
# #         Comment.objects.get(id=comment_id)

# #         self.assertEqual(response.json(),{'message':'SUCCESS_DELETE'})
# #         self.assertEqual(response.status_code, 401)

#         # ============================================================================================================= Mypage test
# class CommentTest(TestCase):
#     def setUp(self):
#         User.objects.create(
#             id            = 1,
#             name          = 'client1',
#             phone_number  = '01012341234',
#             profile_image = 'jaemoon.url',
#             description   = 'jaemoon.desciption',
#             kakao_id      = '1',
#             is_creator    = False
#         )
#         User.objects.create(
#             id          = 2,
#             name        = 'creator',
#             description = 'creator.des',
#             kakao_id    = '2',
#             is_creator  = True
#         )
#         User.objects.create(
#             id          = 3,
#             name        = 'client2',
#             description = 'client.des2',
#             kakao_id    = '3'
#         )
#         User.objects.create(
#             id          = 4,
#             name        = 'creator2',
#             description = 'creator.des3',
#             kakao_id    = '4',
#             is_creator  = True
#         )
#         Category.objects.create(
#             id   = 1,
#             name = '운동'
#         )
#         Category.objects.create(
#             id   = 2,
#             name = '언어'
#         )
#         SubCategory.objects.create(
#             id   = 1,
#             name = 'sub1',
#             category = Category.objects.get(id=1)
#         )
#         SubCategory.objects.create(
#             id   = 2,
#             name = 'sub2',
#             category = Category.objects.get(id=2)
#         )
#         Level.objects.create(
#             id    = 1,
#             level = '고급'
#         )
#         Level.objects.create(
#             id    = 2,
#             level = '초급'
#         )
#         Course.objects.create(
#             id                  = 1,
#             name                = '코스1',
#             thumbnail_image_url = 'thumbnail1',
#             description         = 'des1',
#             price               = 12312300,
#             start_date          = datetime(2021,6,1),
#             end_date            = datetime(2021,12,1),
#             payment_period      = 5,
#             user                = User.objects.get(id=2),
#             sub_category        = SubCategory.objects.get(id=1),
#             level               = Level.objects.get(id=1)
#         )
#         Course.objects.create(
#             id                  = 2,
#             name                = '코스2',
#             thumbnail_image_url = 'thumbnail2',
#             description         = 'des2',
#             price               = 10000,
#             start_date          = datetime(2021,6,1),
#             end_date            = datetime(2021,12,1),
#             payment_period      = 5,
#             user                = User.objects.get(id=4),
#             sub_category        = SubCategory.objects.get(id=1),
#             level               = Level.objects.get(id=2)
#         )
#         Course.objects.create(
#             id                  = 3,
#             name                = '코스3',
#             thumbnail_image_url = 'thumbnail3',
#             description         = 'des3',
#             price               = 10000,
#             start_date          = datetime(2021,6,1),
#             end_date            = datetime(2021,12,1),
#             payment_period      = 5,
#             user                = User.objects.get(id=4),
#             sub_category        = SubCategory.objects.get(id=1),
#             level               = Level.objects.get(id=2)
#         )
#         Stat.objects.create(
#             id   = 1,
#             name = '체력'
#         )
#         Stat.objects.create(
#             id   = 2,
#             name = '지능'
#         )
#         Stat.objects.create(
#             id   = 3,
#             name = '예술'
#         )
#         Stat.objects.create(
#             id   = 4,
#             name = '매력'
#         )
#         CourseStat.objects.create(
#             id = 1,
#             course = Course.objects.get(id=1),
#             stat = Stat.objects.get(id=1),
#             score =  0
#         )
#         CourseStat.objects.create(
#             id = 2,
#             course = Course.objects.get(id=1),
#             stat = Stat.objects.get(id=2),
#             score =  1
#         )
#         CourseStat.objects.create(
#             id = 3,
#             course = Course.objects.get(id=1),
#             stat = Stat.objects.get(id=3),
#             score =  3
#         )
#         CourseStat.objects.create(
#             id = 4,
#             course = Course.objects.get(id=1),
#             stat = Stat.objects.get(id=4),
#             score =  0
#         )
#         CourseStat.objects.create(
#             id = 5,
#             course = Course.objects.get(id=2),
#             stat = Stat.objects.get(id=1),
#             score =  1
#         )
#         CourseStat.objects.create(
#             id = 6,
#             course = Course.objects.get(id=2),
#             stat = Stat.objects.get(id=2),
#             score =  2
#         )
#         CourseStat.objects.create(
#             id = 7,
#             course = Course.objects.get(id=2),
#             stat = Stat.objects.get(id=3),
#             score =  4
#         )
#         CourseStat.objects.create(
#             id = 8,
#             course = Course.objects.get(id=2),
#             stat = Stat.objects.get(id=4),
#             score =  1
#         )
#         CourseStat.objects.create(
#             id = 9,
#             course = Course.objects.get(id=3),
#             stat = Stat.objects.get(id=3),
#             score =  4
#         )
#         CourseStat.objects.create(
#             id = 10,
#             course = Course.objects.get(id=3),
#             stat = Stat.objects.get(id=4),
#             score =  1
#         )
#         UserCourseStat.objects.create(
#             id = 1,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=1)
#         )
#         UserCourseStat.objects.create(
#             id = 2,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=2)
#         )
#         UserCourseStat.objects.create(
#             id = 3,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=3)
#         )
#         UserCourseStat.objects.create(
#             id = 4,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=4)
#         )
#         UserCourseStat.objects.create(
#             id = 9,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=9)
#         )
#         UserCourseStat.objects.create(
#             id = 10,
#             user = User.objects.get(id=1),
#             CourseStat = CourseStat.objects.get(id=10)
#         )
#         UserCourseStat.objects.create(
#             id = 5,
#             user = User.objects.get(id=2),
#             CourseStat = CourseStat.objects.get(id=5)
#         )
#         UserCourseStat.objects.create(
#             id = 6,
#             user = User.objects.get(id=2),
#             CourseStat = CourseStat.objects.get(id=6)
#         )
#         UserCourseStat.objects.create(
#             id = 7,
#             user = User.objects.get(id=2),
#             CourseStat = CourseStat.objects.get(id=7)
#         )
#         UserCourseStat.objects.create(
#             id = 8,
#             user = User.objects.get(id=2),
#             CourseStat = CourseStat.objects.get(id=8)
#         )
#         Like.objects.create(
#             id = 1,
#             user = User.objects.get(id=1),
#             course = Course.object.get(id=1)
#         )
#         Like.objects.create(
#             id = 2,
#             user = User.objects.get(id=3),
#             course = Course.object.get(id=2)
#         )
#         UserCourse.objects.create(
#             id =1,
#             user = User.objects.get(id=1),
#             course = Course.objects.get(id=2)
#         )
#         UserCourse.objects.create(
#             id =2,
#             user = User.objects.get(id=3),
#             course = Course.objects.get(id=1)
#         )
#         UserCourse.objects.create(
#             id =3,
#             user = User.objects.get(id=3),
#             course = Course.objects.get(id=3)
#         )

#         self.token = jwt.encode({'user_id':User.objects.get(id=1).id}, SECRET_KEY,ALGORITHM)
#         print(self.token)

#     def tearDown(self):
#         User.objects.all().delete()
#         Category.objects.all().delete()
#         SubCategory.objects.all().delete()
#         Level.objects.all().delete()
#         Course.objects.all().delete()
#         Stat.objects.all().delete()
#         CourseStat.objects.all().delete()
#         UserCourse.objects.all().delete()
#         UserCourseStat.objects.all().delete()
#         Like.objects.all().delete()

#     def test_mypage_get_success(self):
#         client = Client()

#         response = client.get('/users/mypage/')
#         header = {'HTTP_Authorization' : self.token}
#         token = header['HTTP_Authorization']
#         print(token)
#         payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
#         mypage = {
#             'user_stat': {
#                 'stat': [
#                     {
#                         'stat_name': '체력',
#                         'stat': 0
#                     },
#                     {
#                         'stat_name': '지능',
#                         'stat': 1
#                     },
#                     {
#                         'stat_name': '예슬',
#                         'stat': 3
#                     },
#                     {
#                         'stat_name': '매력',
#                         'stat': 0
#                     }
#                 ]
#             },
#             'like_course': [
#                 {
#                     'like_name': '코스1',
#                     'like_description': 'des1',
#                     'like_price': 12312300,
#                     'like_period': 5,
#                     'like_thumbnail': 'thumbnail1',
#                     'like_user_name': 'creator',
#                     'like_like': 1
#                 }
#             ],
#             'running_course': [
#                 {
#                     'running_name': '코스1',
#                     'running_description': 'des1',
#                     'running_price': 12312300,
#                     'running_period': 5,
#                     'running_thumbnail': 'thumbnail1',
#                     'running_user_name': 'creator',
#                     'running_like': 1
#                 }
#             ]
#         }
#         self.assertEqual(response.json(),{'result':mypage})
#         self.assertEqual(response.status_code, 200)

#     def test_mypage_get_invaild_key(self):
#         client = Client()
#         response = client.get('/users/mypage/')
#         header = {'HTTP_Authorization' : self.token}
#         token = header['HTTP_Authorization']
#         payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
#         mypage = {
#             'user_stat1': {
#                 'stat': [
#                     {
#                         'stat_name': '체력',
#                         'stat': 0
#                     },
#                     {
#                         'stat_name': '지능',
#                         'stat': 1
#                     },
#                     {
#                         'stat_name': '예슬',
#                         'stat': 3
#                     },
#                     {
#                         'stat_name': '매력',
#                         'stat': 0
#                     }
#                 ]
#             },
#             'like_course': [
#                 {
#                     'like_name': '코스1',
#                     'like_description': 'des1',
#                     'like_price': 12312300,
#                     'like_period': 5,
#                     'like_thumbnail': 'thumbnail1',
#                     'like_user_name': 'creator',
#                     'like_like': 1
#                 }
#             ],
#             'running_course': [
#                 {
#                     'running_name': '코스1',
#                     'running_description': 'des1',
#                     'running_price': 12312300,
#                     'running_period': 5,
#                     'running_thumbnail': 'thumbnail1',
#                     'running_user_name': 'creator',
#                     'running_like': 1
#                 }
#             ]
#         }
#         self.assertEqual(response.json(),{'result':'KEY_ERROR'})
#         self.assertEqual(response.status_code, 401)
>>>>>>> 9c3ac82 (review)
