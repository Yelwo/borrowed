from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Object(models.Model):
    type = models.CharField(max_length=255, blank=False, null=False)
    notes = models.CharField(max_length=255, default='', null=False, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='lent_set')

    def __str__(self):
        return f"{self.type} {self.owner}"


class Borrow(models.Model):
    borrower = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True)
    borrowing_date = models.DateField(blank=True, null=True, editable=True)
    due_date = models.DateField(blank=True, null=True, editable=True)
    status = models.CharField(max_length=255, blank=False, null=False, default='borrowed')
    object = models.ForeignKey(Object, on_delete=models.PROTECT, null=False)
    notes = models.CharField(max_length=255, default='', null=False, blank=True)

    def __str__(self) -> str:
        return f"{self.object.type}: {self.borrowing_date} - {self.due_date}"
