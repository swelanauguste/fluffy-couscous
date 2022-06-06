from django.core.management.base import BaseCommand

from ...models import PostStatus


class Command(BaseCommand):
    help = "Add blog statuses"

    def handle(self, *args, **options):
        PostStatus.objects.create(status="draft")
        PostStatus.objects.create(status="published")
        PostStatus.objects.create(status="deleted")
        self.stdout.write(self.style.SUCCESS("blog statuses added"))