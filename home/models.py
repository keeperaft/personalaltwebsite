from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_code = models.IntegerField(default=1234567)
    alt_name = models.CharField(max_length=64, default='John Smith')
    board_of_education = models.CharField(max_length=64, default='Sagamihara-shi')
    sales_person = models.CharField(max_length=64, default='Yamada Taku')
    fax = models.CharField(max_length=64, default='045-242-7779')
    telephone = models.CharField(max_length=12, default='045-242-7555')
    interac_email = models.CharField(max_length=64, default='user@interacmail.com')

    def get_employee_code(self):
        return self.employee_code

    def __str__(self):
        return str(self.user)+' | '+str(self.employee_code)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()