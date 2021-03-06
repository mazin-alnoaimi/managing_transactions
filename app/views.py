from django.shortcuts import render, redirect, reverse
from django import forms
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)

from django.urls import reverse_lazy

from .forms import (ApplicantForm, OrganizationForm, ApplicationForm)

from .models import (Applicant, Organization, Application)


def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html', {'title': 'About'})

def applicant_list(request):
    context = {'applicant_list': Applicant.objects.all()}
    return render(request, "app/applicant_list.html", context)

def applicant_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ApplicantForm()
        else:
            applicant = Applicant.objects.get(pk=id)
            form = ApplicantForm(instance=applicant)
        return render(request, "app/applicant_form.html", {'form': form})
    else:
        if id == 0:
            form = ApplicantForm(request.POST)
        else:
            applicant = Applicant.objects.get(pk=id)
            form = ApplicantForm(request.POST,instance= applicant)

        if form.is_valid():
            form.save()
        else:
            return render(request, "app/applicant_form.html", {'form': form})
        return redirect('/applicant/list')

def applicant_delete(request,id):
    applicant = Applicant.objects.get(pk=id)
    applicant.delete()
    return redirect('/applicant/list')


def organization_list(request):
    context = {'organization_list': Organization.objects.all()}
    return render(request, "app/organization_list.html", context)

def organization_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = OrganizationForm()
        else:
            organization = Organization.objects.get(pk=id)
            form = OrganizationForm(instance=organization)
        return render(request, "app/organization_form.html", {'form': form})
    else:
        if id == 0:
            form = OrganizationForm(request.POST)
        else:
            organization = Organization.objects.get(pk=id)
            form = OrganizationForm(request.POST,instance= organization)

        if form.is_valid():
            form.save()
        else:
            return render(request, "app/organization_form.html", {'form': form})
        return redirect('/organization/list')

def organization_delete(request,id):
    organization = Organization.objects.get(pk=id)
    organization.delete()
    return redirect('/organization/list')


def application_list(request):
    context = {'application_list': Application.objects.all()}
    return render(request, "app/application_list.html", context)

def application_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ApplicationForm()
        else:
            application = Application.objects.get(pk=id)
            form = ApplicationForm(instance=application)
        return render(request, "app/application_form.html", {'form': form})
    else:
        if id == 0:
            form = ApplicationForm(request.POST)
        else:
            application = Application.objects.get(pk=id)
            form = ApplicationForm(request.POST,instance= application)

        if form.is_valid():
            form.user_id = request.user

            form.save()
        else:
            return render(request, "app/application_form.html", {'form': form})
        return redirect('/application/list')

def application_delete(request,id):
    application = Application.objects.get(pk=id)
    application.delete()
    return redirect('/application/list')