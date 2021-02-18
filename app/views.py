from django.shortcuts import render, redirect, reverse
from django import forms
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Applicant
from .models import Organization
from .models import Application

def home(request):
    return render(request, 'app/home.html') #, context)


def about(request):
    return render(request, 'app/about.html', {'title': 'About'})


def applicant(request):
    context = {
        'applicants': Applicant.objects.all()
    }
    return render(request, 'app/applicant.html', context)

def organization(request, applicant=None):
    context = {
        'organizations': Organization.objects.all()
    }
    return render(request, 'app/organization.html', context)

def application(request):
    context = {
        'applications': Application.objects.all()
    }
    return render(request, 'app/application.html', context)

class ApplicantListView(LoginRequiredMixin, ListView):
    model = Applicant
    template_name = 'app/applicant.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'applicants'
    # ordering = ['-date_posted']

    def get_queryset(self):
        return super(ApplicantListView, self).get_queryset().filter(user_id=self.request.user)

class ApplicantDetailView(DetailView):
    model = Applicant

class ApplicantCreateView(LoginRequiredMixin, CreateView):
    model = Applicant
    fields = [
        'cpr', 
        'cpr_expiry_date', 
        'fullname', 
        'gender', 
        'qualification', 
        'occupcation', 
        'flat_no', 
        'building_no', 
        'road_no', 
        'area', 
        'contact1', 
        'contact2', 
        'email', 
        'user_id', 
        'user_id', 
        # 'cpr_doc', 
        # 'passport_doc', 
        # 'behavior_cert_doc', 
        # 'bank_statement_doc'
        ]

    def form_valid(self, form):
        
        if form.instance.cpr_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your CPR')
            return False

        form.instance.user_id = self.request.user
        return super(ApplicantCreateView, self).form_valid(form)

class ApplicantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Applicant
    fields = [
        'cpr', 
        'cpr_expiry_date', 
        'fullname', 
        'gender', 
        'qualification', 
        'occupcation', 
        'flat_no', 
        'building_no', 
        'road_no', 
        'area', 
        'contact1', 
        'contact2', 
        'email']

    def form_valid(self, form):
        
        if form.instance.cpr_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your CPR')
            return False

        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        applicant = self.get_object()
        if self.request.user == applicant.user_id:
            return True
        return False

class ApplicantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Applicant
    success_url = '/applicant'

    def test_func(self):
        applicant = self.get_object()
        if self.request.user == applicant.user_id:
            return True
        return False


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'app/organization.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'organizations'
    # ordering = ['-date_posted']

    def get_queryset(self):
        return super(OrganizationListView, self).get_queryset().filter(user_id=self.request.user)

class OrganizationDetailView(DetailView):
    model = Organization

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    fields = [
        'cr',
        'cr_reg_date',
        'full_en_name',
        'full_ar_name',
        'license_no',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'applicant_id',
        'user_id',
        # 'cr_doc',
        # 'bank_statement_doc',
        # 'lmra_agreement'
        ]
    #widgets = {
    #        'cr_reg_date': DateTimeInput(attrs={'type': 'datetime-local'}),
    #    }

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    fields = [
        'cr',
        'cr_reg_date',
        'full_en_name',
        'full_ar_name',
        'license_no',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'applicant_id',
        'user_id',
        # 'cr_doc',
        # 'bank_statement_doc',
        # 'lmra_agreement'
        ]

    def form_valid(self, form):
        if form.instance.applicant_id:
            if form.instance.applicant.user_id == self.request.user:
                form.instance.user_id = self.request.user
            else:
                messages.warning(self.request, f'You are not allowed to update this record')
        return super().form_valid(form)

    def test_func(self):
        organization = self.get_object()
        if self.request.user == organization.applicant_id.user_id:
            return True
        return False

class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    success_url = '/organization'

    def test_func(self):
        organization = self.get_object()
        if self.request.user == organization.applicant_id.user_id:
            return True
        return False



