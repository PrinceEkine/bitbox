from django.db import models
from django.core.exceptions import ValidationError

def validate_file_size(value):
    """Validate that uploaded file size doesn't exceed 5GB for downloads"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024 * 1024:  # 5GB limit for downloads
        raise ValidationError("The maximum file size is 5GB")

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/', validators=[validate_file_size])
    video_file = models.FileField(upload_to='videos/', validators=[validate_file_size])
    duration = models.IntegerField(help_text="Duration in minutes", default=0)
    director = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=0.0, help_text="Rating from 0.0 to 10.0")
    file_size = models.CharField(max_length=20, blank=True, help_text="e.g., 1.5 GB")
    file_format = models.CharField(max_length=10, default="MP4", help_text="e.g., MP4, MKV")
    quality = models.CharField(max_length=10, default="1080p", help_text="e.g., 720p, 1080p, 4K")
    download_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
    
    def __str__(self):
        return self.title
    
    def get_duration_formatted(self):
        if self.duration >= 60:
            hours = self.duration // 60
            minutes = self.duration % 60
            return f"{hours}h {minutes}m"
        return f"{self.duration}m"
    
    class Meta:
        ordering = ['-year', 'title']

class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True, help_text="Leave blank if ongoing")
    poster = models.ImageField(upload_to='series_posters/', validators=[validate_file_size])
    genres = models.ManyToManyField(Genre, blank=True, related_name='series')
    
    def __str__(self):
        return self.title
    
    @property
    def total_seasons(self):
        return self.seasons.count()
    
    @property
    def total_episodes(self):
        from django.db.models import Count
        return Episode.objects.filter(season__series=self).count()
    
    def get_years(self):
        if self.end_year:
            return f"{self.start_year}-{self.end_year}"
        return f"{self.start_year}-Present"
    
    class Meta:
        verbose_name_plural = "Series"
        ordering = ['-start_year', 'title']

class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True, help_text="Optional season title")
    poster = models.ImageField(upload_to='season_posters/', blank=True, null=True, validators=[validate_file_size])
    
    def __str__(self):
        if self.title:
            return f"{self.series.title} - Season {self.season_number}: {self.title}"
        return f"{self.series.title} - Season {self.season_number}"
    
    @property
    def episode_count(self):
        return self.episodes.count()
    
    class Meta:
        ordering = ['season_number']
        unique_together = ['series', 'season_number']

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='episodes/', validators=[validate_file_size])
    file_size = models.CharField(max_length=20, blank=True)
    file_format = models.CharField(max_length=10, default="MP4")
    quality = models.CharField(max_length=10, default="1080p")
    download_count = models.PositiveIntegerField(default=0)
    release_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", default=0)
    
    def __str__(self):
        return f"S{self.season.season_number:02d}E{self.episode_number:02d} - {self.title}"
    
    def get_episode_code(self):
        return f"S{self.season.season_number:02d}E{self.episode_number:02d}"
    
    def get_duration_formatted(self):
        if self.duration >= 60:
            hours = self.duration // 60
            minutes = self.duration % 60
            return f"{hours}h {minutes}m"
        return f"{self.duration}m"
    
    class Meta:
        ordering = ['episode_number']
        unique_together = ['season', 'episode_number']
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"