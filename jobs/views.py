from django.shortcuts import render

from .models import Job

from datetime import date

# Create your views here.
def index(request) :
    open_jobs_list = Job.objects.filter(filled = False)
    open_jobs_list = open_jobs_list.filter(post_date__lte = date.today())
    open_jobs_list = open_jobs_list.filter(expiration_date__gte = date.today())
    context = {
        'open_jobs_list': open_jobs_list,
    }
    return render(request, 'jobs/index.html', context)

