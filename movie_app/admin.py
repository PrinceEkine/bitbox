from django.contrib import admin
from .models import Genre, Movie, Series, Season, Episode

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'rating', 'download_count', 'is_featured')
    list_filter = ('year', 'genres', 'is_featured', 'quality')
    search_fields = ('title', 'description', 'director')
    filter_horizontal = ('genres',)
    readonly_fields = ('download_count',)

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ['episode_number', 'title', 'release_date', 'duration', 'video_file', 'file_size', 'quality']

class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    fields = ['season_number', 'title', 'poster']
    inlines = [EpisodeInline]

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_year', 'end_year', 'total_seasons', 'total_episodes')
    list_filter = ('start_year', 'genres')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
    inlines = [SeasonInline]
    
    def total_seasons(self, obj):
        return obj.seasons.count()
    total_seasons.short_description = 'Seasons'
    
    def total_episodes(self, obj):
        return Episode.objects.filter(season__series=obj).count()
    total_episodes.short_description = 'Episodes'

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'title', 'episode_count')
    list_filter = ('series', 'season_number')
    inlines = [EpisodeInline]
    
    def episode_count(self, obj):
        return obj.episodes.count()
    episode_count.short_description = 'Episodes'

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'season', 'title', 'download_count', 'release_date', 'duration')
    list_filter = ('season__series', 'season__season_number')
    search_fields = ('title', 'description')
    list_select_related = ('season', 'season__series')
    readonly_fields = ('download_count',)

admin.site.register(Movie, MovieAdmin)