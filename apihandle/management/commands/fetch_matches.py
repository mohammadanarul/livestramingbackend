import os
import datetime
import requests
import django
from livestramingbackend.settings import env
from django.core.management.base import BaseCommand
from apihandle.models import SportType, League, Match

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "livestreamingBackend.settings")
django.setup()

RAPIDAPI_HOST = env('RAPIDAPI_HOST')
RAPIDAPI_KEY = env('RAPIDAPI_KEY')
RAPIDAPI_URL = env('RAPIDAPI_URL')


class Command(BaseCommand):
    help = "Fetches match data from RapidAPI and saves it into the database"

    def handle(self, *args, **kwargs):
        headers = {"x-rapidapi-host": RAPIDAPI_HOST, "x-rapidapi-key": RAPIDAPI_KEY}

        # Get today's date in the format required by the API (YYYY-MM-DD)
        today_date = datetime.date.today().isoformat()

        params = {
            "date": today_date,
        }

        response = requests.get(RAPIDAPI_URL, headers=headers, params=params)

        try:
            data = response.json()
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"Error parsing JSON: {e}"))
            return

        if "response" not in data:
            self.stderr.write(
                self.style.ERROR(f"Key 'response' not found in API response")
            )
            return

        print(f'response_data:{data["response"]}')

        for fixture_data in data["response"]:
            fixture_info = fixture_data["fixture"]
            league_info = fixture_data["league"]
            teams_info = fixture_data["teams"]
            score_info = fixture_data["score"]

            # Extracting fixture and teams IDs
            fixture_id = fixture_info["id"]
            home_team_id = teams_info["home"]["id"]
            away_team_id = teams_info["away"]["id"]

            # Fetch or create SportType
            sport_type_name = league_info.get("sport", "Unknown")
            sport_type, created = SportType.objects.get_or_create(name=sport_type_name)

            # Fetch or create League
            league_name = league_info["name"]
            league, created = League.objects.get_or_create(
                name=league_name,
                sport_type=sport_type,
                country=league_info["country"],  # Add more fields as needed
                logo=league_info["logo"],
            )

            # Save Match data
            # Save Match data
            Match.objects.update_or_create(
                fixture_id=fixture_id,
                league=league,
                home_team_name=teams_info["home"]["name"],
                home_team_logo=teams_info["home"]["logo"],
                home_team_id=home_team_id,
                away_team_name=teams_info["away"]["name"],
                away_team_logo=teams_info["away"]["logo"],
                away_team_id=away_team_id,
                match_date=fixture_info["date"],
                status=fixture_info["status"]["long"],
                home_team_score=score_info["fulltime"]["home"]
                if score_info["fulltime"]["home"]
                else 0,
                away_team_score=score_info["fulltime"]["away"]
                if score_info["fulltime"]["away"]
                else 0,
                # venue_name=fixture_info['venue']['name'],
                # venue_city=fixture_info['venue']['city'] if 'city' in fixture_info['venue'] else 'Unknown City',
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully fetched and saved match data")
        )
