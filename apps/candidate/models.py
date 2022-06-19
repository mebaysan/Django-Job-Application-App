from django.db import models
from django.contrib.auth.models import User
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.contrib import admin


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name="candidate_profile")
    bio = models.TextField()
    skills = models.ManyToManyField("candidate.JobSkill", "candidates")

    class Meta:
        verbose_name = "Candidate Profile"
        verbose_name_plural = "Candidate Profiles"

    def __str__(self):
        return self.user.username


class JobSkill(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=False)

    class Meta:
        verbose_name = "Job Skill"
        verbose_name_plural = "Job Skills"

    def __str__(self):
        return self.name

    def get_unique_slug(self):
        counter = 0
        slug = slugify(unidecode(self.name))
        new_slug = slug
        while JobSkill.objects.filter(slug=new_slug).exists():
            counter += 1
            new_slug = "{}-{}".format(slug, counter)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = self.get_unique_slug()
        else:
            job_skill = JobSkill.objects.get(slug=self.slug)
            if job_skill.name != self.name:
                self.slug = self.get_unique_slug()
        super(JobSkill, self).save(*args, **kwargs)

    @property
    @admin.display(description="Related Job Posts")
    def get_related_job_count(self):
        return self.job_posts.all().count()

    @property
    @admin.display(description="Related Candidates")
    def get_related_candidate_count(self):
        return self.candidates.all().count()


class JobPost(models.Model):
    LOCATION_CHOICES = [
        ("Istanbul/Office", "Istanbul/Office"),
        ("Ankara/Office", "Ankara/Office"),
        ("Remote", "Remote"),
    ]
    TYPE_CHOICES = [
        ("FT", "Full-Time"),
        ("PT", "Part-Time"),
        ("IS", "Internship"),
    ]
    name = models.CharField(max_length=512)
    description = models.TextField()
    skills = models.ManyToManyField(JobSkill, "job_posts")
    location = models.CharField(choices=LOCATION_CHOICES, max_length=15)
    job_type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    slug = models.SlugField(null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    candidates = models.ManyToManyField(CandidateProfile, "job_posts")

    class Meta:
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"

    def __str__(self):
        return self.name

    def get_unique_slug(self):
        counter = 0
        slug = slugify(unidecode(self.name))
        new_slug = slug
        while JobPost.objects.filter(slug=new_slug).exists():
            counter += 1
            new_slug = "{}-{}".format(slug, counter)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = self.get_unique_slug()
        else:
            job_post = JobPost.objects.get(slug=self.slug)
            if job_post.name != self.name:
                self.slug = self.get_unique_slug()
        super(JobPost, self).save(*args, **kwargs)

    @property
    @admin.display(description="Candidate Count")
    def get_candidate_count(self):
        return self.candidates.all().count()
