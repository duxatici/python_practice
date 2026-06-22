from django.db import models
from django.conf import settings


class Video(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="videos"
    )
    is_published = models.BooleanField("Опубликовано?")
    name = models.CharField("Название", max_length=250)
    total_likes = models.IntegerField("Лайки", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class VideoFile(models.Model):
    QUALITY_CHOICES = [("HD", "HD"), ("FHD", "Full HD"), ("UHD", "Ultra HD")]

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")
    file = models.FileField("Путь к файлу")
    quality = models.CharField(
        "Качество видео", choices=QUALITY_CHOICES, max_length=3, default="HD"
    )

    class Meta:
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["video", "user"], name="unique_likes")
        ]
