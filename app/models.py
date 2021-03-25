import datetime
from django.db import models
from django.utils.translation import gettext as _
# from django.urls import reverse
# from django.utils import timezone
from django.contrib.auth.models import User

class Applicant(models.Model):

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
        ('phd', 'PhD'),
    )

    nationality_list = (
        ('none', 'Select your nationality'),
        ('bahraini', 'Bahraini'),
        ('non_bahraini', 'None Bahraini')
    )

    cpr = models.CharField(_("CPR No"), max_length=9)
    cpr_expiry_date = models.DateField(_("CPR Expire Date"), auto_now=False, auto_now_add=False)
    passport_expiry_date = models.DateField(_("Passport Expire Date"), auto_now=False, auto_now_add=False)
    fullname = models.CharField(_("Full Name"), max_length=100)
    nationality =  models.CharField(_("Nationality"), max_length=50, choices=nationality_list, default='none')
    gender = models.CharField(_("Gender"), max_length=10, choices=gender_list)
    qualification = models.CharField(_("Qualification"), max_length=50, choices=qualification_list)
    occupcation = models.CharField(_("Occupation"), max_length=50)
    has_application = models.BooleanField(_("Has Applicatino on process"), default=False)

    # Address fields
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Mobile"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    # Applicant Uploaded Doc fields
    cpr_doc = models.FileField(_("CPR Doc"), upload_to='doc_library', max_length=100)
    passport_doc = models.FileField(_("Passport Doc"), upload_to='doc_library', max_length=100)
    behavior_cert_doc = models.FileField(_("Behavior Certificate Doc"), upload_to='doc_library', max_length=100)
    bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    is_10000_exist = models.BooleanField(_("Is 10000 BD exist in Applicant Bank Statement"), default=False)

    def __str__(self):
        return self.cpr + ' --- ' + self.fullname

class Organization(models.Model):

    cr = models.CharField(_("CR No"), max_length=50, blank=True)
    cr_reg_date = models.DateField(_("Registration Date"), auto_now=False, auto_now_add=False)
    full_en_name = models.CharField(_("Commercial Eng Name"), max_length=250, blank=True)
    license_no = models.CharField(_("License No"), max_length=50, blank=True)
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Fax"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)

    #Owner of compnay
    applicant_id = models.ForeignKey(Applicant, verbose_name=_(""), on_delete=models.CASCADE, blank=True)

    #User who creates this record in the system
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE, blank=True)

    # cr_doc = models.FileField(_("CR Doc"), upload_to='doc_library', max_length=100)
    # bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    # lmra_agreement = models.FileField(_("LMRA Agreement"), upload_to='doc_library', max_length=100)

    def __str__(self):
        return self.full_en_name

class Application(models.Model):

    activity_type_list = (
        ('demostic', 'Demostic Labour Employment'),
        ('foreign', 'Foreign Labour Employement'),
        ('local', 'Bahraini Labour Employment')
    )

    financial_guarantee_list = (
        ('manager_cheque', 'Manager Cheque'),
        ('bank_guarantee', 'Bank Guarantee')
    )

    intial_approval_list = (
        ('approve', 'Approve'),
        ('reject', 'Reject')
    )

    app_type_list = (
        ('initial','Initial Approval'),
        ('final','Final Approval'),
        ('renew','Renewal License'),
        ('cancel','Cancel License')
    )

    app_no = models.CharField(_("Application No"), max_length=50, default='Draft Application')
    app_date = models.DateField(_("Application Date"), default=datetime.date.today)
    app_type = models.CharField(_("Application Type"), max_length=50, choices=app_type_list)
    app_status_index = models.IntegerField(_("Status No"), default=0)
    app_current_status = models.CharField(_("Status"), max_length=50, default='Draft')
    app_next_status = models.CharField(_("Status"), max_length=50, default='Draft')
    activty_type = models.CharField(_("Activity Type"), max_length=50, choices=activity_type_list)
    staff_comments = models.TextField(_("Comments"), blank=True)
    manager_comments = models.TextField(_("Manager Comments"), blank=True)
    approval = models.CharField(_("Manager Decision"), max_length=50, choices=intial_approval_list, blank=True)

    financial_guarantee = models.CharField(_("Financial Guarantee"), max_length=50, choices=financial_guarantee_list, blank=True)
    financial_guarantee_expiry_date = models.DateField(_("Financial Guarantee Expiry Date"), null=True, blank=True)

    # start -- org details
    # will be updated by Layla
    cr = models.CharField(_("CR No"), max_length=50, blank=True)
    cr_reg_date = models.DateField(_("Registration Date"), null=True, blank=True)
    full_en_name = models.CharField(_("Commercial Eng Name"), max_length=250, blank=True)
    license_no = models.CharField(_("License No"), max_length=50, blank=True)
    license_expiry_date = models.DateField(_("License Expiry Date"), null=True, blank=True)
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Fax"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    # end -- org details

    # start -- female accomodation
    fh_flat_no = models.IntegerField(_("Flat No"), default=0)
    fh_building_no = models.IntegerField(_("Building No"), default=0)
    fh_road_no = models.IntegerField(_("Road No"), default=0)
    fh_area = models.CharField(_("Area"), max_length=50, blank=True)
    fh_contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    fh_contact2 = models.CharField(_("Fax"), max_length=50, blank=True)

    qsreq = models.IntegerField(_("Uploaded Documents"), default=0)
    qnreq = models.IntegerField(_("Org Required Documents"), default=1)
    dreq = models.FloatField(_("Adequacy of Requirements Level"), default=0)

    qsrec = models.IntegerField(_("Satisfying Recommendations"), default=0)
    qnrec = models.IntegerField(_("All Recommendations"), default=1)
    drec = models.FloatField(_("Adequacy of Recommendations Level"), default=0)

    #Attachments
    cr_doc = models.FileField(_("CR Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    lmra_agreement = models.FileField(_("LMRA Agreement"), upload_to='doc_library', max_length=100, null=True, blank=True)
    cert1_doc = models.FileField(_("MOIS Cert"), upload_to='doc_library', max_length=100, null=True, blank=True)
    cert2_doc = models.FileField(_("MOH Cert"), upload_to='doc_library', max_length=100, null=True, blank=True)
    cert3_doc = models.FileField(_("MOL Cert"), upload_to='doc_library', max_length=100, null=True, blank=True)
    cr_rent_doc = models.FileField(_("CR Rental Agreement Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    fh_rent_doc = models.FileField(_("Temp FH Rental Agreement Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    cr_ewa_bill_doc = models.FileField(_("CR EWA Bill Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    fh_ewa_bill_doc = models.FileField(_("Temp FH EWA Bill Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    employment_office_receipt = models.FileField(_("Employment Office Receipt"), upload_to='doc_library', max_length=100, null=True, blank=True)


    applicant_id = models.ForeignKey(Applicant, verbose_name=_(""), on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)


    def __str__(self):
        return self.app_no