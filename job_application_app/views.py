from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
from django.contrib.auth.models import User
from apps.candidate.models import JobPost, JobSkill

# password
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


@login_required
def index(request):
    job_posts = JobPost.objects.filter(is_active=True).all().order_by("-updated_date")
    job_skills = JobSkill.objects.all()
    searchedTitle = request.GET.get("inputJobTitle")
    searchedSkills = request.GET.getlist("inputSkills")
    if searchedTitle:
        job_posts = job_posts.filter(name__contains=searchedTitle).all()
    if searchedSkills:
        job_posts = job_posts.filter(skills__name__in=searchedSkills).all().distinct()
    return render(
        request, "index.html", {"job_posts": job_posts, "job_skills": job_skills}
    )


def register(request):
    if request.method == "POST":
        username = request.POST.get("inputUsername")  # it will be also email
        password = request.POST.get("inputPassword")
        first_name = request.POST.get("inputFirstName")
        last_name = request.POST.get("inputLastName")
        role = request.POST.get("inputRole")
        new_user = User(
            username=username,
            email=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=True if role == "Staff" else False,
            is_active=False
            if role == "Staff"
            else True,  # if user is staff, the super user has to activate his acc
        )
        new_user.set_password(password)
        new_user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Staff {username} is created successfully. They will be able to access to the admin panel when the superuser activate their account."
            if role == "Staff"
            else f"Candidate {username} created successfully. Now, they can log in into the system.",
        )
        return redirect("login")
    return render(request, "core/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("inputUsername")
        password = request.POST.get("inputPassword")
        user = authenticate(username=username, password=password)
        if user is not None:
            dj_login(request, user)
            if user.is_staff:
                return redirect("admin:index")
            return redirect("index")
        else:
            messages.add_message(
                request,
                messages.WARNING,
                "User couldn't login with the creds. Please, try again.",
            )
            return redirect("login")
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "core/login.html")


@login_required
def logout(request):
    dj_logout(request)
    messages.add_message(
        request,
        messages.SUCCESS,
        "User successfully logged out.",
    )
    return redirect("login")


def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "admin@mr-kar.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:

                        return HttpResponse("Invalid header found.")

                    messages.success(
                        request,
                        "A message with reset password instructions has been sent to your inbox.",
                    )
                    return redirect("index")
            messages.add_message(
                request, messages.WARNING, "An invalid email has been entered."
            )
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )
