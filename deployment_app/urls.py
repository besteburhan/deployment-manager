from django.urls import path
from deployment_app import views


app_name = 'deployment_app'

urlpatterns = [
        # registration
        path('register/', views.RegisterView.as_view(), name='register'),
        path('login/', views.LoginView.as_view(), name='login'),
        # profile
        path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
        path('edit_profile/',views.EditProfile.as_view(),name='edit_profile'),
        # team
        path('teams/', views.TeamsView.as_view(), name='teams'),
        path('teams/create_team', views.TeamCreationView.as_view(), name='create_team'),
        path('teams/team_detail/<int:team_id>', views.TeamDetailView.as_view(), name='team_detail'),
        # github
        path('connect_github/', views.GithubConnectionView.as_view(), name='connect_github'),
        path('choose_github_projects/', views.GithubProjectsSelectionView.as_view(), name='choose_github_projects'),
        # projects
        path('projects/', views.ProjectsView.as_view(), name='main_projects'),
        path('projects/<int:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
        # deployment_notes
        path('deployment_notes/<int:note_id>/', views.DeploymentNoteDetailView.as_view(), name="deployment_detail")

]
