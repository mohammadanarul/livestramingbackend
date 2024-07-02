from django.contrib import admin
from .models import SportType, League, Match, FilterCriteria

@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('fixture_id', 'league', 'home_team_name', 'away_team_name', 'match_date', 'status', 'home_team_score', 'away_team_score', 'liveurl')
    search_fields = ('home_team_name', 'away_team_name', 'venue_name', 'venue_city')
    list_filter = ('league', 'status', 'match_date')


admin.site.register(FilterCriteria)