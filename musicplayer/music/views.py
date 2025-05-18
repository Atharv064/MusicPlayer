from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegisterForm, SongForm, UserUpdateForm, ProfileUpdateForm, PlaylistForm, AddToPlaylistForm
from .models import Song, Playlist, PlaylistSong
from django.contrib import messages
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .forms import UserEditForm
from django.core.paginator import Paginator


def home(request):
    songs = Song.objects.all()
    return render(request, 'music/home.html', {'songs': songs})

@login_required
def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'music/song_detail.html', {'song': song})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'music/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'music/login.html', {'error': 'Invalid credentials'})
    return render(request, 'music/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@staff_member_required
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            return redirect('home')
    else:
        form = SongForm()
    return render(request, 'music/add_song.html', {'form': form})

@staff_member_required
def manage_users(request):
    user_list = User.objects.all().order_by('-date_joined')
    
    search_query = request.GET.get('search', '')
    if search_query:
        user_list = user_list.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
                                   

    paginator = Paginator(user_list, 10)

    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'music/manage_users.html', {
        'users': users, 
        'search_query': search_query
        })




@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('manage-users')
        else:
            form = UserEditForm(instance=user)
        return render(request, 'music/edit_user.html', {'form':form, 'user':user})
    
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('manage-users')
    return render(request, 'music/confirm_delete_user.html', {'user':user})

@staff_member_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            messages.success(request, 'Song uploaded successdully!')
            return redirect('home')
        else:
            form = SongForm(user=request.user)
        return render(request, 'music/uploaded_song.html', {'form':form})
    

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form':p_form,
    }
    return render(request, 'music/profile.html', context)

def user_profile(request, username):
    user = User.objects.get(username = username)
    return render(request, 'music/user_profile.html', {'user_profile':user})


@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'music/playlist_list.html', {'playlists': playlists})


@login_required
def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, 'Playlist created successfully!')
            return redirect('playlist-list')
        else:
            form = PlaylistForm()
        return render(request, 'music/playlist_form.html', {'form':form})
    
@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    return render(request, 'music/playlist_detail.html',{'playlist':playlist})

@login_required
def playlist_update(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Playlist updated successfully!')
            return redirect('playlist-detail', pk=playlist.pk)
    else:
        form = PlaylistForm(instance = playlist)
    return render(request, 'music/playlist_form.html', {'form':form})

@login_required
def playlist_delete(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    if request.method == 'POST':
        playlist.delete()
        messages.success(request, 'Playlist deleted successfully!')
        return redirect('playlist-list')
    return render(request, 'music/playlist_confirm_delete.html', {'playlist': playlist})

@login_required
def add_to_playlist(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        form = AddToPlaylistForm(request.user, request.POST)
        if form.is_valid():
            playlist = form.cleaned_data['playlist']
            # Add song to playlist with the next available position
            position = PlaylistSong.objects.filter(playlist=playlist).count() + 1
            PlaylistSong.objects.create(
                playlist=playlist,
                song=song,
                position=position
            )
            messages.success(request, f'Song added to {playlist.name}!')
            return redirect('song-detail', pk=song.pk)
    else:
        form = AddToPlaylistForm(request.user)
    return render(request, 'music/add_to_playlist.html', {'form': form, 'song': song})

@login_required
def remove_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        PlaylistSong.objects.filter(playlist=playlist, song=song).delete()
        # Reorder remaining songs
        for index, item in enumerate(PlaylistSong.objects.filter(playlist=playlist).order_by('position'), start=1):
            item.position = index
            item.save()
        messages.success(request, 'Song removed from playlist!')
        return redirect('playlist-detail', pk=playlist.pk)
    return render(request, 'music/remove_from_playlist.html', {'playlist': playlist, 'song': song})

def search_songs(request):
    query = request.GET.get('q')
    if query:
        vector = SearchVector('title', weight='A') + \
                 SearchVector('artist', weight='B') + \
                 SearchVector('album', weight='C')
        search_query = SearchQuery(query)
        songs = Song.objects.annotate(
            rank=SearchRank(vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    else:
        songs = Song.objects.none()
    return render(request, 'music/search_results.html', {
        'songs': songs,
        'query':query
    })


def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)
