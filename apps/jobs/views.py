from django.views.generic import ListView
from .models import Jobs


class JobListView(ListView):
    model = Jobs
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 20
    ordering = ['-posted_on']
    
    def get_queryset(self):
        return Jobs.objects.all().order_by('-posted_on')