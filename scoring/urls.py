from django.urls import path
from .import views

urlpatterns = [
    path('scoring/', views.scoring, name='scoring'),

    path('scoring/register/', views.register, name='scoring_register'),
    path('scoring/my-login', views.my_login, name='scoring_my-login'),
    path('scoring/user-logout', views.user_logout, name='scoring_user-logout'),
    path('scoring/dashboard', views.dashboard, name='scoring_dashboard'),
    path('scoring/database', views.database_tables, name='scoring_database'),

    # CRUD

    # Agegroup
    path('scoring/agegroups/', views.agegroups, name='scoring_agegroups'),
    path('scoring/agegroup/create/', views.create_agegroup, name='scoring_agegroup_create'),
    path('scoring/agegroup/update/<uuid:pk>/', views.update_agegroup, name='scoring_agegroup_update'),
    path('scoring/agegroup/singular/<uuid:pk>/', views.singular_agegroup, name='scoring_agegroup_singular'),
    path('scoring/agegroup/delete/<uuid:pk>/', views.delete_agegroup, name='scoring_agegroup_delete'),

    # Archer
    path('scoring/archers/', views.archers, name='scoring_archers' ),
    path('scoring/archer/create/', views.create_archer, name='scoring_archer_create' ),
    path('scoring/archer/update/<uuid:pk>/', views.update_archer, name='scoring_archer_update'),
    path('scoring/archer/singular/<uuid:pk>/', views.singular_archer, name='scoring_archer_singular'),
    path('scoring/archer/delete/<uuid:pk>/', views.delete_archer, name='scoring_archer_delete'),

    # Category
    path('scoring/categories', views.categories, name='scoring_categories'),
    path('scoring/category/create', views.create_category, name='scoring_category_create'),
    path('scoring/category/update/<uuid:pk>/', views.update_category, name='scoring_category_update'),
    path('scoring/category/singular/<uuid:pk>/', views.singular_category, name='scoring_category_singular'),
    path('scoring/category/delete/<uuid:pk>/', views.delete_category, name='scoring_category_delete'),

    # Club
    path('scoring/clubs/', views.clubs, name='scoring_clubs' ),
    path('scoring/club/create/', views.create_club, name='scoring_club_create' ),
    path('scoring/club/update/<uuid:pk>/', views.update_club, name='scoring_club_update'),
    path('scoring/club/singular/<uuid:pk>/', views.singular_club, name='scoring_club_singular'),
    path('scoring/club/delete/<uuid:pk>/', views.delete_club, name='scoring_club_delete'),

    # Competition
    path('scoring/competitions/', views.competitions, name='scoring_competitions' ),
    path('scoring/competition/create/', views.create_competition, name='scoring_competition_create' ),
    path('scoring/competition/update/<uuid:pk>/', views.update_competition, name='scoring_competition_update'),
    path('scoring/competition/singular/<uuid:pk>/', views.singular_competition, name='scoring_competition_singular'),
    path('scoring/competition/delete/<uuid:pk>/', views.delete_competition, name='scoring_competition_delete'),

    # Discipline
    path('scoring/disciplines/', views.disciplines, name='scoring_disciplines' ),
    path('scoring/discipline/create/', views.create_discipline, name='scoring_discipline_create' ),
    path('scoring/discipline/update/<uuid:pk>/', views.update_discipline, name='scoring_discipline_update'),
    path('scoring/discipline/singular/<uuid:pk>/', views.singular_discipline, name='scoring_discipline_singular'),
    path('scoring/discipline/delete/<uuid:pk>/', views.delete_discipline, name='scoring_discipline_delete'),

    # Round
    path('scoring/rounds/', views.rounds, name='scoring_rounds' ),
    path('scoring/round/create/', views.create_round, name='scoring_round_create' ),
    path('scoring/round/update/<uuid:pk>/', views.update_round, name='scoring_round_update'),
    path('scoring/round/singular/<uuid:pk>/', views.singular_round, name='scoring_round_singular'),
    path('scoring/round/delete/<uuid:pk>/', views.delete_round, name='scoring_round_delete'),

    # Score
    path('scoring/scores/', views.scores, name='scoring_scores' ),
    path('scoring/score/create/', views.create_score, name='scoring_score_create' ),
    path('scoring/score/update/<uuid:pk>/', views.update_score, name='scoring_score_update'),
    path('scoring/score/singular/<uuid:pk>/', views.singular_score, name='scoring_score_singular'),
    path('scoring/score/delete/<uuid:pk>/', views.delete_score, name='scoring_score_delete'),

    # ScoringSheet
    path('scoring/scoringsheets/', views.scoringsheets, name='scoring_scoringsheets' ),
    path('scoring/scoringsheet/create/', views.create_scoringsheet, name='scoring_scoringsheet_create' ),
    path('scoring/scoringsheet/update/<uuid:pk>/', views.update_scoringsheet, name='scoring_scoringsheet_update'),
    path('scoring/scoringsheet/singular/<uuid:pk>/', views.singular_scoringsheet, name='scoring_scoringsheet_singular'),
    path('scoring/scoringsheet/delete/<uuid:pk>/', views.delete_scoringsheet, name='scoring_scoringsheet_delete'),

    # TargetFace
    path('scoring/targetfaces/', views.targetfaces, name='scoring_targetfaces' ),
    path('scoring/targetface/create/', views.create_targetface, name='scoring_targetface_create' ),
    path('scoring/targetface/update/<uuid:pk>/', views.update_targetface, name='scoring_targetface_update'),
    path('scoring/targetface/singular/<uuid:pk>/', views.singular_targetface, name='scoring_targetface_singular'),
    path('scoring/targetface/delete/<uuid:pk>/', views.delete_targetface, name='scoring_targetface_delete'),

    # Team
    path('scoring/teams/', views.teams, name='scoring_teams' ),
    path('scoring/team/create/', views.create_team, name='scoring_team_create' ),
    path('scoring/team/update/<uuid:pk>/', views.update_team, name='scoring_team_update'),
    path('scoring/team/singular/<uuid:pk>/', views.singular_team, name='scoring_team_singular'),
    path('scoring/team/delete/<uuid:pk>/', views.delete_team, name='scoring_team_delete'),
]
