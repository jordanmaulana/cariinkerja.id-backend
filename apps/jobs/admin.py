from django.contrib import admin
from .models import Jobs, JobAssessment


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = [
        'uid',
        'title',
        'company_name',
        'link',
        'experience_level',
        'location',
        'employment_type',
        'work_location',
        'job_title_category',
        'posted_on',
    ]
    list_filter = [
        'employment_type',
        'work_location',
        'experience_level',
        'job_title_category',
        'posted_on',
    ]
    search_fields = [
        'title',
        'description',
        'location',
        'hard_skills',
        'soft_skills',
        'job_title_category',
    ]
    readonly_fields = ['uid', 'created_on', 'updated_on']


@admin.register(JobAssessment)
class JobAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'uid',
        'job',
        'profile',
        'summary',
        'hard_skill_gap',
        'soft_skill_gap',
        'created_on',
        'updated_on',
        'actor',
    ]
    list_filter = [
        'created_on',
        'updated_on',
    ]
    search_fields = [
        'summary',
        'hard_skill_gap',
        'soft_skill_gap',
        'job__title',
        'profile__user__username',
    ]
    readonly_fields = ['uid', 'created_on', 'updated_on']
    raw_id_fields = ['job', 'profile']