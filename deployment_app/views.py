from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from deployment_app import forms
from django.contrib.auth.models import User
from deployment_app.models import Staff, Team, Project, DeploymentNote, Comment
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.utils import timezone
from django.core.files import File
from django.db.models import Q
import pytz
import requests
import os
from .statistics import k_means_clustering
import matplotlib
matplotlib.use('Agg')


class IndexView(View):
    def get(self, request):
        if request.is_ajax():
            value = int(request.GET['value'])
            staffs = Staff.objects.all()
            if value == 1:  # for first statistic
                user_data_dict = {}
                names_user = []
                for staff in staffs:
                    staff_team_ids = staff.team.all().values_list('id', flat=True)
                    num_projects = Project.objects.filter(team_id__in=list(staff_team_ids)).count()
                    num_deploys = DeploymentNote.objects.filter(sender_id=staff.staff_id).count()
                    if num_projects != 0 or num_deploys != 0:
                        user_data_dict[staff.staff_id] = [num_projects, num_deploys]

                cluster_centers, groups = k_means_clustering.find_clusters(4, user_data_dict)
                data_points = [[] for i in range(len(groups))]
                for i in range(len(groups)):
                    elements = groups[i]
                    for e in elements:
                        staff_name = Staff.objects.get(staff_id=e).staff.first_name
                        names_user.append(staff_name)
                        data_points[i].append([user_data_dict[e][0], user_data_dict[e][1]])
                data = {
                    "datapoints": data_points,
                    "names_user": names_user,
                }

                return JsonResponse(data)

            elif value == 2:  # for second statistic
                user_data_dict = {}
                names_user = []
                for staff in staffs:
                    staff_team_ids = staff.team.all().values_list('id', flat=True)
                    num_teams = Team.objects.filter(id__in=list(staff_team_ids)).count()
                    num_projects = Project.objects.filter(team_id__in=list(staff_team_ids)).count()
                    if num_teams != 0 or num_projects != 0:
                        user_data_dict[staff.staff_id] = [num_teams, num_projects]

                cluster_centers, groups = k_means_clustering.find_clusters(4, user_data_dict)
                data_points = [[] for i in range(len(groups))]
                for i in range(len(groups)):
                    elements = groups[i]
                    for e in elements:
                        staff_name = Staff.objects.get(staff_id=e).staff.first_name
                        names_user.append(staff_name)
                        data_points[i].append([user_data_dict[e][0], user_data_dict[e][1]])
                data = {
                    "datapoints": data_points,
                    "names_user": names_user,
                }
                return JsonResponse(data)

        return render(request, 'deployment_app/index.html', {})


class RegisterView(View):
    staff_form = forms.StaffForm()
    staff_additional_info_form = forms.StaffAdditionalInfoForm()

    def get(self, request):
        return render(request, 'deployment_app/registration/registration.html',
                      {'staff_form': self.staff_form, 'staff_additional_info_form': self.staff_additional_info_form})

    def post(self, request):
        self.staff_form = forms.StaffForm(data=request.POST)
        self.staff_additional_info_form = forms.StaffAdditionalInfoForm(data=request.POST)
        # if user input is valid then new user will be created
        if self.staff_form.is_valid() and self.staff_additional_info_form.is_valid():
            staff = self.staff_form.save(commit=False)
            staff.set_password(self.staff_form.cleaned_data['password'])
            staff.username = self.staff_form.cleaned_data['email'].lower()
            staff.save()
            staff_additional_info = self.staff_additional_info_form.save(commit=False)
            staff_additional_info.phone = self.staff_additional_info_form.cleaned_data['phone']
            staff_additional_info.staff = staff
            staff_additional_info.save()
            return HttpResponseRedirect(reverse('deployment_app:login'))
        else:
            # user input is not valid
            print(self.staff_form.errors)
            return render(request, 'deployment_app/registration/registration.html',
                          {'staff_form': self.staff_form,
                           'staff_additional_info_form': self.staff_additional_info_form})


class LoginView(View):
    login_form = forms.LoginForm()

    def get(self, request):
        return render(request, 'deployment_app/registration/login.html',
                      {'login_form': self.login_form})

    def post(self, request):
        self.login_form = forms.LoginForm(data=request.POST)
        if self.login_form.is_valid():
            staff = authenticate(username=self.login_form.cleaned_data['email'],
                                 password=self.login_form.cleaned_data['password'])
            if staff and staff.is_active:
                login(request, staff)
                return HttpResponseRedirect(reverse('index'))
        else:
            print('Login failed')
            return HttpResponse("invalid login details")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('deployment_app:login'))


class ProfileView(View):
    def get(self, request, **kwargs):
        return render(request, 'deployment_app/profile/profile.html', {})


