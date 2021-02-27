from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),

    # path('applicant/', ApplicantListView.as_view(), name='applicant-list'),
    # path('applicant/<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    # path('applicant/new/', ApplicantCreateView.as_view(), name='applicant-create'),
    # path('applicant/<int:pk>/update/', ApplicantUpdateView.as_view(), name='applicant-update'),
    # path('applicant/<int:pk>/delete/', ApplicantDeleteView.as_view(), name='applicant-delete'),

    path('applicant/list/',views.applicant_list,name='applicant_list'),
    path('applicant/new/', views.applicant_form,name='applicant_insert'),
    path('applicant/<int:id>/update/', views.applicant_form,name='applicant_update'),
    path('applicant/<int:id>/delete/',views.applicant_delete,name='applicant_delete'),

    path('organization/list/',views.organization_list,name='organization_list'),
    path('organization/new/', views.organization_form,name='organization_insert'),
    path('organization/<int:id>/update/', views.organization_form,name='organization_update'),
    path('organization/<int:id>/delete/',views.organization_delete,name='organization_delete'),

    path('application/list/',views.application_list,name='application_list'),
    path('application/new/', views.application_form,name='application_insert'),
    path('application/<int:id>/update/', views.application_form,name='application_update'),
    path('application/<int:id>/delete/',views.application_delete,name='application_delete')

    # path('organization/', OrganizationListView.as_view(), name='organization-list'),
    # path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    # path('organization/new/', OrganizationCreateView.as_view(), name='organization-create'),
    # path('organization/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization-update'),
    # path('organization/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),


    # path('application/', ApplicationListView.as_view(), name='application-list'),
    # path('application/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    # path('application/new/', ApplicationCreateView.as_view(), name='application-create'),

    # path('application/new_intial_approval/', ApplicationIntialApprovalCreateView.as_view(), name='application-intial-approval-create'),
    # path('application/new_final_approval/', ApplicationFinalApprovalCreateView.as_view(), name='application-final-approval-create'),
    # path('application/new_renewal/', ApplicationRenewalCreateView.as_view(), name='application-renewal-create'),
    # path('application/new_revoke/', ApplicationRevokeCreateView.as_view(), name='application-revoke-create'),

    # path('application/<int:pk>/update/', ApplicationUpdateView.as_view(), name='application-update'),
    # path('application/<int:pk>/update_intial_approval/', ApplicationIntialApprovalUpdateView.as_view(), name='application-intial-approval-update'),
    # path('application/<int:pk>/update_final_approval/', ApplicationFinalApprovalUpdateView.as_view(), name='application-final-approval-update'),
    # path('application/<int:pk>/update_renewal/', ApplicationRenewalUpdateView.as_view(), name='application-renewal-update'),
    # path('application/<int:pk>/update_revoke/', ApplicationRevokeUpdateView.as_view(), name='application-revoke-update'),

    # path('application/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application-delete'),
]