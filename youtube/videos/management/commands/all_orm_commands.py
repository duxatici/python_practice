from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from videos.models import Video

import logging

logging.getLogger("django.db.backends").disabled = True


class Command(BaseCommand):
    help = "Execute all SQL commands"

    def handle(self, *args: Any, **options: Any) -> str | None:
        connection.queries_log.clear()
        list(Video.objects.all())
        print("=== all ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.filter(is_published=True))
        print("\n=== filter ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.exclude(is_published=True))
        print("\n=== exclude ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.defer("name"))
        print("\n=== defer ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.only("name", "total_likes"))
        print("\n=== only ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.values("id", "name"))
        print("\n=== values ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.values_list("id", flat=True))
        print("\n=== values_list ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.select_related("owner").all()[:5])
        print("\n=== select_related ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        list(Video.objects.prefetch_related("files").all()[:5])
        print("\n=== prefetch_related ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        with transaction.atomic():
            list(Video.objects.select_for_update().filter(pk=1))
        print("\n=== select_for_update ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        Video.objects.count()
        print("\n=== count ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        Video.objects.exists()
        print("\n=== exists ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        Video.objects.get_or_create(
            id=Video.objects.first().id,
            defaults={"name": "test", "owner_id": 1, "is_published": True},
        )
        print("\n=== get_or_create ===")
        for q in connection.queries:
            print(q["sql"])
            print()

        connection.queries_log.clear()
        v = Video.objects.first()
        v.name = v.name
        v.save()
        print("\n=== save ===")
        for q in connection.queries:
            print(q["sql"])
            print()
