from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='normal@user.com')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # self.assertRaises()
        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            assert 'username does not exist'
        self.assertEqual(user.username, 'user')

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='user', email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', email='normal@user.com')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='superuser', email='super@user.com', password='mypass')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'superuser')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@user.com', password='mypass', is_superuser=False)
