from django.shortcuts import render, redirect, reverse
from django import forms
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView
)

from django.urls import reverse_lazy

from .forms import (ApplicantForm, OrganizationForm, ApplicationForm)

from .models import (Applicant, Organization, Application)


def home(request):
    return render(request, 'app/home.html') #, context)

def about(request):
    return render(request, 'app/about.html', {'title': 'About'})

def applicant_list(request):
    context = {'applicant_list': Applicant.objects.all()}
    return render(request, "app/applicant_list.html", context)

def applicant_form(request, id=0):
    print("====================================================================== 0")
    if request.method == "GET":
        print("====================================================================== 1")
        if id == 0:
            print("====================================================================== 2")
            form = ApplicantForm()
        else:
            print("====================================================================== 4")
            applicant = Applicant.objects.get(pk=id)
            form = ApplicantForm(instance=applicant)
        print("====================================================================== 5")
        return render(request, "app/applicant_form.html", {'form': form})
    else:
        print("====================================================================== 6")
        if id == 0:
            print("====================================================================== 7")
            form = ApplicantForm(request.POST)
        else:
            print("====================================================================== 8")
            applicant = Applicant.objects.get(pk=id)
            form = ApplicantForm(request.POST,instance= applicant)

        if form.is_valid():
            print("====================================================================== 9")
            form.save()
        else:
            print("====================================================================== 10")
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
    print("====================================================================== 0")
    if request.method == "GET":
        print("====================================================================== 1")
        if id == 0:
            print("====================================================================== 2")
            form = OrganizationForm()
        else:
            print("====================================================================== 4")
            organization = Organization.objects.get(pk=id)
            form = OrganizationForm(instance=organization)
        print("====================================================================== 5")
        return render(request, "app/organization_form.html", {'form': form})
    else:
        print("====================================================================== 6")
        if id == 0:
            print("====================================================================== 7")
            form = OrganizationForm(request.POST)
        else:
            print("====================================================================== 8")
            organization = Organization.objects.get(pk=id)
            form = OrganizationForm(request.POST,instance= organization)

        if form.is_valid():
            print("====================================================================== 9")
            form.save()
        else:
            print("====================================================================== 10")
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
    print("====================================================================== 0")
    if request.method == "GET":
        print("====================================================================== 1")
        if id == 0:
            print("====================================================================== 2")
            form = ApplicationForm()
        else:
            print("====================================================================== 4")
            application = Application.objects.get(pk=id)
            form = ApplicationForm(instance=application)
        print("====================================================================== 5")
        return render(request, "app/application_form.html", {'form': form})
    else:
        print("====================================================================== 6")
        if id == 0:
            print("====================================================================== 7")
            form = ApplicationForm(request.POST)
            if form.instance.applicant_id.has_application:
                messages.warning(self.request, _('This applicant either received the license or has an application on going'))
                return super().form_invalid(form)

            if not form.instance.applicant_id.nationality == 'bahraini':
                messages.warning(self.request, f'This application accept Bahrain nationality only')
                return super().form_invalid(form)
        else:
            print("====================================================================== 8")
            application = Application.objects.get(pk=id)
            form = ApplicationForm(request.POST,instance= application)

        if form.is_valid():
            print("====================================================================== 9")
            form.user_id = request.user

            form.save()
        else:
            print("====================================================================== 10")
            return render(request, "app/application_form.html", {'form': form})
        return redirect('/application/list')

def application_delete(request,id):
    application = Application.objects.get(pk=id)
    application.delete()
    return redirect('/application/list')






