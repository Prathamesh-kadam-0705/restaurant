from django.urls import path

from organizations.views import (
    BranchDetailView,
    BranchListCreateView,
    CategoryDetailView,
    CategoryListCreateView,
    FoodDetailView,
    FoodListCreateView,
    MemberDetailView,
    MemberListCreateView,
    OrganizationDetailView,
    OrganizationListCreateView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view()),

    path("<int:id>/", OrganizationDetailView.as_view()),

    path(
        "<int:id>/branches/",
        BranchListCreateView.as_view()
    ),

    path(
        "<int:id>/branches/<int:branch_id>/",
        BranchDetailView.as_view()
    ),

    path(
        "<int:id>/members/",
        MemberListCreateView.as_view()
    ),

    path(
        "<int:id>/members/<int:member_id>/",
        MemberDetailView.as_view()
    ),
    path(
        "<int:id>/branches/<int:branch_id>/foods/",
        FoodListCreateView.as_view()
    ),
    path(
        "<int:id>/branches/<int:branch_id>/foods/<int:food_id>/",
        FoodDetailView.as_view()
    ),
    path(
        "<int:id>/branches/<int:branch_id>/categories/",
        CategoryListCreateView.as_view()
    ),
    path(
        "<int:id>/branches/<int:branch_id>/categories/<int:category_id>/",
        CategoryDetailView.as_view()
    ),
]