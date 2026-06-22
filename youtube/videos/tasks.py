from celery import shared_task
from django.contrib.auth import get_user_model

from .models import Video

User = get_user_model()


@shared_task
def notify_like(video_id: int, user_id: int) -> None:
    video = Video.objects.get(id=video_id)
    user = User.objects.get(id=user_id)

    message = f"[Уведомление] Пользователь {user.username} лайкнул видео '{video.name}'"
    print(message)
