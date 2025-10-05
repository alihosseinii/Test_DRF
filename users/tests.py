from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import UserInformation
from django.contrib.auth.models import User

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse("singup")
        data = {
            "phone_number": "+989123456789",
            "password": "StrongPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserInformation.objects.filter(phone="+989123456789").exists())
        print(response.status_code)
        print(response.data)
        print(UserInformation.objects.all())




    def test_login_user(self):
        # اول کاربر رو بسازیم
        UserInformation.object.create_user(phone_number="+989123456789", password="StrongPass123")

        url = reverse("login")
        data = {
            "phone": "+989123456789",
            "password": "StrongPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_tickets_with_token(self):
        user = UserInformation.object.create_user(phone_number="+989123456789", password="StrongPass123")
        self.client.force_authenticate(user=user)

        url = reverse("tickets")
        data = {
            "title": "Concert",
            "description": "VIP ticket"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Concert")
