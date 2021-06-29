
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestViews(TestCase):

    
    @classmethod
    def setUpClass(cls):
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.User = get_user_model()

        cls.user_data = {
            'username':'test_username',
            'email':'test_username@mail.com',
            'password1':'123456789uffa',
            'password2':'123456789uffa'
        }

        return super().setUpClass()

    def setUp(self):
        self.client = Client()
        return super().setUp()
    
    def test_get_user_login_page(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')


    def test_get_register_user_page(self):
        
        response = self.client.get(self.register_url)
       
      
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    def test_login_user(self):

        self.client.post(self.register_url,self.user_data)

        response = self.client.post(self.login_url,{
            'username': self.user_data['username'], 
            'password': self.user_data['password1']
        })

        self.assertEquals(response.status_code, 302)

    

    def test_register_user(self):
        username = 'test_username'
        email = 'test_username@mail.com'
        password = '123456789uffa'

        response = self.client.post(self.register_url,self.user_data)
        
        #check attributes
        fetchedUser = self.User.objects.get(email=email)


        self.assertEquals(response.status_code, 302)
        self.assertEquals(fetchedUser.username, username)
        self.assertEquals(fetchedUser.email, email)
        self.assertTrue(fetchedUser.is_authenticated)
    