class EditProfile(View):
    edit_profile_form = forms.EditProfileForm()

    def get(self, request):
        self.edit_profile_form.initial['email'] = request.user.email
        self.edit_profile_form.initial['phone'] = request.user.staff.phone
        self.edit_profile_form.initial['first_name'] = request.user.first_name
        self.edit_profile_form.initial['last_name'] = request.user.last_name
        return render(request, 'deployment_app/profile/edit_profile.html',
                      {'edit_profile_form': self.edit_profile_form})

    def post(self, request):
        self.edit_profile_form = forms.EditProfileForm(data=request.POST)
        if self.edit_profile_form.is_valid():
            request.user.first_name = self.edit_profile_form.cleaned_data['first_name']
            request.user.last_name = self.edit_profile_form.cleaned_data['last_name']
            request.user.email = self.edit_profile_form.cleaned_data['email']
            request.user.password = make_password(self.edit_profile_form.cleaned_data['password'], hasher='pbkdf2_sha256')
        if 'photo' in request.FILES:
            request.user.staff.profile_photo = request.FILES['photo']
            print(request.FILES['photo'])
        request.user.staff.phone = self.edit_profile_form.cleaned_data['phone']
        request.user.save()
        request.user.staff.save()
        return HttpResponseRedirect(reverse('deployment_app:login'))


class TeamsView(View):
    def get(self, request):
        user_teams = request.user.staff.team.all()
        return render(request, 'deployment_app/team/teams.html',
                      {'user_teams': user_teams})


class TeamCreationView(View):
    team_create_form = forms.TeamForm()

    def post(self, request):
        team_create_form = forms.TeamForm(data=request.POST)

        if team_create_form.is_valid():
            team = team_create_form.save(commit=False)
            team.team_admin = User.objects.get(id=request.user.id)
            team.save()
            staff = Staff.objects.get(staff_id=request.user.id)
            staff.team.add(team)
            return HttpResponseRedirect(reverse('deployment_app:teams'))

        else:
            print(team_create_form.errors)
            return render(request, 'deployment_app/team/team_creation.html',
                          {'team_create_form': team_create_form})

    def get(self, request):
        return render(request, 'deployment_app/team/team_creation.html',
                      {'team_create_form': self.team_create_form})


class TeamDetailView(View):

    def get(self, request, **kwargs):
        team = Team.objects.get(id=kwargs['team_id'])
        team_projects = Project.objects.filter(team_id=team.id)
        team_members = Staff.objects.filter(Q(team=team.id), ~Q(staff_id=request.user.id))
        return render(request, 'deployment_app/team/team_detail.html',
                      {'team': team, 'team_projects': team_projects, 'team_members':team_members})

    def post(self, request, **kwargs):
        if 'member_adding' in request.POST:
            team = Team.objects.get(id=kwargs['team_id'])
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
            except Exception as ex:
                print(ex)
                return HttpResponse("INVALID EMAIL")
            add_user = User.objects.get(email=email)
            add_user.staff.team.add(team)
            return HttpResponseRedirect(reverse('deployment_app:team_detail', kwargs={'team_id': kwargs['team_id']}))
        elif 'create-project' in request.POST:
            project = Project(project_name=request.POST['project_name'], team_id=kwargs['team_id'])
            project.save()
            request.user.staff.project.add(project)
            HttpResponse("You've successfully created your team project.")
            return HttpResponseRedirect(reverse('deployment_app:team_detail', kwargs={'team_id': kwargs['team_id']}))


class ProjectsView(View):

    def get(self, request):
        staff = request.user.staff
        user_projects = staff.project.all()
        return render(self.request, 'deployment_app/projects/main_projects.html',
                      {'user_projects': user_projects, 'staff': staff})


