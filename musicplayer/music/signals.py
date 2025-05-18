from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Song

@receiver(post_save, sender=Song)
def update_search_vector(sender, instance, **kwargs):
    Song.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('title', 'artist', 'album')
    )
    