from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils import timezone
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
    flat_no = models.IntegerField(_("Flat No"))
    building_no = models.IntegerField(_("Building No"))
    road_no = models.IntegerField(_("Road No"))
    area = models.CharField(_("Area"), max_length=50)
    contact1 = models.CharField(_("Phone"), max_length=50)
    contact2 = models.CharField(_("Mobile"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    # Applicant Uploaded Doc fields
    cpr_doc = models.FileField(_("CPR Doc"), upload_to='doc_library', max_length=100)
    passport_doc = models.FileField(_("Passport Doc"), upload_to='doc_library', max_length=100)
    behavior_cert_doc = models.FileField(_("Behavior Certificate Doc"), upload_to='doc_library', max_length=100)

    # Applicant Bank Related Fields
    bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    is_10000_exist = models.BooleanField(_("Is 10000 BD exist in Applicant Bank Statement"), default=False)

    class Meta:
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("applicant-list") #, kwargs={"pk": self.pk})

    def get_success_url(self):
        return reverse('applicant-list') #, args=(somethinguseful,))

class Organization(models.Model):

    cr = models.CharField(_("CR No"), max_length=50)
    cr_reg_date = models.DateField(_("Registration Date"), auto_now=False, auto_now_add=False)
    full_en_name = models.CharField(_("Commercial Eng Name"), max_length=250)
    full_ar_name = models.CharField(_("Commercial Arb Name"), max_length=250)
    license_no = models.CharField(_("License No"), max_length=50)
    flat_no = models.IntegerField(_("Flat No"))
    building_no = models.IntegerField(_("Building No"))
    road_no = models.IntegerField(_("Road No"))
    area = models.CharField(_("Area"), max_length=50)
    contact1 = models.CharField(_("Phone"), max_length=50)
    contact2 = models.CharField(_("Fax"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    applicant_id = models.ForeignKey(Applicant, verbose_name=_(""), on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    # cr_doc = models.FileField(_("CR Doc"), upload_to='doc_library', max_length=100) 
    # bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    # lmra_agreement = models.FileField(_("LMRA Agreement"), upload_to='doc_library', max_length=100)
    
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.full_en_name

    def get_absolute_url(self):
        return reverse("organization-list") #, kwargs={"pk": self.pk})


class Application(models.Model):

    app_type_list = (
        ('new', 'New'),
        ('renew', 'Renew'),
        ('modify', 'Modify'),
        ('license_cancel', 'License Cancellation')
    )

    app_status_list = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('verification', 'Violations Verification'),
        ('request_statement', 'Request Statements'),
        ('review_statement', 'Reviewing Statements'),
        ('initial_approval', 'Inital Approval'),
        ('verify_documents', 'Verify Documents'),
        ('issue_decision', 'Issue the Decision'),
        ('paying_fees', 'Paying Fees'),                                # for new and modify license applications
        ('paying_renewal_fees', 'Paying Renewal Fees'),                # for renewal license application
        ('paying_cancellation_fees', 'Paying Cancellation Fees'),      # for cancellation license application
        ('done', 'Receive License'),
        ('cancellarion_done', 'Cancel License'),
        ('app_cencel', 'Canceled by Applicant'),
    )

    activity_type_list = (
        ('demostic', 'Demostic Labour Employment'),
        ('foreign', 'Foreign Labour Employement'),
        ('local', 'Bahraini Labour Employment')
    )

    financial_guarantee_list = (
        ('manager_cheque', 'Manager Cheque'),
        ('bank_guarantee', 'Bank Guarantee')
    )
    app_no = models.CharField(_("Application No"), max_length=50)
    app_date = models.DateField(_("Application Date"), auto_now=False, auto_now_add=False)
    app_type = models.CharField(_("Application Type"), max_length=50, choices=app_type_list)
    app_status = models.CharField(_("Status"), max_length=50, default='draft')
    activty_type = models.CharField(_("Activity Type"), max_length=50, choices=activity_type_list)
    financial_guarantee = models.CharField(_("Financial Guarantee")
                                            , max_length=50, choices=financial_guarantee_list)
    financial_guarantee_expiry_date = models.DateField(_("Financial Guarantee Expiry Date")
                                                        , auto_now=False, auto_now_add=False)
    # signature = models.BinaryField(_("Signature"))
    # signature_date = models.DateField(_("Submit Date"), auto_now=False, auto_now_add=False)
    
    # rent_doc = models.FileField(_("Rental Agreement Doc"), upload_to='doc_library', max_length=100)
    # ewa_bill_doc = models.FileField(_("EWA Bill Doc"), upload_to='doc_library', max_length=100)
    # moh_approval_cert = models.FileField(_("MOH Approval Accomodation Certificate"), upload_to='doc_library', max_length=100)
    # mol_approval_cert = models.FileField(_("MOL Approval Certificate"), upload_to='doc_library', max_length=100)
    # employment_office_receipt = models.FileField(_("Employment Office Receipt"), upload_to='doc_library', max_length=100)
    # license_cancelication_doc = models.FileField(_("License Cancelication Doc"), upload_to='doc_library', max_length=100)
    # bank_announcement_doc = models.FileField(_("Bank Announcement Doc"), upload_to='doc_library', max_length=100)

    # emp_id = models.ForeignKey(User, verbose_name=_("Employee Name"), on_delete=models.CASCADE)   
    # emp_name = models.CharField(_('Approved By'), max_length=50) 
    # emp_approval_date = models.DateField(_("Approval Date"), auto_now=False, auto_now_add=False)
    org_id = models.ForeignKey(Organization, verbose_name=_("Organization Name"), on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Application")

    def __str__(self):
        return self.app_no

    def get_absolute_url(self):
        return reverse("application-list") #, kwargs={"pk": self.pk})