class ProjectDetailView(View):

    def post(self, request, **kwargs):
        project_id = kwargs['project_id']
        project = Project.objects.get(id=project_id)
        if 'deploy' in request.POST:
            if 'file' in request.FILES:
                project.last_upload_date = timezone.now()
                deployment = DeploymentNote()
                file = open(str(project.last_upload_date), 'w+')
                deployment.project_file = request.FILES['file']
                deployment.created_at = project.last_upload_date
                deployment.sender = request.user
                deployment.project = project
                if request.POST['note_area']:
                    file.write(request.POST['note_area'])
                    deployment.note_file.save(str(project.last_upload_date), File(file))
                    file.close()
                    os.remove(str(project.last_upload_date))
                project.save()
                deployment.save()
                return HttpResponseRedirect(reverse('deployment_app:project_detail', kwargs={'project_id': project_id}))
        else:
            return HttpResponseRedirect(reverse('deployment_app:project_detail', kwargs={'project_id': project_id}))

    def get(self, request, **kwargs):

        project_id = kwargs['project_id']
        project = Project.objects.get(id=project_id)
        user_teams = request.user.staff.team.all()
        # check the user has a permission to view the page
        if not (project in request.user.staff.project.all() or project.team in user_teams):
            return HttpResponseForbidden("You can't view this page.")
        is_updated = False
        if project.is_github_project:
            updated_at_str = self.get_github_repo_updated_date(request, project)
            updated_at = self.convert_str_to_aware_date(updated_at_str)
            print(updated_at)
            print(project.last_upload_date)
            if updated_at > project.last_upload_date:
                project.last_upload_date = updated_at
                project.save()
                is_updated = True

        deployment_notes = DeploymentNote.objects.filter(project=project_id).order_by('created_at')
        comments = Comment.objects.all()
        return render(request, 'deployment_app/projects/project_detail.html',
                      {'project': project, 'is_updated': is_updated,
                       'deployment_notes': deployment_notes, 'comments': comments})

    @staticmethod
    def get_github_repo_updated_date(request, project):
        repo_url = "https://api.github.com/repos/" + request.user.staff.github_username + "/" + project.project_name
        response_repo = requests.get(repo_url)
        updated_at = response_repo.json()['updated_at']
        return updated_at

    @staticmethod
    def convert_str_to_aware_date(date_str):
        date_datetime = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        year = int(date_datetime.strftime("%Y"))
        month = int(date_datetime.strftime("%m"))
        day = int(date_datetime.strftime("%d"))
        hour = int(date_datetime.strftime("%H"))
        min = int(date_datetime.strftime("%M"))
        ms = int(date_datetime.strftime("%S"))
        aware_datetime = datetime(year, month, day, hour, min, ms, 0, pytz.UTC)
        print("time:", aware_datetime)
        return aware_datetime


class DeploymentNoteDetailView(View):
    def get(self, request, **kwargs):
        print("get")
        note_id = kwargs['note_id']
        deploy_note = DeploymentNote.objects.get(id=note_id)
        project = Project.objects.get(id=deploy_note.project.id)
        if not (project in request.user.staff.project.all() or project.team in request.user.staff.team.all()):
            return HttpResponseForbidden("You can't view this page.")

        comments = deploy_note.comment_set.all()
        file = open('media/'+str(deploy_note.note_file), 'r')
        deploy_content = file.read()
        print(deploy_content)
        return render(request, 'deployment_app/deployment_notes/deployment_detail.html',
                      {
                          'note': deploy_note,
                          'comments': comments,
                          'deploy_content': deploy_content,
                      })


class GithubConnectionView(View):
    base_url_user = 'https://api.github.com/users/'

    def post(self, request):
        username = request.POST['username']
        response = requests.get(self.base_url_user + username)
        context_json = response.json()
        if response.status_code != 200:
            return HttpResponse("wrong username")
        else:
            request.user.staff.github_username = username
            request.user.staff.save()
            return render(request, 'deployment_app/github/github_connection.html', context_json)

    def get(self, request):
        context_json = None
        if request.user.staff.github_username:
            response = requests.get(self.base_url_user + request.user.staff.github_username)
            context_json = response.json()

        return render(request, 'deployment_app/github/github_connection.html', context_json)


class GithubProjectsSelectionView(View):
    base_url_user = 'https://api.github.com/users/'
    base_url_repos = "https://api.github.com/repos/"

    def get(self, request):
        user_projects = request.user.staff.project.all().values_list('project_name', flat=True)
        context = self.get_repositories_dict(self, request)
        return render(request, 'deployment_app/github/connect_github_projects.html',
                      {'json': context, 'user_projects': list(user_projects)})

    def post(self, request):
        context = self.get_repositories_dict(self, request)
        for key in context:
            project_name = context[key]
            if request.POST.get(project_name):  # chosen
                response_repos = requests.get(
                    self.base_url_repos + request.user.staff.github_username + "/" + project_name)
                updated_at = response_repos.json()['updated_at']
                project = Project(project_name=project_name, last_upload_date=updated_at, is_github_project=1)
                project.save()
                request.user.staff.project.add(project)
        return HttpResponseRedirect(reverse('deployment_app:main_projects'))

    @staticmethod
    def get_repositories_dict(self, request):
        user_projects = request.user.staff.project.all().values_list('project_name', flat=True)
        github_username = request.user.staff.github_username
        repos_url = self.base_url_user + github_username + "/" + "repos"
        response = requests.get(repos_url)
        repos_json = response.json()
        context = {}
        for i in range(len(repos_json)):
            if not repos_json[i]['name'] in user_projects:
                context[str(i)] = repos_json[i]['name']
        return context
