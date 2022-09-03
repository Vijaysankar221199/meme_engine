from django.db import models
from django.contrib.auth.models import User

class Meme(models.Model):
    memeId = models.AutoField(primary_key=True)
    memeName = models.CharField(max_length = 180)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    status = models.BooleanField(default = False, blank = True)
    tags = models.CharField(max_length = 300)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.task
