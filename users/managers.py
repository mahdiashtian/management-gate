from django.db import models


class RoomManager(models.Manager):
    def all(self):

        return self.prefetch_related(
            'members',
        ).select_related(
            'owner'
        )
