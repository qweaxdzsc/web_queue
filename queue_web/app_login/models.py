from django.db import models

# Create your models here.


class User(models.Model):

    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    authorization = models.CharField(max_length=128, default='normal')

    def __str__(self):
        tip = """[ID: %s, email: %s] """ % (str(self.id), self.email)
        return tip

    class Meta:
        ordering = ["id"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


