# Generated by Django 4.0.5 on 2022-06-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_candidateprofile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Job Skill',
                'verbose_name_plural': 'Job Skills',
            },
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('description', models.TextField()),
                ('location', models.CharField(choices=[('Istanbul', 'Istanbul'), ('Ankara', 'Ankara'), ('Remote', 'Remote')], max_length=8)),
                ('skills', models.ManyToManyField(related_name='job_posts', to='candidate.jobskill')),
            ],
            options={
                'verbose_name': 'Job Post',
                'verbose_name_plural': 'Job Posts',
            },
        ),
    ]