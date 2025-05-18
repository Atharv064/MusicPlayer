from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import PermissionDenied

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['title']),
            models.Index(fields=['artist']),
            models.Index(fields=['album']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.uploaded_by.is_staff:
            raise PermissionDenied("Only Admin user can upload songs")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    def get_absolute_url(self):
        return reverse('song-detail', kwargs={'pk': self.pk})

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField('Song', through='PlaylistSong')
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', null = True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('playlist-detail', kwargs = {'pk':self.pk})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank = True)
    location = models.CharField(max_length=30, blank = True)
    birth_date = models.DateField(null = True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')


    def __str__(self):
        return f'{self.user.username} Profile'
    

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.playlist.name} - {self.song.title}"
    