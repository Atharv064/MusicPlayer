from django.contrib import admin
from .models import Song, Playlist, Profile

#Register your models here.
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Profile)

