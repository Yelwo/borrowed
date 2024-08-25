from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

class Objects(models.Manager):
    def my_objects(self, user: User):
        borrowed_object_ids = Borrow.objects.filter(status='borrowed', borrower__user=user).values_list('object_id', flat=True)
        lent_object_ids = Borrow.objects.filter(status='borrowed', object__owner__user=user).values_list('object_id', flat=True)
        return self.filter(
            Q(owner__user=user) & ~Q(id__in=lent_object_ids) | Q(id__in=borrowed_object_ids)
        )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Object(models.Model):
    type = models.CharField(max_length=255, blank=False, null=False)
    notes = models.CharField(max_length=255, default='', null=False, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='lent_set')
    objects = Objects()

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
