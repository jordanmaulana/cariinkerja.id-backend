from rest_framework import serializers
from apps.jobs.models import Jobs, JobAssessment


class JobsListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for job list operations
    """
    class Meta:
        model = Jobs
        fields = [
            'uid',
            'title',
            'company_name',
            'location',
            'employment_type',
            'work_location',
            'job_title_category',
            'posted_on',
            'source_platform',
            'created_on',
        ]
        read_only_fields = ['uid', 'created_on']


class JobsDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for job detail operations
    """
    class Meta:
        model = Jobs
        fields = [
            'uid',
            'title',
            'description',
            'link',
            'hard_skills',
            'soft_skills',
            'experience_level',
            'location',
            'employment_type',
            'work_location',
            'job_title_category',
            'posted_on',
            'requirements',
            'company_name',
            'source_platform',
            'created_on',
            'updated_on',
        ]
        read_only_fields = ['uid', 'created_on', 'updated_on']


# Alias for backward compatibility
JobsSerializer = JobsDetailSerializer


class JobAssessmentSerializer(serializers.ModelSerializer):
    job = JobsDetailSerializer(read_only=True)
    job_uid = serializers.CharField(write_only=True)
    
    class Meta:
        model = JobAssessment
        fields = [
            'uid',
            'job',
            'job_uid',
            'profile',
            'summary',
            'hard_skill_gap',
            'soft_skill_gap',
            'score',
            'created_on',
            'updated_on',
        ]
        read_only_fields = ['uid', 'created_on', 'updated_on', 'profile']
    
    def create(self, validated_data):
        job_uid = validated_data.pop('job_uid')
        try:
            job = Jobs.objects.get(uid=job_uid)
            validated_data['job'] = job
        except Jobs.DoesNotExist:
            raise serializers.ValidationError({'job_uid': 'Job not found'})
        
        return super().create(validated_data)