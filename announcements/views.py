#-*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Announcement

from datetime import date

# Create your views here.
def index(request) :
    latest_announcements_list = Announcement.objects.filter(end_date__gte = date.today())
    context = {
        'latest_announcements_list': latest_announcements_list,
    }
    return render(request, 'announcements/index.html', context)

def past(request) :
    past_announcements_list = Announcement.objects.filter(end_date__lt = date.today())
    context = {
        'past_announcements_list': past_announcements_list,
    }
    return render(request, 'announcements/past.html', context)

