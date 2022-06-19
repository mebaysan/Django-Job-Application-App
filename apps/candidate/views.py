from django.shortcuts import render, redirect, get_object_or_404
from .models import JobPost, JobSkill
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
def profile(request):
    if request.method == "POST":
        # get data
        username = request.POST.get("inputEmail")
        first_name = request.POST.get("inputFirstName")
        last_name = request.POST.get("inputLastName")
        bio = request.POST.get("inputBio")
        skills = request.POST.getlist("inputSkills")

        # update user with new data
        user = request.user
        user.username = username
        user.email = username
        user.first_name = first_name
        user.last_name = last_name
        user.candidate_profile.bio = bio
        user.candidate_profile.skills.set(skills)
        # error check for unique username & email

        try:
            user.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{request.user.username} successfully updated.",
            )
        except Exception as e:
            messages.add_message(
                request,
                messages.WARNING,
                f"{request.user.username} couldn't update. Error: {e}",
            )
        return redirect("candidate:profile")

    job_skills = JobSkill.objects.all()
    return render(request, "candidate/profile.html", {"job_skills": job_skills})


@login_required
def update_password(request):
    if request.method == "POST":
        # get data
        old_password = request.POST.get("inputOldPassword")
        new_password = request.POST.get("inputNewPassword")
        re_new_password = request.POST.get("inputReNewPassword")
        if not request.user.check_password(old_password):
            messages.add_message(
                request, messages.WARNING, "You have to use the exact old password"
            )
            return redirect("candidate:update_password")
        if not new_password == re_new_password:
            messages.add_message(
                request, messages.WARNING, "New passwords doesn't match."
            )
            return redirect("candidate:update_password")
        request.user.set_password(new_password)
        request.user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Password has been updated successfully. You can use it for next logins.",
        )
        return redirect("logout")
    return render(request, "candidate/update_password.html")


@login_required
@require_http_methods(["POST"])
def apply_for_position(request):
    applied_job_slug = request.POST.get("appliedJobSlug")
    applied_job = get_object_or_404(JobPost, slug=applied_job_slug)
    request.user.candidate_profile.job_posts.add(applied_job)
    messages.add_message(
        request, messages.SUCCESS, "You have successfully applied to the position."
    )
    return redirect("index")


@login_required
@require_http_methods(["POST"])
def undo_for_position(request):
    applied_job_slug = request.POST.get("appliedJobSlug")
    applied_job = get_object_or_404(JobPost, slug=applied_job_slug)
    request.user.candidate_profile.job_posts.remove(applied_job)
    messages.add_message(
        request, messages.SUCCESS, "You have successfully undid application for the position."
    )
    return redirect("candidate:applied_jobs")


@login_required
def candidate_jobs(request):
    user_jobs = request.user.candidate_profile.job_posts.all()
    return render(request, "candidate/applied_jobs.html", {"job_posts": user_jobs})
