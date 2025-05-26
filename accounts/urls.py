from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"),
    path("teacher-dashboard/", views.teacher_dashboard_view, name="teacher_dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("teacher-completed/", views.teacher_completed_view, name="teacher_completed"),
    path("admin-add-task/", views.admin_add_task_view, name="admin_add_task"),
    path(
        "admin-edit-task/<int:task_id>/",
        views.admin_edit_task_view,
        name="admin_edit_task",
    ),
    path(
        "mark-task-completed/<int:task_id>/",
        views.mark_task_completed_view,
        name="mark_task_completed",
    ),
    path(
        "admin-delete-task/<int:task_id>/",
        views.admin_delete_task_view,
        name="admin_delete_task",
    ),
    path(
        "teacher-task-details/<int:task_id>/",
        views.teacher_task_details_view,
        name="teacher_task_details",
    ),
    path("filter-tasks/", views.filter_tasks_view, name="filter_tasks"),
]
