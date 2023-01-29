from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=150)

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=200)

    def get_username(self):
            return self.username

    def get_email(self):
        return self.email
