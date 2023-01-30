from django.core.exceptions import ValidationError
from .models import Register, User
from django.shortcuts import get_object_or_404
import bcrypt

class UserService():
    def find_user(self, start):
        return [q.get_username() for q in User.objects.filter(username__startswith=start).all()]

    def find_user_by_username(self, username):
        return get_object_or_404(User, pk = username)

class RegisterService():
    def register(self, username, password, email):
        if Register.objects.filter(username = username).exists():
            raise ValidationError("Username already exists")
        else:
            password:bytes = password.encode('utf-8')
            hashed_password:bytes = bcrypt.hashpw(password, bcrypt.gensalt(10))
            Register(username = username, password = hashed_password.decode('utf-8')).save() #We have to decode because password is store as a str in DB
            User(username = username, email = email).save()

    def authenticate(self, username, password):
        exists = Register.objects.filter(username = username).exists()
        if exists:
            registration = Register.objects.filter(username = username).last()
            password = password.encode('utf-8')
            registration_password = registration.get_password().encode('utf-8') #We have to encode because password is store as a str in DB
            return bcrypt.checkpw(password, registration_password)
        else:
            return False;