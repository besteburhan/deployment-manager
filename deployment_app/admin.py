from django.contrib import admin
from deployment_app.models import Staff, Team, Project

# Register your models here.
admin.site.register(Staff)
admin.site.register(Project)
admin.site.register(Team)
