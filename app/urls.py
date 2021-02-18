from django.urls import path
from . import views

from .views import (
    ApplicantListView,
    ApplicantDetailView,
    ApplicantCreateView,
    ApplicantUpdateView,
    ApplicantDeleteView,

    OrganizationListView,
    OrganizationDetailView,
    OrganizationCreateView,
    OrganizationUpdateView,
    OrganizationDeleteView,
    
    ApplicationListView,
    ApplicationDetailView,
    ApplicationCreateView,
    ApplicationUpdateView,
    ApplicationDeleteView,
)

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    
    path('applicant/', ApplicantListView.as_view(), name='applicant-list'),
    path('applicant/<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    path('applicant/new/', ApplicantCreateView.as_view(), name='applicant-create'),
    path('applicant/<int:pk>/update/', ApplicantUpdateView.as_view(), name='applicant-update'),
    path('applicant/<int:pk>/delete/', ApplicantDeleteView.as_view(), name='applicant-delete'),

    path('organization/', OrganizationListView.as_view(), name='organization-list'),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization/new/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organization/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),

    path('application/', ApplicationListView.as_view(), name='application-list'),
    path('application/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('application/new/', ApplicationCreateView.as_view(), name='application-create'),
    path('application/<int:pk>/update/', ApplicationUpdateView.as_view(), name='application-update'),
    path('application/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application-delete'),
]