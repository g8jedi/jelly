from django.urls import path

from . import views

app_name = 'human_resources'
urlpatterns = [
    # ex: /human-resources/create-employee
    path('create-employee/', views.CreateEmployeeView.as_view(), name='create-employee'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee-list/', views.EmployeeListView.as_view(), name='employee-list'),
    path('comprobante/<int:pk>/', views.ComprobanteDetailView.as_view(), name='comprobante-detail'),
    path('create-nomina/', views.CreateNominaView.as_view(), name='create-nomina'),
    path('comprobante-submit/<int:pk>/', views.ComprobanteSubmit.as_view(), name='comprobante-submit'),
    path('nomina/<int:pk>/', views.NominaDetailView.as_view(), name='nomina-detail'),
    path('nomina/email-comprobantes/<int:pk>/', views.email_comprobantes, name='email-comprobantes'),
]
