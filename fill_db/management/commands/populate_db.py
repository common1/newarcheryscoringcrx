import random
from django.core.management.base import BaseCommand
from lorem_text import lorem

from custom_user.models import User

from scoring.models import (
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
DEFAULT_USERNAME = "admin"
DEFAULT_SUPERUSER_EMAil = "me@mail.com"
DEFAULT_SUPERUSER_PASSWORD = "abcd@1234"
DEFAULT_DISPLAY_NAME = "Admin User"

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
                self.stdout.write(self.style.SUCCESS('Superuser "admin" ensured.'))
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Snippets
        self.create_sample_archers()
        # self.create_sample_clubs()
        # self.create_sample_club_memberships()
        # self.create_sample_disciplines()
        # self.create_sample_discipline_memberships()
        # self.create_sample_categories()
        # self.create_sample_category_memberships()
        self.create_sample_teams()
        self.create_sample_team_memberships()
        # self.create_sample_scoringsheets()
        # self.create_sample_target_face_name_choices()
        # self.create_sample_target_faces()
        # self.create_sample_rounds("Indoor", 18, "meter", 2026, 'donderdag', '20:00')
        # self.create_sample_round_memberships()
        # self.create_sample_competitions()
        # self.create_sample_competitions_memberships()
        # self.create_sample_scores()

    def random_with_N_digits(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1

        return randint(range_start, range_end)

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

        archers = []
        for archer_info in ARCHERS:
            archer = Archer(
                author=self.user,
                first_name=archer_info['first_name'],
                last_name=archer_info['last_name'],
                union_number=archer_info['union_number'],
                info=lorem.paragraph(),
            )
            archers.append(archer)

        for archer in archers:
            if not Archer.objects.filter(union_number=archer.union_number):
                archer.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Archer - {archer.first_name} {archer.last_name} created'))

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
        
        clubs = []
        for club_info in CLUBS:
            club  = Club(
                author=self.user,
                name=club_info['name'],
                town=club_info['town'],
                info=lorem.paragraph(),
            )
            clubs.append(club)

        for club in clubs:
            if not Club.objects.filter(name=club.name):
                club.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Club "{club.name} created" '))

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
        
        disciplines = []
        for discipline_info in DISCIPLINES:
            discipline  = Discipline(
                author=self.user,
                name=discipline_info['name'],
                info=lorem.paragraph(),
            )
            disciplines.append(discipline)
        
        for discipline in disciplines:
            if not Discipline.objects.filter(name=discipline.name):
                discipline.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Discipline "{discipline.name} created"'))

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


    # def create_sample_discipline_memberships(self):
    #     for i in range(1, 10):
    #         discipline = random.choice(Discipline.objects.all())
    #         archer = random.choice(Archer.objects.all())
    #         discipline_membership = DisciplineMembership.objects.filter(
    #             archer=archer,
    #             discipline=discipline,
    #         )
    #         if not discipline_membership:
    #             discipline_membership = DisciplineMembership.objects.create(
    #                 author=self.user,
    #                 discipline=discipline,
    #                 archer=archer,
    #                 info=lorem.paragraph(),
    #             )
    #             if SCREEN_OUTPUT:
    #                 self.stdout.write(self.style.SUCCESS(f'New DisciplineMembership created: Discipline - {discipline_membership.discipline.name} ; Archer - {discipline_membership.archer.first_name} {discipline_membership.archer.last_name}'))

    def create_sample_categories(self):
        CATEGORIES = [
            {"name": "Recurve"},
            {"name": "Compound"},
            {"name": "Barebow"},
            {"name": "Longbow"},
            {"name": "Traditional"},
        ]

        categories = []
        for category_info in CATEGORIES:
            category  = Category(
                author=self.user,
                name=category_info['name'],
                info=lorem.paragraph(),
            )
            categories.append(category)

        for category in categories:
            if not Category.objects.filter(name=category.name):
                category.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Category - {category.name} created'))

        # categories = [
        #     Category(
        #         author=self.user,
        #         name="Recurve",
        #         info=lorem.paragraph(),
        #     ),
        #     Category(
        #         author=self.user,
        #         name="Compound",
        #         info=lorem.paragraph(),
        #     ),
        #     Category(
        #         author=self.user,
        #         name="Barebow",
        #         info=lorem.paragraph(),
        #     ),
        #     Category(
        #         author=self.user,
        #         name="Longbow",
        #         info=lorem.paragraph(),
        #     ),
        #     Category(
        #         author=self.user,
        #         name="Traditional",
        #         info=lorem.paragraph(),
        #     ),
        # ]
       
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

        teams = []
        for team_info in TEAMS:
            team  = Team(
                author=self.user,
                name=team_info['name'],
                info=lorem.paragraph(),
            )
            teams.append(team)

        # teams = [
        #     Team(
        #         author=self.user,
        #         name='The Archers',
        #         info=lorem.paragraph(),              
        #     ),
        #     Team(
        #         author=self.user,
        #         name='Bullseye Squad',
        #         info=lorem.paragraph(),              
        #     ),
        #     Team(
        #         author=self.user,
        #         name='Arrow Masters',
        #         info=lorem.paragraph(),              
        #     ),
        #     Team(
        #         author=self.user,
        #         name='Target Titans',
        #         info=lorem.paragraph(),              
        #     ),
        #     Team(
        #         author=self.user,
        #         name='Precision Crew',
        #         info=lorem.paragraph(),              
        #     ),
        # ]
        for team in teams:
            if not Team.objects.filter(name=team.name):
                team.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Team "{team.name} created"'))
                         
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
        ]
        
        # scoringsheets = [
        #     ScoringSheet(
        #         author=self.user,
        #         name="Outdoor 30 meter",
        #         columns=3,
        #         rows=12,
        #         info=lorem.sentence()
        #     ),
        #     ScoringSheet(
        #         author=self.user,
        #         name="Outdoor 50 meter",
        #         columns=3,
        #         rows=12,
        #         info=lorem.sentence()
        #     ),
        #     ScoringSheet(
        #         author=self.user,
        #         name="Outdoor 60 meter",
        #         columns=3,
        #         rows=12,
        #         info=lorem.sentence()
        #     ),
        #     ScoringSheet(
        #         author=self.user,
        #         name="Outdoor 70 meter",
        #         columns=3,
        #         rows=12,
        #         info=lorem.sentence()
        #     ),
        #     ScoringSheet(
        #         author=self.user,
        #         name="Outdoor 90 meter",
        #         columns=3,
        #         rows=12,
        #         info=lorem.sentence()
        #     ),
        # ]
        for scoringsheet in scoringsheets:
            if not ScoringSheet.objects.filter(name=scoringsheet.name):
                scoringsheet.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Scoringsheet - {scoringsheet.name} created'))

    # TODO: Finish create_sample_target_face_name_choices
    def create_sample_target_face_name_choices(self):
        targetfacenamechoices = [
            TargetFaceNameChoice(
                author=self.user,
                environment="Indoor",
                discipline="Target Archery",
                targetsize="40 cm",
                keyfeature="10-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Indoor",
                discipline="Target Archery",
                targetsize="60 cm",
                keyfeature="10-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Target Archery",
                targetsize="122 cm",
                keyfeature="10-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Target Archery",
                targetsize="80 cm",
                keyfeature="10-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Field Archery",
                targetsize="80 cm",
                keyfeature="6-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Field Archery",
                targetsize="60 cm",
                keyfeature="6-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Field Archery",
                targetsize="40 cm",
                keyfeature="6-Zone",
                info=lorem.paragraph(),
            ),
            TargetFaceNameChoice(
                author=self.user,
                environment="Outdoor",
                discipline="Field Archery",
                targetsize="20 cm",
                keyfeature="6-Zone",
                info=lorem.paragraph(),
            ),
        ]
        for targetfacenamechoice in targetfacenamechoices:
            new_name = f"{targetfacenamechoice.environment} {targetfacenamechoice.discipline} {targetfacenamechoice.targetsize} {targetfacenamechoice.keyfeature}"
            if not TargetFaceNameChoice.objects.filter(name=new_name):
                targetfacenamechoice.name = new_name
                targetfacenamechoice.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'TargetFaceNameChoice "{new_name} created" '))
    
    def create_sample_target_faces(self):
        TARGET_FACE_NAMES = [
            "Indoor Target Archery 40 cm 10-Zone",
            "Indoor Target Archery 60 cm 10-Zone",
            "Outdoor Field Archery 20 cm 6-Zone",
            "Outdoor Field Archery 40 cm 6-Zone",
            "Outdoor Field Archery 60 cm 6-Zone",
            "Outdoor Field Archery 80 cm 6-Zone",
            "Outdoor Target Archery 122 cm 10-Zone",
            "Outdoor Target Archery 80 cm 10-Zone",
        ]

        targetface_instances = []
        for targetface_name in TARGET_FACE_NAMES:
            obj = TargetFace(
                author=self.user,
                name=targetface_name,
                info=lorem.paragraph(),
            ),
            targetface_instances.append(obj[0])

        for targetface_instance in targetface_instances:
            if not TargetFace.objects.filter(name=targetface_instance.name):
                targetface_instance.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'TargetFace - {targetface_instance.name} created'))

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
        rounds = []
        rounds_info = self.get_rounds_info(prefix, distance, unit, year, day, start_time)
        for round_info in rounds_info:
            round = Round(
                author = self.user,
                name = round_info['name'],
                start_date = round_info['start_date'],
                start_time = round_info['start_time'],
                info=lorem.paragraph(),
            )
            rounds.append(round)

        for round in rounds:
            if not Round.objects.filter(name=round.name):
                round.save()
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

        competitions = []
        for year in self.YEARS:
            name_string = f"Indoor 30 pijlen, {year}"
            competition = Competition(
                author=self.user,
                name=name_string,
                info=lorem.paragraph(),
            ),
            competitions.append(competition[0])

        for competition in competitions:
            if not Competition.objects.filter(name=competition.name):
                competition.save()
                if SCREEN_OUTPUT:
                    self.stdout.write(self.style.SUCCESS(f'Competition - {competition.name} created'))
    
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

            
