# urls.py - Simplified for downloads only
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/download/', views.download_movie, name='download_movie'),
    path('series/', views.series_list, name='series_list'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('series/<int:series_id>/season/<int:season_number>/', views.season_detail, name='season_detail'),
    path('series/<int:series_id>/season/<int:season_number>/episode/<int:episode_number>/', views.episode_detail, name='episode_detail'),
    path('episode/<int:episode_id>/download/', views.download_episode, name='download_episode'),
    path('test/', views.test_view, name='test_view'),
]