import random
from django.core.management.base import BaseCommand
from lorem_text import lorem

from custom_user.models import User

from scoring.models import (
    AgeGroup,
    Archer, 
    Club,
    ClubMembership,
    Discipline,
    DisciplineMembership,
    Category,
    CategoryMembership,
    TargetFaceNameChoice,
    TargetFace,
    Team,
    TeamMembership,
    ScoringSheet,
    Round,
    RoundMembership,
    Score,
    Competition,
    CompetitionMembership,
)

from datetime import date, timedelta
import calendar
from faker import Faker
from random import randint

DAYS_OF_WEEK = {
    "monday": 0,
    "maandag": 0,
    "tuesday": 1,
    "dinsdag": 1,
    "wednesday": 2,
    "woensdag": 2,
    "thursday": 3,
    "donderdag": 3,
    "friday": 4,
    "vrijdag": 4,
    "saturday": 5,
    "zaterdag": 5,
    "sunday": 6,
    "zondag": 6,
}

SCREEN_OUTPUT = True

# DEFAULT_USERNAME = "admin"
DEFAULT_SUPERUSER_EMAil = "me@mail.com"
DEFAULT_SUPERUSER_PASSWORD = "abcd@1234"
# DEFAULT_DISPLAY_NAME = "Admin User"