class ApplicationCreateView(LoginRequiredMixin, CreateView):

    model = Application
    fields = [
        'org_id',
        # 'app_no',
        'app_date',
        'app_type',
        # 'app_status',
        'activty_type',
        'license_no',
        'license_expiry_date',
        # 'financial_guarantee',
        # 'financial_guarantee_expiry_date'
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
        # check if applicant has an application or has active license
        if form.instance.applicant_id.has_application:
            messages.warning(self.request, _('This applicant either received the license or has an application on going'))
            return super(ApplicationCreateView, self).form_invalid(form)

        #renewal condition
        if form.instance.app_type == 'renewal':
            #system will check if user enter the expiry date or not
            if form.instance.license_expiry_date: # if yes ... do the math
                ex_2m_date = form.instange.license_expiry_date + relativedelta(months=-2)
                ex_1m_date = form.instange.license_expiry_date + relativedelta(months=-1)
                if not(ex_2m_date <= form.instance.app_date <= ex_1m_date):
                    messages.warning(self.request, _('Please contact the concern department..'))
                    return super(ApplicationCreateView, self).form_invalid(form)
            else:
                messages.warning(self.request, _('Please enter the license expiry date'))
                return super(ApplicationCreateView, self).form_invalid(form)

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
        if form.instance.applicant_id.cpr_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your CPR')
            return super(ApplicantUpdateView, self).form_invalid(form)

        if form.instance.applicant_id.passport_expiry_date <= datetime.datetime.now().date():
            messages.warning(self.request, f'Please renew your Passport')
            return super(ApplicantUpdateView, self).form_invalid(form)

        if not form.instance.applicant_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return super(ApplicantUpdateView, self).form_invalid(form)

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
            form.insp_status = 'Verify Documents'

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


# Intial Approval
class ApplicationIntialApprovalCreateView(LoginRequiredMixin, CreateView):

    model = Application
    fields = [
        'cr',
        'activty_type',
        'applicant_id',
        ]

    def form_valid(self, form):

        form.instance.user_id = self.request.user
        form.instance.app_no = 'Draft Application'
        form.instance.app_date = datetime.datetime.now().date()
        form.instance.app_status = 'Draft'
        form.instance.app_type = 'Intial Approval'

        #system should pass the applicant number
        if form.instance.applicant_id:
            # check if applicant has an application or has active license
            if form.instance.applicant_id.has_application:
                messages.warning(self.request, _('This applicant either received the license or has an application on going'))
                return super(ApplicationIntialApprovalCreateView, self).form_invalid(form)
            else:
                form.instance.applicant_id.has_application = True
        else:
            messages.warning(self.request, _('Please select a applicant..'))
            return super(ApplicationIntialApprovalCreateView, self).form_invalid(form)

        return super(ApplicationIntialApprovalCreateView, self).form_valid(form)

class ApplicationIntialApprovalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = [
        'cr',
        'app_date',
        'app_status',
        'staff_comments',
        'manager_comments',
        'intial_approval',
        ]

    def form_valid(self, form):
        if not form.instance.applicant_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return super(ApplicationIntialApprovalUpdateView, self).form_invalid(form)

        # this condition to set the applicant ability to apply fot another application in future
        # if 'cancel-btn' in self.data:
        #     form.instance.app_status = 'Cancelled by applicant'
        #     form.instance.applicant_id.has_application = False

        if form.instance.app_status == 'Draft':
            # generate numbers
            form.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(form.instance.id)
            form.instance.app_status = "Submitted"

        elif form.instance.app_status == 'Submitted':
            form.instance.app_status = 'Violations Verification'

        elif form.instance.app_status == 'Violations Verification':
            form.instance.app_status = 'Request Statements'

        elif form.instance.app_status == 'Request Statements':
            form.instance.app_status = 'Review Documents'

        elif form.instance.app_status == 'Review Documents':
            form.instance.app_status = 'Request Manager Approval/Reject'

        elif form.instance.app_status == 'Request Manager Approval/Rejcet':
            if form.instance.intial_approval == 'approve':
                form.instance.app_status = 'Intial Approval'
            else:
                form.instance.app_status = 'Rejected'

        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.user_id:
            return True
        elif self.request.user.is_staff:
            return True
        else:
            return False


# Final Approval
class ApplicationFinalApprovalCreateView(LoginRequiredMixin, CreateView):

    model = Application
    fields = [
        'cr',
        'full_en_name',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'activty_type',
        'financial_guarantee',
        'financial_guarantee_expiry_date',
        'cr_rent_doc',
        'cr_ewa_bill_doc',
        'cert1_doc',
        'cert2_doc',
        'cert3_doc',
        'employment_office_receipt',
        'fh_flat_no',
        'fh_building_no',
        'fh_road_no',
        'fh_area',
        'fh_contact1',
        'fh_contact2',
        'applicant_id',
        ]

    def form_valid(self, form):

        form.instance.user_id = self.request.user
        form.instance.app_no = 'Draft Application'
        form.instance.app_date = datetime.datetime.now().date()
        form.instance.app_status = 'Draft'
        form.instance.app_type = 'Final Approval'

        #system should pass the applicant number
        if form.instance.applicant_id:
            # check if applicant has an application or has active license
            if form.instance.applicant_id.has_application:
                messages.warning(self.request, _('This applicant either received the license or has an application on going'))
                return super(ApplicationFinalApprovalCreateView, self).form_invalid(form)
            else:
                form.instance.applicant_id.has_application = True
        else:
            messages.warning(self.request, _('Please select a applicant..'))
            return super(ApplicationFinalApprovalCreateView, self).form_invalid(form)

        return super(ApplicationFinalApprovalCreateView, self).form_valid(form)

class ApplicationFinalApprovalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = [
        'cr',
        'full_en_name',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'activty_type',
        'financial_guarantee',
        'financial_guarantee_expiry_date',
        'cr_rent_doc',
        'cr_ewa_bill_doc',
        'cert1_doc',
        'cert2_doc',
        'cert3_doc',
        'employment_office_receipt',
        'fh_flat_no',
        'fh_building_no',
        'fh_road_no',
        'fh_area',
        'fh_contact1',
        'fh_contact2',
        'applicant_id',
        ]

    def form_valid(self, form):
        if not form.instance.applicant_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return super(ApplicationFinalApprovalUpdateView, self).form_invalid(form)

        if form.instance.app_status == 'Draft':
            # generate numbers
            form.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(form.instance.id)
            form.instance.app_status = "Submitted"

        elif form.instance.app_status == 'Submitted':
            form.instance.app_status = 'Verify Documents'

        elif form.instance.app_status == 'Verify Documents':
            form.instance.app_status = 'Verify Requirements'

        elif form.instance.app_status == 'Verify Requirements':
            form.instance.app_status = 'Issue the Decision'

        elif form.instance.app_status == 'Issue the Decision':
            form.instance.app_status = 'Payment Fees'

        elif form.instance.app_status == 'Request Manager Approval/Rejcet':
            if form.instance.intial_approval == 'approve':
                form.instance.app_status = 'Receive License Certificate'
            else:
                form.instance.app_status = 'Rejected'

        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.user_id:
            return True
        elif self.request.user.is_staff:
            return True
        else:
            return False


# Renewal License
class ApplicationRenewalCreateView(LoginRequiredMixin, CreateView):

    model = Application
    fields = [
        'cr',
        'full_en_name',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'activty_type',
        'financial_guarantee',
        'financial_guarantee_expiry_date',
        'cr_rent_doc',
        'cr_ewa_bill_doc',
        'cert1_doc',
        'cert2_doc',
        'cert3_doc',
        'employment_office_receipt',
        'fh_flat_no',
        'fh_building_no',
        'fh_road_no',
        'fh_area',
        'fh_contact1',
        'fh_contact2',
        'applicant_id',
        ]

    def form_valid(self, form):

        form.instance.user_id = self.request.user
        form.instance.app_no = 'Draft Application'
        form.instance.app_date = datetime.datetime.now().date()
        form.instance.app_status = 'Draft'
        form.instance.app_type = 'Renewal License'

        #system should pass the applicant number
        if form.instance.applicant_id:
            # check if applicant has an application or has active license
            if form.instance.applicant_id.has_application:
                messages.warning(self.request, _('This applicant either received the license or has an application on going'))
                return super(ApplicationRenewalCreateView, self).form_invalid(form)
            else:
                form.instance.applicant_id.has_application = True
        else:
            messages.warning(self.request, _('Please select a applicant..'))
            return super(ApplicationRenewalCreateView, self).form_invalid(form)

        return super(ApplicationRenewalCreateView, self).form_valid(form)

class ApplicationRenewalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = [
        'cr',
        'full_en_name',
        'flat_no',
        'building_no',
        'road_no',
        'area',
        'contact1',
        'contact2',
        'email',
        'activty_type',
        'financial_guarantee',
        'financial_guarantee_expiry_date',
        'cr_rent_doc',
        'cr_ewa_bill_doc',
        'cert1_doc',
        'cert2_doc',
        'cert3_doc',
        'employment_office_receipt',
        'fh_flat_no',
        'fh_building_no',
        'fh_road_no',
        'fh_area',
        'fh_contact1',
        'fh_contact2',
        'applicant_id',
        ]

    def form_valid(self, form):
        if not form.instance.applicant_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return super(ApplicationRenewalUpdateView, self).form_invalid(form)

        if form.instance.app_status == 'Draft':
            # generate numbers
            form.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(form.instance.id)
            form.instance.app_status = "Submitted"

        elif form.instance.app_status == 'Submitted':
            form.instance.app_status = 'Violations Verification'

        elif form.instance.app_status == 'Violations Verification':
            form.instance.app_status = 'Request Statements'

        elif form.instance.app_status == 'Request Statements':
            form.instance.app_status = 'Review Documents'

        elif form.instance.app_status == 'Review Documents':
            form.instance.app_status = 'Issue the Decision'

        elif form.instance.app_status == 'Issue the Decision':
            form.instance.app_status = 'Payment Fees'

        elif form.instance.app_status == 'Payment Fees':
            form.instance.app_status = 'Request Manager Approval/Rejcet'

        elif form.instance.app_status == 'Request Manager Approval/Rejcet':
            if form.instance.intial_approval == 'approve':
                form.instance.app_status = 'Receive License Certificate'
            else:
                form.instance.app_status = 'Rejected'

        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.user_id:
            return True
        elif self.request.user.is_staff:
            return True
        else:
            return False


# Revoke License
class ApplicationRevokeCreateView(LoginRequiredMixin, CreateView):

    model = Application
    fields = [
        'cr',
        'full_en_name',
        'license_no',
        'license_expiry_date',
        'applicant_id',
        ]

    def form_valid(self, form):

        form.instance.user_id = self.request.user
        form.instance.app_no = 'Draft Application'
        form.instance.app_date = datetime.datetime.now().date()
        form.instance.app_status = 'Draft'
        form.instance.app_type = 'Revoke License'

        #system should pass the applicant number
        if form.instance.applicant_id:
            # check if applicant has an application or has active license
            if form.instance.applicant_id.has_application:
                messages.warning(self.request, _('This applicant either received the license or has an application on going'))
                return super(ApplicationRevokeCreateView, self).form_invalid(form)
            else:
                form.instance.applicant_id.has_application = True
        else:
            messages.warning(self.request, _('Please select a applicant..'))
            return super(ApplicationRevokeCreateView, self).form_invalid(form)

        return super(ApplicationRevokeCreateView, self).form_valid(form)

class ApplicationRevokeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = [
        'cr',
        'full_en_name',
        'license_no',
        'license_expiry_date',
        'applicant_id',
        ]

    def form_valid(self, form):
        if not form.instance.applicant_id.nationality == 'bahraini':
            messages.warning(self.request, f'This application accept Bahrain nationality only')
            return super(ApplicationRevokeUpdateView, self).form_invalid(form)

        if form.instance.app_status == 'Draft':
            # generate numbers
            form.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(form.instance.id)
            form.instance.app_status = "Submitted"

        elif form.instance.app_status == 'Submitted':
            form.instance.app_status = 'Violations Verification'

        elif form.instance.app_status == 'Violations Verification':
            form.instance.app_status = 'Request Statements'

        elif form.instance.app_status == 'Request Statements':
            form.instance.app_status = 'Review Documents'

        elif form.instance.app_status == 'Review Documents':
            form.instance.app_status = 'Issue the Decision'

        elif form.instance.app_status == 'Issue the Decision':
            form.instance.app_status = 'Payment Fees'

        elif form.instance.app_status == 'Payment Fees':
            form.instance.app_status = 'Request Manager Approval/Rejcet'

        elif form.instance.app_status == 'Request Manager Approval/Rejcet':
            if form.instance.intial_approval == 'approve':
                form.instance.app_status = 'Receive License Certificate'
            else:
                form.instance.app_status = 'Rejected'

        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.user_id:
            return True
        elif self.request.user.is_staff:
            return True
        else:
            return False


class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    success_url = '/application'

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.user_id:
            return True
        return False