from django.contrib import admin

from .models import Applicant, Organization, Application

admin.site.register(Applicant)
admin.site.register(Organization)
admin.site.register(Application)