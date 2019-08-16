import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from deployment_app.models import User, Staff, DeploymentNote, Team, Project

#

class Command(BaseCommand):
    help = 'populate database'

    def handle(self, *args, **options):
        for i in range(50):
            user = User()
            user.password = "123456"
            user.first_name = "firstname" + str(i)
            user.last_name = "lastname" + str(i)
            user.email = "email" + str(i) + "@e.com"
            user.username = "username" + str(i)
            staff = Staff()
            user.save()
            staff.staff = user
            staff.save()
            team_number = random.randrange(20)
            for t in range(team_number):
                u = Team.objects.filter(team_name=str("teamname" + str(t))).exists()
                if Team.objects.filter(team_name=str("teamname" + str(t))).exists():
                    team = Team.objects.get(team_name="teamname" + str(t))
                    staff.team.add(team)
                    projects = Project.objects.filter(team_id=team.id)
                    for p in projects:
                        deployment_number = random.randrange(10)
                        for d in range(deployment_number):
                            deployment_note = DeploymentNote()
                            deployment_note.created_at = timezone.now()
                            deployment_note.sender = user
                            deployment_note.project = p
                            deployment_note.save()

                else:
                    team = Team()
                    team.team_name = "teamname" + str(t)
                    team.team_admin_id = user.id
                    team.save()
                    staff.team.add(team)
                    project_number = random.randrange(10)
                    for p in range(project_number):
                        project = Project()
                        project.project_name = "projectname" + str(t) + "-" + str(p)
                        project.team = team
                        project.save()
                        deployment_number = random.randrange(10)
                        for d in range(deployment_number):
                            deployment_note = DeploymentNote()
                            deployment_note.created_at = timezone.now()
                            deployment_note.sender = user
                            deployment_note.project = project
                            deployment_note.save()

        self.stdout.write(self.style.SUCCESS('Successfull'))
