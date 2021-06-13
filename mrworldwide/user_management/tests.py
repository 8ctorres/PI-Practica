from django.test import TestCase, Client
from django.contrib.auth.models import User
from user_management.views import *
from user_management.models import *
import base64

# Create your tests here.
class UserProfileTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_user_sign_up(self):
        self.user = User.objects.create_user(username="testuser", password="testpasswd")
        self.c.login(username="testuser", password="testpasswd")
        resp = self.c.get("/user/profile", {})
        self.assertEquals(resp.status_code, 200)

    def test_user_notloggedin(self):
        resp = self.c.get("/user/profile", {})
        self.assertEquals(resp.status_code, 302) #Te redirige a la pantalla de login
