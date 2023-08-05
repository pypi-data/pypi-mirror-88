import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ... import __title__
from ...utils import LoggerAddTag


logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class Command(BaseCommand):
    help = "Preloads data required for this app from ESI"

    def handle(self, *args, **options):
        call_command(
            "eveuniverse_load_types",
            __title__,
            "--category_id",
            "6",
            "--category_id",
            "65",
        )
