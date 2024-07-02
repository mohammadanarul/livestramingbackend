from django.db import models

class SportType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100)
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE)
    logo = models.URLField(default='default_logo_url')
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    fixture_id = models.PositiveIntegerField(unique=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_team_name = models.CharField(max_length=100)
    home_team_logo = models.URLField()
    home_team_id = models.PositiveIntegerField()
    away_team_name = models.CharField(max_length=100)
    away_team_logo = models.URLField()
    away_team_id = models.PositiveIntegerField()
    match_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    # venue_name = models.CharField(max_length=100)
    # venue_city = models.CharField(max_length=100)
    liveurl = models.URLField(blank=True, null=True)  # Optional live URL field

    def __str__(self):
        return f"{self.home_team_name} vs {self.away_team_name}"



class FilterCriteria(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name