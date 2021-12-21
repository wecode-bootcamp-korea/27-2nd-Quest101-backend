import jwt,json

from django.http import response
from datetime import datetime

from django.test import TestCase, Client

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
        
        comment = {}
        
        response = client.post('/products/comments/1',json.dumps(comment),**header, content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
        self.assertEqual(response.status_code, 401)

    def test_comment_get_success(self):
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
            }]

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

    def test_comment_delete_doesnotexist(self): 
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        
        body = {
            'comment_id' : 3
        }

        response = client.delete('/products/comments/1',json.dumps(body),**header)
        self.assertEqual(response.json(),{'message':'INVAILD_COMMENT'})
        self.assertEqual(response.status_code, 401)
