from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import random

from videos.models import Video


class Command(BaseCommand):
    help = "Create 10k users and 100k videos"

    def handle(self, *args: Any, **options: Any) -> str | None:
        users = []
        User = get_user_model()
        password = make_password("123")
        for i in range(10_000):
            users.append(User(username=f"user_{i}", password=password))
        User.objects.bulk_create(users, batch_size=1000)

        videos = []
        for i in range(100_000):
            videos.append(
                Video(
                    owner=random.choice(users),
                    is_published=True,
                    name=f"Мое супер видео №{i}",
                    total_likes=random.randint(0, 1_000_000),
                )
            )
        Video.objects.bulk_create(videos, batch_size=1000)
