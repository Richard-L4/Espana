from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=20)
    message = models.CharField()

    def __str__(self):
        return f"{self.name} | {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
