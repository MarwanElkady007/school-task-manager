from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user_type = request.POST.get("user_type")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        if user_type == "teacher":
            user.profile.is_teacher = True
            user.profile.save()
        if user_type == "admin":
            user.is_staff = True
            user.save()
            user.profile.is_teacher = False

        messages.success(request, "Signup successful! Please login.")
        return redirect("login")

    return render(request, "signup.html")


def home_view(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("loginUsername")
        password = request.POST.get("loginPassword")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Add success message once
            messages.success(request, "Logged in successfully!")

            if user.is_staff:
                return redirect("admin_dashboard")
            elif user.profile.is_teacher:
                return redirect("teacher_dashboard")
            else:
                messages.error(request, "You are not authorized.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


@login_required
def admin_dashboard_view(request):
    tasks = Task.objects.all()
    return render(request, "admin-dashboard.html", {"tasks": tasks})


@login_required
def admin_add_task_view(request):
    if request.method == "POST":
        title = request.POST.get("taskTitle")
        teacher_id = request.POST.get("teacherName")
        priority = request.POST.get("priority")
        description = request.POST.get("description")

        assigned_to = User.objects.get(id=teacher_id)

        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            assigned_to=assigned_to,
            created_by=request.user,
        )

        messages.success(request, "Task added successfully!")
        return redirect("admin_dashboard")

    teachers = User.objects.filter(profile__is_teacher=True)
    return render(request, "admin-add-task.html", {"teachers": teachers})


@login_required
def admin_edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("taskTitle")
        task.priority = request.POST.get("priority")
        task.description = request.POST.get("description")
        teacher_id = request.POST.get("teacherName")
        task.assigned_to = User.objects.get(id=teacher_id)
        task.save()

        # Check if it's an AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"success": True, "message": "Task updated successfully."}
            )

        # Normal form submission
        messages.success(request, "Task updated successfully.")
        return redirect("admin_dashboard")

    # Important part for displaying teachers in the form
    teachers = User.objects.filter(profile__is_teacher=True)
    return render(request, "admin-edit-task.html", {"task": task, "teachers": teachers})


@login_required
def teacher_dashboard_view(request):
    priority = request.GET.get("priority")

    if priority in ["low", "medium", "high"]:
        tasks = Task.objects.filter(
            assigned_to=request.user, is_completed=False, priority=priority
        )
    else:
        tasks = Task.objects.filter(assigned_to=request.user, is_completed=False)

    return render(
        request,
        "teacher-dashboard.html",
        {"tasks": tasks, "selected_priority": priority},
    )


def logout_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


@login_required
def teacher_completed_view(request):
    tasks = Task.objects.filter(assigned_to=request.user, is_completed=True)
    return render(request, "teacher-completed.html", {"tasks": tasks})


@login_required
def mark_task_completed_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == "POST":
        task.is_completed = True
        task.completed_on = timezone.now()
        task.save()

        # Check if request is AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"success": True, "message": "Task marked as completed successfully!"}
            )

        # Regular request flow
        messages.success(request, "Task marked as completed successfully!")
        return redirect("teacher_dashboard")

    return redirect("teacher_dashboard")


@login_required
def admin_delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    task.delete()

    # Check if request is AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Task deleted successfully!"})

    # Regular request flow
    messages.success(request, "Task deleted successfully!")
    return redirect("admin_dashboard")


@login_required
def teacher_task_details_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    return render(request, "teacher-task-details.html", {"task": task})


@login_required
def filter_tasks_view(request):
    priority = request.GET.get("priority")
    tasks = Task.objects.filter(assigned_to=request.user, is_completed=False)

    if priority and priority in ["low", "medium", "high"]:
        tasks = tasks.filter(priority=priority)

    return render(request, "partials/task_rows.html", {"tasks": tasks})
