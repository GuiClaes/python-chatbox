from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=200)
    emission_time = models.DateTimeField('emission time', null = True)
    author = models.CharField(max_length=200)

    def get_content(self):
        return self.content

    def get_emission_time(self):
        return self.emission_time

    def get_author(self):
        return self.author