from django.db import models

class UserProfile(models.Model):
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    location = models.CharField()
    experience = models.TextField()
    education = models.TextField()
    certificates = models.TextField()
    skills = models.TextField()
    description = models.TextField()
    projects = models.TextField()

    def __str__(self):
        return self.name