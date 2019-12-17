from django.contrib import admin
from profile_details.models import *

# Register your models here.
@admin.register(CandidateDetails)
class CandidateDetails(admin.ModelAdmin):
    list_display = [field.name for field in CandidateDetails._meta.fields]

@admin.register(Skills)
class Skills(admin.ModelAdmin):
    list_display = [field.name for field in Skills._meta.fields]