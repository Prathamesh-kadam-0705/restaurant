from django.urls import path
from organizations.views import OrganizationDetailView, OrganizationListCreateView

urlpatterns = [
    path("",OrganizationListCreateView.as_view()),
    path("<int:id>/", OrganizationDetailView.as_view()),
]