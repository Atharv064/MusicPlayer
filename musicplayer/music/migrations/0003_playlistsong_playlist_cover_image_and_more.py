# Generated by Django 5.2 on 2025-05-17 11:43

import django.contrib.postgres.indexes
import django.contrib.postgres.search
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='playlist_covers/'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='song',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='music_song_search__341a43_gin'),
        ),
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['title'], name='music_song_title_8e56ff_idx'),
        ),
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['artist'], name='music_song_artist_173532_idx'),
        ),
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['album'], name='music_song_album_05217d_idx'),
        ),
        migrations.AddField(
            model_name='playlistsong',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.playlist'),
        ),
        migrations.AddField(
            model_name='playlistsong',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song'),
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='songs',
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(through='music.PlaylistSong', to='music.song'),
        ),
    ]
