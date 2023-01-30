from django.test import TestCase
from .models import User, Register
from .service import UserService, RegisterService
import bcrypt

class UserServiceTest(TestCase):
    def setUp(self):
        User.objects.create(username = "User1", email = "User1@gmail.com")
        User.objects.create(username = "User2", email = "User2@gmail.com")

    def test_find_user(self):
        user_service = UserService()
        user_found = user_service.find_user(start="Use")
        self.assertEqual(len(user_found), 2)
        self.assertEqual(user_found[0], "User1")
        self.assertEqual(user_found[1], "User2")

        user_found = user_service.find_user(start="Test")
        self.assertEqual(len(user_found), 0)

        user_found = user_service.find_user(start="User1")
        self.assertEqual(len(user_found), 1)
        self.assertEqual(user_found[0], "User1")

    def test_find_user_by_username(self):
        user_service = UserService()
        user = user_service.find_user_by_username(username = "User1")
        self.assertEqual(user.username, "User1")
        self.assertEqual(user.email, "User1@gmail.com")

class RegisterServiceTest(TestCase):
    def setUp(self):
        password = "crypted_password"
        password:bytes = password.encode('utf-8')
        hashed_password:bytes = bcrypt.hashpw(password, bcrypt.gensalt(10))
        Register.objects.create(username = "User1", password = hashed_password.decode('utf-8'))

    def test_register(self):
        register_service = RegisterService()
        register_service.register(username = "User2", password = "crypted_password", email = "test@gmail.com")
        registered = Register.objects.filter(username = "User2").last()
        user = User.objects.filter(username = "User2").last()
        self.assertEqual(registered.username, "User2")
        self.assertNotEqual(registered.password, "crypted_password")
        self.assertEqual(user.username, "User2")
        self.assertEqual(user.email, "test@gmail.com")

    def test_authenticate(self):
        register_service = RegisterService()
        authenticated = register_service.authenticate(username = "User1", password = "crypted_password")
        self.assertTrue(authenticated)