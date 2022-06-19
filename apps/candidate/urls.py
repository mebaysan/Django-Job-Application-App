from django.urls import path
from . import views

app_name = "candidate"
urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("update-password/", views.update_password, name="update_password"),
    path("apply/", views.apply_for_position, name="apply_for_position"),
    path("applied-jobs/", views.candidate_jobs, name="applied_jobs"),
    path("undo/", views.undo_for_position, name="undo_for_position"),
]