class Command(BaseCommand):
    user = None
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # get or create superuser
            self.user = User.objects.filter(email=DEFAULT_SUPERUSER_EMAil).first()
            if not self.user:
                self.user = User.objects.create_superuser(
                    password=DEFAULT_SUPERUSER_PASSWORD, 
                    email=DEFAULT_SUPERUSER_EMAil
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS('Superuser "admin" created.'))
                            
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.create_normal_users()
        self.create_sample_agegroups()
        self.create_sample_archers()
        self.create_sample_clubs()
        self.create_sample_club_memberships()
        self.create_sample_disciplines()
        self.create_sample_discipline_memberships()
        self.create_sample_categories()
        self.create_sample_category_memberships()
        self.create_sample_teams()
        self.create_sample_team_memberships()
        self.create_sample_scoringsheets()
        self.create_sample_target_face_name_choices()
        self.create_sample_target_faces()
        self.create_sample_rounds("Indoor", 18, "meter", 2026, 'donderdag', '20:00')
        self.create_sample_rounds("Indoor", 18, "meter", 2027, 'donderdag', '20:00')
        self.create_sample_round_memberships()
        self.create_sample_competitions()
        self.create_sample_competitions_memberships()
        self.create_sample_scores()

    def create_normal_users(self):
        NORMAL_USERS = [
            {"email": "you1@mail.com", "password": "abcd@1234"},
            {"email": "you2@mail.com", "password": "abcd@1234"},
            {"email": "you3@mail.com", "password": "abcd@1234"},
            {"email": "you4@mail.com", "password": "abcd@1234"},
            {"email": "you5@mail.com", "password": "abcd@1234"},
        ]

        for normal_user in NORMAL_USERS:
            user = User.objects.filter(email=normal_user['email']).first()
            if not user:
                new_user = User.objects.create(
                    email=normal_user['email'],
                    password=normal_user['password']
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'New user with email { new_user.email } created'))

    def create_sample_agegroups(self):
        AGEGROUPS = [
            {"name": "Onder 12", "from_year": None, "until_year": 11},
            {"name": "Onder 14", "from_year": None, "until_year": 13},
            {"name": "Onder 18", "from_year": None, "until_year": 17},
            {"name": "Onder 21", "from_year": None, "until_year": 20},
            {"name": "Senior",   "from_year": 21,   "until_year": None},
            {"name": "50+",      "from_year": 50,   "until_year": None},
            {"name": "60+",      "from_year": 60,   "until_year": None},
        ]

        for agegroup in AGEGROUPS:
            if not AgeGroup.objects.filter(name=agegroup['name']):
                new_agegroup = AgeGroup.objects.create(
                    author=self.user,
                    name=agegroup['name'],
                    from_year=agegroup['from_year'],
                    until_year=agegroup['until_year'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'AgeGroup {new_agegroup.name} created'))

    def create_sample_archers(self):
        ARCHERS = [
            {"first_name": "Robin", "last_name": "Hood", "union_number": 121212},
            {"first_name": "Katniss", "last_name": "Evergreen", "union_number": 212121},
            {"first_name": "Legolas", "last_name": "Nightshade", "union_number": 343434},
            {"first_name": "Lara", "last_name": "Croft", "union_number": 434343},
            {"first_name": "Oliver", "last_name": "Queen", "union_number": 565656},
            {"first_name": "Merida", "last_name": "Barveheart", "union_number": 656565},
            {"first_name": "Howard", "last_name": "Archer", "union_number": 787878},
            {"first_name": "Tuck", "last_name": "Shot", "union_number": 878787},
            {"first_name": "Luna", "last_name": "Aimsalot", "union_number": 112233},
            {"first_name": "Archeron", "last_name": "Finn", "union_number": 223344},
            {"first_name": "Hawkeye", "last_name": "Pierce", "union_number": 334455},
            {"first_name": "Green", "last_name": "Arrow", "union_number": 445566},
            {"first_name": "Artemis", "last_name": "Storm", "union_number": 556677},
            {"first_name": "Bowman", "last_name": "Jackson", "union_number": 667788},
            {"first_name": "Penny", "last_name": "Pindrop", "union_number": 778899},
            {"first_name": "Shotzi", "last_name": "McShotface", "union_number": 998877},
            {"first_name": "Elinor", "last_name": "Dashwood", "union_number": 887766},
            {"first_name": "Finnly", "last_name": "Swift", "union_number": 776655},
            {"first_name": "Aiden", "last_name": "Aimright", "union_number": 665544},
            {"first_name": "Willow", "last_name": "Winstone", "union_number": 554433},
        ]

        for archer in ARCHERS:
            if not Archer.objects.filter(union_number=archer['union_number']):
                new_archer = Archer.objects.create(
                    author=self.user,
                    first_name=archer['first_name'],
                    last_name=archer['last_name'],
                    union_number=archer['union_number'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Archer "{new_archer}" created'))

    def create_sample_clubs(self):
        CLUBS = [
            {"name": "The Golden Arrows", "town": "Aarle-Rixtel"},
            {"name": "Arrow Dynamics", "town": "Best"},
            {"name": "Bullseye Archers", "town": "Bladel"},
            {"name": "The Flying Shafts", "town": "Boxtel"},
            {"name": "Target Masters", "town": "Budel"},
            {"name": "Arrowheads", "town": "Chaam"},
            {"name": "The Quiver Club", "town": "Dongen"},
            {"name": "Straight Shooters", "town": "Eersel"},
            {"name": "The Firing Line", "town": "Etten-Leur"},
            {"name": "Archery United", "town": "Geffen"},
            {"name": "The Point Blank Club", "town": "Geldrop"},
            {"name": "The Recurve Rangers", "town": "Gemert"},
            {"name": "Bowmen of Brabant", "town": "Gilze"},
            {"name": "The Aim High Club", "town": "Grave"},
            {"name": "The Silent Shooters", "town": "Helmond"},
            {"name": "The Arrow Alliance", "town": "Heusden"},
            {"name": "The Target Tazers", "town": "Hilvarenbeek"},
            {"name": "The Precision Pointers", "town": "Hooge Mierde"},
            {"name": "The Flying Arrows", "town": "Lierop"},
            {"name": "The Bow Squa", "town": "Oirschot"},
        ]

        for club in CLUBS:
            if not Club.objects.filter(name=club['name']):
                new_club  = Club.objects.create(
                    author=self.user,
                    name=club['name'],
                    town=club['town'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Club "{new_club.name} created" '))

    def create_sample_club_memberships(self):
        clubs = Club.objects.all()
        archers = Archer.objects.all()
        for club in clubs:
            for archer in archers:
                club_membership = ClubMembership.objects.filter(
                    archer=archer,
                    club=club,
                )
                if not club_membership:
                    club_membership = ClubMembership.objects.create(
                        author=self.user,
                        club=club,
                        archer=archer,
                        info=lorem.paragraph(),
                    )
                    if SCREEN_OUTPUT:
                        self.stdout.write(self.style.SUCCESS(f'New ClubMembership created: Club - {club_membership.club.name} ; Archer - {club_membership.archer.first_name} {club_membership.archer.last_name}'))

    def create_sample_disciplines(self):
        DISCIPLINES = [
            {"name": "Target Archery"},
            {"name": "Indoor Archery"},
            {"name": "Field Archery"},
            {"name": "3D Archery"},
            {"name": "Flight Archery"},
            {"name": "Clout Archery"},
            {"name": "Ski Archery"},
            {"name": "Para Archery"},
            {"name": "Run archery"},
            {"name": "Bowhunting"},
        ]

        for discipline in DISCIPLINES:
            if not Discipline.objects.filter(name=discipline['name']):
                new_discipline  = Discipline.objects.create(
                    author=self.user,
                    name=discipline['name'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Discipline "{new_discipline.name} created"'))

    def create_sample_discipline_memberships(self):
        disciplines = Discipline.objects.all()
        archers = Archer.objects.all()
        for discipline in disciplines:
            for archer in archers:                
                discipline_membership = DisciplineMembership.objects.filter(
                    archer=archer,
                    discipline=discipline,
                )
                if not discipline_membership:
                    discipline_membership = DisciplineMembership.objects.create(
                        author=self.user,
                        discipline=discipline,
                        archer=archer,
                        info=lorem.paragraph(),
                    )
                    if SCREEN_OUTPUT:
                        self.stdout.write(self.style.SUCCESS(f'New DisciplineMembership created: Discipline - {discipline_membership.discipline.name} ; Archer - {discipline_membership.archer.first_name} {discipline_membership.archer.last_name}'))

    def create_sample_categories(self):
        CATEGORIES = [
            {"name": "Recurve"},
            {"name": "Compound"},
            {"name": "Barebow"},
            {"name": "Longbow"},
            {"name": "Traditional"},
        ]

        for category in CATEGORIES:
            if not Category.objects.filter(name=category['name']):
                new_category  = Category.objects.create(
                    author=self.user,
                    name=category['name'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Category - {new_category.name} created'))

    def create_sample_category_memberships(self):
        categories = Category.objects.all()
        archers = Archer.objects.all()
        for category in categories:
            for archer in archers:                
                category_membership = CategoryMembership.objects.filter(
                    archer=archer,
                    category=category,
                )
                if not category_membership:
                    category_membership = CategoryMembership.objects.create(
                        author=self.user,
                        category=category,
                        archer=archer,
                        info=lorem.paragraph(),
                    )
                    if SCREEN_OUTPUT:
                        self.stdout.write(self.style.SUCCESS(f'New CategoryMembership created: Category - {category_membership.category.name} ; Archer - {category_membership.archer.first_name} {category_membership.archer.last_name}'))                
        
    def create_sample_teams(self):
        TEAMS = [
            {"name": "De Gouden Pijl"},
            {"name": "Pijl en Boog"},
            {"name": "Doelgericht"},
            {"name": "De Schutters van Brabant"},
            {"name": "De Vliegende Pijlen"},
            {"name": "Het Doel"},
            {"name": "De Boogschutters"},
            {"name": "De Trefzekeren"},
            {"name": "De Pijlspits"},
            {"name": "Boog en Pees"},
            {"name": "De Schietvereniging"},
            {"name": "De Pijlstormers"},
            {"name": "Het Wit Kruis"},
            {"name": "De Handboogclub"},
            {"name": "De Doelschutters"},
            {"name": "De Brabantse Bogen"},
            {"name": "De Pijlclub"},
            {"name": "De Schietclub"},
            {"name": "De Boogschutters van Nederland"},
            {"name": "De Toppers"},
        ]

        for team in TEAMS:
            if not Team.objects.filter(name=team['name']):
                new_team  = Team.objects.create(
                    author=self.user,
                    name=team['name'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Team "{new_team.name} created"'))

    def create_sample_team_memberships(self):
        teams = Team.objects.all()
        archers = Archer.objects.all()
        for team in teams:
            for archer in archers:
                team_membership = TeamMembership.objects.filter(
                    archer=archer,
                    team=team,
                )
                if not team_membership:
                    team_membership = TeamMembership.objects.create(
                        author=self.user,
                        team=team,
                        archer=archer,
                        info=lorem.paragraph(),
                    )
                    if SCREEN_OUTPUT:
                        self.stdout.write(self.style.SUCCESS(f'New TeamMembership created: Discipline - {team_membership.team.name} ; Archer - {team_membership.archer.first_name} {team_membership.archer.last_name}'))
                
    def create_sample_scoringsheets(self):
        SCORINGSHEETS = [
            {"name": "Indoor 18 meter", "columns": 3, "rows": 10},
            {"name": "Indoor 25 meter", "columns": 5, "rows": 5},
            {"name": "Outdoor 30 meter", "columns": 3, "rows": 12},
            {"name": "Outdoor 30 meter", "columns": 3, "rows": 12},
            {"name": "Outdoor 50 meter", "columns": 3, "rows": 12},
            {"name": "Outdoor 60 meter", "columns": 3, "rows": 12},
            {"name": "Outdoor 70 meter", "columns": 3, "rows": 12},
            {"name": "Outdoor 90 meter", "columns": 3, "rows": 12},
        ]

        for scoringsheet in SCORINGSHEETS:
            if not ScoringSheet.objects.filter(name=scoringsheet['name']):
                new_scoringsheet  = ScoringSheet.objects.create(
                    author=self.user,
                    name=scoringsheet['name'],
                    columns=scoringsheet['columns'],
                    rows=scoringsheet['rows'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Scoringsheet - {new_scoringsheet.name} created'))
        
    def create_sample_target_face_name_choices(self):
        TARGETFACENAMECHOICES = [
            {"environment": "Indoor",  "discipline": "Target Archery", "targetsize": "40 cm",  "keyfeature": "10-Zone"},
            {"environment": "Outdoor", "discipline": "Target Archery", "targetsize": "60 cm",  "keyfeature": "10-Zone"},
            {"environment": "Outdoor", "discipline": "Target Archery", "targetsize": "122 cm", "keyfeature": "10-Zone"},
            {"environment": "Outdoor", "discipline": "Target Archery", "targetsize": "80 cm",  "keyfeature": "10-Zone"},
            {"environment": "Outdoor", "discipline": "Field Archery",  "targetsize": "80 cm",  "keyfeature": "6-Zone"},
            {"environment": "Outdoor", "discipline": "Field Archery",  "targetsize": "60 cm",  "keyfeature": "6-Zone"},
            {"environment": "Outdoor", "discipline": "Field Archery",  "targetsize": "40 cm",  "keyfeature": "6-Zone"},
            {"environment": "Outdoor", "discipline": "Field Archery",  "targetsize": "20 cm",  "keyfeature": "6-Zone"},
        ]

        for targetfacenamechoice in TARGETFACENAMECHOICES:
            new_name = f"{targetfacenamechoice['environment']} {targetfacenamechoice['discipline']} {targetfacenamechoice['targetsize']} {targetfacenamechoice['keyfeature']}"
            if not TargetFaceNameChoice.objects.filter(name=new_name):
                new_targetfacenamechoice  = TargetFaceNameChoice.objects.create(
                    author=self.user,
                    name=new_name,
                    environment=targetfacenamechoice['environment'],
                    discipline=targetfacenamechoice['discipline'],
                    targetsize=targetfacenamechoice['targetsize'],
                    keyfeature=targetfacenamechoice['keyfeature'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'TargetFaceNameChoice {new_targetfacenamechoice.name}" created" '))
    
    def create_sample_target_faces(self):
        TARGETFACENAMES = [
            "Indoor Target Archery 40 cm 10-Zone",
            "Indoor Target Archery 60 cm 10-Zone",
            "Outdoor Field Archery 20 cm 6-Zone",
            "Outdoor Field Archery 40 cm 6-Zone",
            "Outdoor Field Archery 60 cm 6-Zone",
            "Outdoor Field Archery 80 cm 6-Zone",
            "Outdoor Target Archery 122 cm 10-Zone",
            "Outdoor Target Archery 80 cm 10-Zone",
        ]

        for targetfacename in TARGETFACENAMES:
            if not TargetFace.objects.filter(name=targetfacename):
                new_targetfacename = TargetFace.objects.create(
                    author=self.user,
                    name=targetfacename,
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'TargetFace {new_targetfacename.name} created'))

    def get_rounds_info(self, prefix, distance, unit, year, day, start_time):
        # Start a januari 1 of the given year
        d = date(year, 1,1)

        # look for the first 'day'
        d += timedelta(days=(DAYS_OF_WEEK[day]) % 7)
        
        rounds_info = []
        # Loop through the year, as long as we are in the same year
        while d.year == year: 
            name = f"{prefix} {distance} {unit} {day} {d.day} {calendar.month_name[d.month]} {d.year}"
            start_date = f"{d.year}-{d.month:02d}-{d.day:02d}"
            info = {'name': name, 'start_date': start_date, 'start_time': start_time}
            rounds_info.append(info)
            d += timedelta(days = 7) # Add a week

        return rounds_info

    def create_sample_rounds(self, prefix, distance, unit, year, day, start_time):
        rounds = self.get_rounds_info(prefix, distance, unit, year, day, start_time)
        
        for round in rounds:
            if not Round.objects.filter(name=round['name']):
                round = Round.objects.create(
                    author = self.user,
                    name = round['name'],
                    start_date = round['start_date'],
                    start_time = round['start_time'],
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Round - {round.name} created'))

    def create_sample_round_memberships(self):
        # Create all Round Archer combinations
        for round in Round.objects.all():
            for archer in Archer.objects.all():
                round_membership = RoundMembership.objects.filter(
                    archer=archer,
                    round=round,
                )
                if not round_membership:
                    round_membership = RoundMembership.objects.create(
                        author=self.user,
                        round=round,
                        archer=archer,
                        info=lorem.paragraph(),
                    )
                    if SCREEN_OUTPUT:
                        self.stdout.write(self.style.SUCCESS(f'New RoundMembership created: Round - {round_membership.round.name} ; Archer - {round_membership.archer.first_name} {round_membership.archer.last_name}'))                

    YEARS = range(2026, 2036, 1)

    def create_sample_competitions(self):

        for year in self.YEARS:
            name_string = f"Indoor 30 pijlen, {year}"
            if not Competition.objects.filter(name=name_string):
                new_competition = Competition.objects.create(
                    author=self.user,
                    name=name_string,
                    info=lorem.paragraph(),
                )
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Competition {new_competition.name} created'))

    def create_sample_competitions_memberships(self):
        for year in self.YEARS:
            competitions = Competition.objects.all()
            rounds = Round.objects.all()
            for competition in competitions:
                for round in rounds:
                    competition_membership = CompetitionMembership.objects.filter(
                        round=round,
                        competition=competition,
                    )
                    if not competition_membership:
                        # Add competition_membership if years are equal
                        if str(year) in competition.name and str(year) in round.name:
                            competition_membership = CompetitionMembership.objects.create(
                                author=self.user,
                                competition=competition,
                                round=round,
                                info=lorem.paragraph(),
                            )
                            if SCREEN_OUTPUT:
                                self.stdout.write(self.style.SUCCESS(f'New CompetitionMembership created: Competition - {competition_membership.competition.name} ; Round - {competition_membership.round.name}'))                

    # TODO: Finish create_sample_scores
    def create_sample_scores(self):
        scores = []
        roundmemberships = RoundMembership.objects.all()
        
        score = Score(
            author = self.user,
            round_archer = roundmemberships.first(),
            score = 235,
            number_of_arrows = 30,
            info=lorem.paragraph(),
        )
        scores.append(score)
        for score in scores:
            if not Score.objects.filter(round_archer=score.round_archer):
                score.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Score - {score.score} created'))

            