class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'app/application.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'applications'
    # ordering = ['-date_posted']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return super(ApplicationListView, self).get_queryset().filter(user_id=self.request.user)
        else:
            return super(ApplicationListView, self).get_queryset()

class ApplicationDetailView(DetailView):
    model = Application

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    
    model = Application
    fields = [
        'org_id',
        # 'app_no',
        'app_date',
        'app_type',
        # 'app_status',
        'activty_type',
        'financial_guarantee',
        'financial_guarantee_expiry_date'
        # 'signature',
        # 'signature_date',
        # 'rent_doc',
        # 'ewa_bill_doc',
        # 'moh_approval_cert',
        # 'mol_approval_cert',
        # 'employment_office_receipt',
        # 'license_cancelication_doc',
        # 'bank_announcement_doc',
        # 'emp_id',
        # 'emp_approval_date',
        
        ]

    def form_valid(self, form):
        if form.instance.applicant_id.has_application:
            messages.warning(self.request, _('This applicant either received the license or has an application on going'))
            return False

        form.instance.user_id = self.request.user
        form.instance.app_no = 'Draft Application'
        form.instance.app_date = datetime.datetime.now().date()
        form.instance.app_status = 'Draft'
        form.instance.applicant_id.has_application = True
        return super(ApplicationCreateView, self).form_valid(form)

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = [
        'app_no',
        'app_date',
        # 'app_type',
        'app_status',
        # 'activty_type',
        # 'financial_guarantee',
        # 'financial_guarantee_expiry_date',
        # 'signature',
        # 'signature_date',
        # 'rent_doc',
        # 'ewa_bill_doc',
        # 'moh_approval_cert',
        # 'mol_approval_cert',
        # 'employment_office_receipt',
        # 'license_cancelication_doc',
        # 'bank_announcement_doc',
        # 'emp_id',
        # 'emp_approval_date',
        # 'org_id'
        ]

    def form_valid(self, form):
        # form.instance.user_id = self.request.user
        # This is general workflow

        if form.instance.applicant_id.cpr_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your CPR')
            return False

        if form.instance.applicant_id.passport_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your Passport')
            return False

        if not form.instance.applican_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return False
        
        # this condition to set the applicant ability to apply fot another application in future
        if 'cancel-btn' in self.data:
            form.instance.app_status = 'Cancelled by applicant'
            form.instance.applicant_id.has_application = False

        if form.instance.app_status == 'Draft':
            # generate numbers
            form.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(form.instance.id)
            form.instance.app_status = "Submitted"

        elif form.instance.app_status == 'Submitted':
            form.instance.app_status = 'Violations Verification'

        elif form.instance.app_status == 'Violations Verification':
            form.instance.app_status = 'Request Statements'

        elif form.instance.app_status == 'Request Statements':
            form.instance.app_status = 'Inital Approval'

        elif form.instance.app_status == 'Inital Approval':
            form.instance.app_status = 'Verify Documents'

        elif form.instance.app_status == 'Verify Documents':
            form.instance.app_status = 'Issue the Decision'
        
        elif form.instance.app_status == 'Issue the Decision':
            if form.instance.app_type == 'new' or form.instance.app_type == 'modify':
                form.instance.app_status = 'Paying New/Modify Fees'
            elif form.instance.app_type == 'renew':
                form.instance.app_status = 'Paying Renewal Fees'
            elif form.instance.app_type == 'license_cancel':
                form.instance.app_status = 'Paying Cancellation Fees'
            else:
                form.instance.app_status = 'Application Cancellation Fees'
        else:
            form.instance.app_status = 'Receive License'
            if form.instance.app_type == 'license_cancel':
                form.instance.app_status = 'Cancelled License'

        
        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.org_id.user_id:
            return True
        elif self.request.user.is_staff:
            # if application.app_status == 'draft':
            #     application.app_date.disabled = True
            return True
        else:
            return False

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    success_url = '/application'

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.org_id.user_id:
            return True
        return False