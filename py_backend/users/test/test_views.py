from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
import json

class RegisterTests(TestCase):

    def setUp(self):
        CustomUser.objects.create(
            username="lboulatr",
            email="lboulatr@gmail.com",
            password="Damiendubocal75")
    
    def test_basic_user(self):
        user = CustomUser.objects.get(username="lboulatr")
        user = CustomUser.objects.get(email="lboulatr@gmail.com")
        self.assertEqual(user.username, 'lboulatr')
        self.assertEqual(user.email, 'lboulatr@gmail.com')

    def test_new_user_in_database(self):
        newUser = {
            'username': 'bob_seger',
            'email': 'bobseger@gmail.com',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        initial_user_count = CustomUser.objects.count()

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), initial_user_count + 1)

    def test_new_username_too_short(self):
        newUser = {
            'username': 'bo',
            'email': 'bobseger@gmail.com',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_new_password_too_short(self):
        newUser = {
            'username': 'bobby_seger',
            'email': 'bobseger@gmail.com',
            'password1': 'Newt',
            'password2': 'Newt'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        newUser = {
            'username': 'bob_seger',
            'email': 'lboulatrgmail.com',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
    
    def test_invalid_email_2(self):
        newUser = {
            'username': 'bob_seger',
            'email': 'lboulatr@gmailcom',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_email_is_already_used(self):
        newUser = {
            'username': 'bob_seger',
            'email': 'lboulatr@gmail.com',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_username_is_already_used(self):
        newUser = {
            'username': 'lboulatr',
            'email': 'routine@gmail.com',
            'password1': 'Newtrans9+',
            'password2': 'Newtrans9+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_weak_password(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password1': '+',
            'password2': '+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_different_password1(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,',
            'password2': 'Km4C47_x£6v,+'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_different_password2(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,+',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_username(self):
        newUser = {
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,+',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_email(self):
        newUser = {
            'username': 'ochoa',
            'password1': 'Km4C47_x£6v,+',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_password1(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_password2(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
    
    def test_not_json_register(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,+',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=newUser)

        self.assertEqual(response.status_code, 406)

    def test_username_too_long(self):
        newUser = {
            'username': 'ochoaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': 'ochoaloco@gmail.com',
            'password1': 'Km4C47_x£6v,',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
    
    def test_invalid_email(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoalocogmail.com',
            'password1': 'Km4C47_x£6v,',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
    
    def test_invalid_email＿2(self):
        newUser = {
            'username': 'ochoa',
            'email': 'ochoaloco@gmailcom',
            'password1': 'Km4C47_x£6v,',
            'password2': 'Km4C47_x£6v,'
        }

        response = self.client.post(
            reverse('register'), 
            data=json.dumps(newUser), 
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

# =========================================================================================

class LoginTests(TestCase):

    def setUp(self):
        CustomUser.objects.create_user(
            username="lboulatr",
            email="lboulatr@gmail.com",
            password="Damiendubocal75")

    def test_basic_user(self):
        user = CustomUser.objects.get(username="lboulatr")
        user = CustomUser.objects.get(email="lboulatr@gmail.com")
        self.assertEqual(user.username, 'lboulatr')
        self.assertEqual(user.email, 'lboulatr@gmail.com')

    def test_basic_login(self):
        user = {
            'username': 'lboulatr',
            'password': 'Damiendubocal75'
        }

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_not_json_login(self):
        user = {
            'username': 'lboulatr',
            'password': 'Damiendubocal75'
        }

        response = self.client.post(
            reverse('login'), 
            data=user)

        self.assertEqual(response.status_code, 406)
        
    def test_wrong_login(self):
        user = {
            'username': 'lboulatx',
            'password': 'Damiendubocal75'
        }

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_wrong_password(self):
        user = {
            'username': 'lboulatr',
            'password': 'Damiendubocal75*'
        }

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_missing_username(self):
        user = {
            'password': 'Damiendubocal75'
        }

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        user = {
            'username': 'lboulatr'
        }

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_missing_datas(self):
        user = {}

        response = self.client.post(
            reverse('login'), 
            data=json.dumps(user), 
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)