from django.urls import path
from . import views

app_name = "placement"

urlpatterns = [
    # Home & Authentication
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # Student Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    # Mock Test
    path("test/", views.mock_test, name="mock_test"),
    path("test/submit/", views.submit_test, name="submit_test"),
    # Eligibility & Prediction
    path("eligibility/", views.eligibility_checker, name="eligibility"),
    path("prediction/", views.placement_prediction, name="prediction"),
    # Admin
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/companies/", views.manage_companies, name="manage_companies"),
    path("admin/companies/add/", views.add_company, name="add_company"),
    path(
        "admin/companies/<int:company_id>/edit/",
        views.edit_company,
        name="edit_company",
    ),
    path(
        "admin/companies/<int:company_id>/delete/",
        views.delete_company,
        name="delete_company",
    ),
    path("admin/tests/", views.manage_tests, name="manage_tests"),
    path("admin/tests/add/", views.add_question, name="add_question"),
    path(
        "admin/tests/<int:question_id>/delete/",
        views.delete_question,
        name="delete_question",
    ),
]
