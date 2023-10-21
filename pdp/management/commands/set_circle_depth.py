from django.core.management.base import BaseCommand

from pdp.models import Circle


class Command(BaseCommand):
    help = "Compute the depth for all circles"

    def handle(self, *args, **kwargs):
        for circle in Circle.objects.filter(parent=None):
            self.set_depth(circle, 0)

    def set_depth(self, circle, current_depth):
        circle.depth = current_depth
        circle.save()
        for child in circle.children.all():
            self.set_depth(child, current_depth + 1)
