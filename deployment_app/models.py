from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Team(models.Model):
    team_admin = models.ForeignKey(User, on_delete=models.SET_NULL, default="", null=True)
    team_name = models.CharField(max_length=256)
    # team_password = models.CharField(max_length=256, null=False, blank=False, default='')

    def __str__(self):
        return self.team_name


class Project(models.Model):
    project_name = models.CharField(max_length=256)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    last_upload_date = models.DateTimeField(auto_now_add=False, null=True)
    is_github_project = models.BooleanField(default=0)

    def __str__(self):
        return self.project_name


class Staff(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in format: '+999999999'.Up to 15 digits allowed.")

    staff = models.OneToOneField(User, on_delete=models.CASCADE, default="", null=False)
    github_username = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    team = models.ManyToManyField(Team,  blank=True) # teams olarak refactor et
    project = models.ManyToManyField(Project, blank=True)  # usage to add: staff_var.projects.add(p1)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True)

    def __str__(self):
        return self.staff.first_name + " " + self.staff.last_name


class DeploymentNote(models.Model):
    note_file = models.FileField(upload_to='deployment_notes/', null=True)
    project_file = models.FileField(upload_to='project_files/', null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    deployment_note = models.ForeignKey(DeploymentNote, on_delete=models.CASCADE )
    created_at = models.DateTimeField(default=timezone.now, null=False)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)
