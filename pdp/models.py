from django.contrib.auth.models import User
from django.db import models


class Circle(models.Model):
    TO_DO = 'TO_DO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'

    STATUS_CHOICES = [
        (TO_DO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=TO_DO)

    def __str__(self):
        return self.name
