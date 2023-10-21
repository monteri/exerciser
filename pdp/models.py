from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    circle = models.ForeignKey(
        "Circle", on_delete=models.SET_NULL, null=True, blank=True
    )


class Circle(models.Model):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    STATUS_CHOICES = [
        (TO_DO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="circles")
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=TO_DO)
    depth = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        name = (
            f"{instance.first_name} {instance.last_name}"
            if instance.first_name and instance.last_name
            else instance.username
        )
        circle = Circle.objects.create(name=name, user=instance)
        UserAccount.objects.create(user=instance, circle=circle)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.useraccount.save()
