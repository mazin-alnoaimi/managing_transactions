from django import forms
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from .models import (Applicant, Organization, Application)

gender_list = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

qualification_list = (
        ('secondary_school', 'Secondary School'),
        ('diploma', 'Diploma'),
        ('bsc', 'BSc'),
        ('high_diploma', 'High Diploma'),
        ('master', 'Master'),
        ('phd', 'PhD')
    )

nationality_list = (
        ('none', 'Select your nationality'),
        ('bahraini', 'Bahraini'),
        ('non_bahraini', 'None Bahraini')
    )

class ApplicantForm(forms.ModelForm):

    user_id = forms.ModelChoiceField(User.objects.all())

    class Meta:
        model = Applicant
        fields = (
            'cpr',
            'cpr_expiry_date',
            'fullname',
            'gender',
            'nationality',
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
            'passport_expiry_date'
        )


    def clean(self):
        cleaned_data = super().clean()
        cpr_expiry_date = cleaned_data.get("cpr_expiry_date")
        passport_expiry_date = cleaned_data.get("passport_expiry_date")

        if cpr_expiry_date <= datetime.datetime.now().date():
            self.add_error('cpr_expiry_date', "Please renew your CPR ")

        if passport_expiry_date <= datetime.datetime.now().date():
            self.add_error('passport_expiry_date', "Please renew your Passport")

        # form.instance.user_id = self.request.user
        # return super(ApplicantForm, self).form_valid(form)

class OrganizationForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(User.objects.all())
    applicant_id = forms.ModelChoiceField(Applicant.objects.all())

    class Meta:
        model = Organization
        fields = (
            'cr',
            'cr_reg_date',
            'full_en_name',
            'license_no',
            'flat_no',
            'building_no',
            'road_no',
            'area',
            'contact1',
            'contact2',
            'email',
            'applicant_id',
            'user_id'
        )

class ApplicationForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(User.objects.all())
    applicant_id = forms.ModelChoiceField(Applicant.objects.all())

    class Meta:
        model = Application
        fields = (
            'app_no',
            'app_date',
            'app_type',
            'app_status',
            'activty_type',
            'financial_guarantee',
            'financial_guarantee_expiry_date',
            # Company Details ---- Start
            'cr',
            'cr_reg_date',
            'full_en_name',
            'license_no',
            'license_expiry_date',
            'flat_no',
            'building_no',
            'road_no',
            'area',
            'contact1',
            'contact2',
            'email',
            # Company Details ---- End
            # Female Accommodation ---- Start
            'fh_flat_no',
            'fh_building_no',
            'fh_road_no',
            'fh_area',
            'fh_contact1',
            'fh_contact2',
            # Female Accommodation ---- End
            'staff_comments',
            'manager_comments',
            'intial_approval',
            'user_id',
            'applicant_id'
        )

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        if self.fields['app_type'].initial == 'Initial Approval':
            self.fields['cr'].widget = forms.HiddenInput()
            self.fields['cr_reg_date'].widget = forms.HiddenInput()
            self.fields['full_en_name'].widget = forms.HiddenInput()
            self.fields['license_no'].widget = forms.HiddenInput()
            self.fields['license_expiry_date'].widget = forms.HiddenInput()
            self.fields['flat_no'].widget = forms.HiddenInput()
            self.fields['building_no'].widget = forms.HiddenInput()
            self.fields['road_no'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['contact1'].widget = forms.HiddenInput()
            self.fields['contact2'].widget = forms.HiddenInput()
            self.fields['fh_flat_no'].widget = forms.HiddenInput()
            self.fields['fh_building_no'].widget = forms.HiddenInput()
            self.fields['fh_road_no'].widget = forms.HiddenInput()
            self.fields['fh_area'].widget = forms.HiddenInput()
            self.fields['fh_contact1'].widget = forms.HiddenInput()
            self.fields['fh_contact2'].widget = forms.HiddenInput()

            #open for update an exist record(instance)
            if self.instance.id:
                if self.instance.app_status == 'Submitted':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['intial_approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.fields['app_status'].initial == 'Draft':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['intial_approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
            #open new form for entering new date -- no instance exist
            elif self.fields['app_status'].initial == 'Draft':
                self.fields['staff_comments'].widget = forms.HiddenInput()
                self.fields['manager_comments'].widget = forms.HiddenInput()
                self.fields['intial_approval'].widget = forms.HiddenInput()
                self.fields['financial_guarantee'].widget = forms.HiddenInput()
                self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        applicant_id = cleaned_data.get("applicant_id")

        if applicant_id.has_application:
            messages.warning(self.request, _('This applicant either received the license or has an application on going'))
            self.add_error('applicant_id', "Application Exist")

    def save(self, *args, **kwargs):
        if self.fields['app_type'].initial == 'Initial Approval':
            # self.user_id = self.request.user

            if self.instance.id:  # if true then this is update form
                if self.instance.app_status == 'Draft':
                    self.instance.app_status = "Submitted"
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)

                elif self.instance.app_status == 'Submitted':
                    self.instance.app_status = 'Violations Verification'

                elif self.instance.app_status == 'Violations Verification':
                    self.instance.app_status = 'Request Statements'

                elif self.instance.app_status == 'Request Statements':
                    self.instance.app_status = 'Review Documents'

                elif self.instance.app_status == 'Review Documents':
                    self.instance.app_status = 'Request Manager Approval/Reject'

                elif self.instance.app_status == 'Request Manager Approval/Reject':
                    if self.instance.intial_approval == 'approve':
                        self.instance.app_status = 'Initial Approval'
                    else:
                        self.instance.app_status = 'Rejected'

        elif self.fields['app_type'].initial == 'Final Approval':
            # self.user_id = self.request.user

            if self.instance.id:  # if true then this is update form
                if self.instance.app_status == 'Draft':
                    self.instance.app_status = "Submitted"
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)

                elif self.instance.app_status == 'Submitted':
                    self.instance.app_status = 'Verify Documents'

                elif self.instance.app_status == 'Verify Documents':
                    self.instance.app_status = 'Verify Requirements'

                elif self.instance.app_status == 'Verify Requirements':
                    self.instance.app_status = 'Issue the Decision'

                elif self.instance.app_status == 'Issue the Decision':
                    self.instance.app_status = 'Payment Fees'

                elif self.instance.app_status == 'Payment Fees':
                    self.instance.app_status = 'Request Manager Approval/Reject'

                elif self.instance.app_status == 'Request Manager Approval/Reject':
                    if self.instance.intial_approval == 'approve':
                        self.instance.app_status = 'Final Approval'
                    else:
                        self.instance.app_status = 'Rejected'

        elif self.fields['app_type'].initial == 'Renewal License':
            # self.user_id = self.request.user

            if self.instance.id:  # if true then this is update form
                if self.instance.app_status == 'Draft':
                    self.instance.app_status = "Submitted"
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)

                elif self.instance.app_status == 'Submitted':
                    self.instance.app_status = 'Verify Documents'

                elif self.instance.app_status == 'Verify Documents':
                    self.instance.app_status = 'Verify Statements'

                elif self.instance.app_status == 'Verify Statements':
                    self.instance.app_status = 'Issue the Decision'

                elif self.instance.app_status == 'Issue the Decision':
                    self.instance.app_status = 'Payment Fees'

                elif self.instance.app_status == 'Payment Fees':
                    self.instance.app_status = 'Request Manager Approval/Reject'

                elif self.instance.app_status == 'Request Manager Approval/Reject':
                    if self.instance.intial_approval == 'approve':
                        self.instance.app_status = 'Renewal license Approval'
                    else:
                        self.instance.app_status = 'Rejected'

        elif self.fields['app_type'].initial == 'Cancel License':
            # self.user_id = self.request.user

            if self.instance.id:  # if true then this is update form
                if self.instance.app_status == 'Draft':
                    self.instance.app_status = "Submitted"
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)

                elif self.instance.app_status == 'Submitted':
                    self.instance.app_status = 'Verify Documents'

                elif self.instance.app_status == 'Verify Documents':
                    self.instance.app_status = 'Verify Statements'

                elif self.instance.app_status == 'Verify Statements':
                    self.instance.app_status = 'Issue the Decision'

                elif self.instance.app_status == 'Issue the Decision':
                    self.instance.app_status = 'Request Manager Approval/Reject'

                elif self.instance.app_status == 'Request Manager Approval/Reject':
                    if self.instance.intial_approval == 'approve':
                        self.instance.app_status = 'Cancel License Approval'
                    else:
                        self.instance.app_status = 'Rejected'

        super().save(*args, **kwargs)