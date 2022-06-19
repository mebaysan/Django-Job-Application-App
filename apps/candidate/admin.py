from django.contrib import admin
from .models import CandidateProfile, JobSkill, JobPost


class CandidateProfileAdmin(admin.ModelAdmin):
    fields = ("user", "bio", "skills")


class JobSkillAdmin(admin.ModelAdmin):
    fields = (("name", "slug"),)
    readonly_fields = ("slug",)
    list_display = ("name", "get_related_job_count", "get_related_candidate_count")
    search_fields = ("name",)


class JobPostAdmin(admin.ModelAdmin):
    fields = (
        ("name", "slug"),
        ("description",),
        ("skills",),
        ("location", "job_type", "is_active"),
        ("created_date", "updated_date"),
        ('candidates',)
    )
    raw_id_fields = ('candidates',)
    readonly_fields = ("slug", "created_date", "updated_date")
    radio_fields = {"location": admin.HORIZONTAL, "job_type": admin.HORIZONTAL}
    list_display = (
        "name",
        "slug",
        "location",
        "job_type",
        "updated_date",
        "is_active",
        "get_candidate_count",
    )
    list_filter = ("location", "job_type", "is_active")
    search_fields = ("name",)


admin.site.register(CandidateProfile, CandidateProfileAdmin)
admin.site.register(JobSkill, JobSkillAdmin)
admin.site.register(JobPost, JobPostAdmin)
