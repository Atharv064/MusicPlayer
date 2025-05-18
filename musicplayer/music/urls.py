from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('song/<int:pk>/', views.song_detail, name='song-detail'),
    path('add-song/', views.add_song, name='add-song'),
    path('manage-users/', views.manage_users, name='manage-users'),
    path('profile/', views.profile, name='profile'), 
    path('user/<str:username>/', views.user_profile, name = 'user-profile'),
    path('playlists/', views.playlist_list, name='playlist-list'),
    path('playlists/create/', views.playlist_create, name='playlist-create'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist-detail'),
    path('playlists/<int:pk>/update/', views.playlist_update, name='playlist-update'),
    path('playlists/<int:pk>/delete/', views.playlist_delete, name='playlist-delete'),
    path('song/<int:song_id>/add-to-playlist/', views.add_to_playlist, name='add-to-playlist'),
    path('playlists/<int:playlist_id>/remove-song/<int:song_id>/', views.remove_from_playlist, name='remove-from-playlist'),
    path('search/', views.search_songs, name='song-search'),
    path('manage-users/edit/<int:user_id>/', views.edit_user, name='edit-user'),
    path('manage-users/delete/<int:user_id>/', views.delete_user, name='delete-user'),
    path('upload/', staff_member_required(views.upload_song), name='upload-song'),
]
