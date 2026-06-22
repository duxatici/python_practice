from django.db import transaction, IntegrityError
from django.db.models import QuerySet, OuterRef, Subquery, Sum, Value, Q
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.views import APIView, Request
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User

from .models import Video, Like
from .serializers import VideoSerializer
from .tasks import notify_like


class VideoIdsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        video_ids = Video.objects.filter(is_published=True).values_list("id", flat=True)
        return Response(video_ids)


class VideosViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self) -> QuerySet[Video]:
        user = self.request.user

        if user.is_staff:
            return Video.objects.all()
        elif user.is_authenticated:
            return Video.objects.filter(Q(is_published=True) | Q(owner=user))
        else:
            return Video.objects.filter(is_published=True)

    @action(detail=True, methods=["POST", "DELETE"])
    @transaction.atomic
    def likes(self, request: Request, pk: int | None = None) -> Response:
        if not request.user.is_authenticated:
            return Response({"detail": "But first register pirojochek!"}, status=401)
        video = Video.objects.select_for_update().get(pk=pk)
        if video.is_published:
            if request.method == "POST":
                try:
                    Like.objects.create(video=video, user=request.user)
                    video.total_likes += 1
                    video.save()
                    notify_like.delay(video_id=video.id, user_id=request.user.id)  # type: ignore
                except IntegrityError:
                    return Response({"detail": "Already liked!"}, status=200)
                return Response({"detail": "Liked!"}, status=201)
            if request.method == "DELETE":
                deleted, _ = Like.objects.filter(
                    video=video, user=request.user
                ).delete()
                if deleted == 0:
                    return Response({"detail": "Like not found!"}, status=404)
                video.total_likes -= 1
                video.save()
                return Response(status=204)
            else:
                return Response({"detail": "Method not allowed!"}, status=405)
        else:
            return Response({"detail": "Video is not published!"}, status=400)


class StatisticGroupByView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        count_likes_by_user = (
            Video.objects.filter(is_published=True)
            .values("owner__username")
            .annotate(total_likes=Sum("total_likes"))
            .order_by("-total_likes")
        )
        return Response(count_likes_by_user)


class StatisticSubqueryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        likes = (
            Video.objects.filter(is_published=True, owner=OuterRef("pk"))
            .values("owner")
            .annotate(total=Sum("total_likes"))
            .values("total")[:1]
        )
        count_likes_by_user = (
            User.objects.annotate(likes=Coalesce(Subquery(likes), Value(0)))
            .order_by("-likes")
            .values("username", "likes")
        )
        return Response(count_likes_by_user)
