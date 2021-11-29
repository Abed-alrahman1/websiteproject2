from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages


class TestViews(TestCase):

    def test_signup(self):
        """Testing sign-up functionality."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signup.html")

    def test_signin(self):
        """Testing sign-in functionality."""
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signin.html")

    def test_signup_user(self):
        """Test function to check if user gets moved to sign-in page"""
        self.user = {
            "username": "username",
            "fname": "fname",
            "lname": "lname",
            "email": "email@gmail.com",
            "pass1": "pass1",
            "pass2": "pass1",
        }
        response = self.client.post(reverse("signup"), self.user)
        self.assertEqual(response.status_code, 302)

    def test_username_taken(self):
        """Test function to catch username duplications"""
        self.user = {
            "username": "username",
            "fname": "fname",
            "lname": "lname",
            "email": "email@gmail.com",
            "pass1": "pass1",
            "pass2": "pass1",
        }
        self.client.post(reverse("signup"), self.user)
        response = self.client.post(reverse("signup"), self.user)
        self.assertEqual(response.status_code, 409)

        # response is made into request ..
        storage = get_messages(response.wsgi_request)
        self.assertIn("Username Already Exists! , Try Again", list(map(lambda x: x.message, storage)))

    def test_email_exists(self):
        """Test function to check email duplication"""
        self.user = {
            "username": "username1",
            "fname": "fname",
            "lname": "lname",
            "email": "email@gmail.com",
            "pass1": "pass1",
            "pass2": "pass1",
        }
        self.test_user2 = {
            "username": "username11",
            "fname": "fname",
            "lname": "lname",
            "email": "email@gmail.com",
            "pass1": "pass1",
            "pass2": "pass1",
        }
        self.client.post(reverse("signup"), self.user)
        response = self.client.post(reverse("signup"), self.test_user2)
        self.assertEqual(response.status_code, 409)



