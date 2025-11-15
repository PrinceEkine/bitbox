# views.py - Updated for download-only
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import FileResponse
from django.db.models import F
from .models import Movie, Series, Season, Episode

def home(request):
    """Home page showing downloadable content"""
    featured_movies = Movie.objects.filter(is_featured=True)[:8]
    featured_series = Series.objects.all()[:8]
    latest_movies = Movie.objects.order_by('-id')[:6]
    popular_movies = Movie.objects.order_by('-download_count')[:6]
    
    search_query = request.GET.get('q')
    if search_query:
        featured_movies = Movie.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        featured_series = Series.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'home.html', {
        'featured_movies': featured_movies,
        'featured_series': featured_series,
        'latest_movies': latest_movies,
        'popular_movies': popular_movies,
        'search_query': search_query or ''
    })

def movie_list(request):
    """All movies available for download"""
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    """Movie detail page with download options"""
    movie = get_object_or_404(Movie, id=movie_id)
    similar_movies = Movie.objects.exclude(id=movie_id).order_by('?')[:4]
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'similar_movies': similar_movies
    })

def download_movie(request, movie_id):
    """Download movie file and increment counter"""
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Increment download count
    movie.download_count = F('download_count') + 1
    movie.save()
    
    response = FileResponse(movie.video_file.open(), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{movie.title}.{movie.file_format.lower()}"'
    return response

def series_list(request):
    """All series available for download"""
    series = Series.objects.all()
    return render(request, 'series_list.html', {'series': series})

def series_detail(request, series_id):
    """Series detail page"""
    series = get_object_or_404(Series, id=series_id)
    return render(request, 'series_detail.html', {'series': series})

def season_detail(request, series_id, season_number):
    """Season detail page"""
    season = get_object_or_404(Season, series__id=series_id, season_number=season_number)
    return render(request, 'season_detail.html', {'season': season})

def episode_detail(request, series_id, season_number, episode_number):
    """Episode detail page with download"""
    episode = get_object_or_404(
        Episode,
        season__series__id=series_id,
        season__season_number=season_number,
        episode_number=episode_number
    )
    return render(request, 'episode_detail.html', {'episode': episode})

def download_episode(request, episode_id):
    """Download episode file"""
    episode = get_object_or_404(Episode, id=episode_id)
    
    # Increment download count
    episode.download_count = F('download_count') + 1
    episode.save()
    
    response = FileResponse(episode.video_file.open(), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{episode.get_episode_code()} - {episode.title}.{episode.file_format.lower()}"'
    return response