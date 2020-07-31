from django.db import models

# Create your models here.


class User(models.Model):
    # gender = (
    #     ('male', "男"),
    #     ('female', "女"),
    # )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        tip = """[ID: %s, email: %s] """ % (str(self.id), self.email)
        return tip

    class Meta:
        ordering = ["id"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


