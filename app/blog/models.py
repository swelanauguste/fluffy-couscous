import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from hitcount.models import HitCountMixin
from users.models import User


class PostStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Post Statuses"

    def __str__(self):
        return self.status


class PublishedManager(HitCountMixin, models.Manager):
    def get_queryset(self):
        published_status = PostStatus.objects.get(status="published").pk
        return super().get_queryset().filter(status=published_status)


class Post(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    default_status = PostStatus.objects.get(status="draft").pk
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique_for_date="published", blank=True, null=True
    )
    content = models.TextField()
    author = models.ForeignKey(
        User, related_name="blog_posts", on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.ForeignKey(
        PostStatus,
        related_name="post_statuses",
        on_delete=models.CASCADE,
        default=default_status,
    )
    published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    published_post = PublishedManager()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-published",)

    def __str__(self) -> str:
        return self.title
