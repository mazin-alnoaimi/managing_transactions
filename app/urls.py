from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),

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
    path('application/<int:id>/delete/',views.application_delete,name='application_delete'),
]