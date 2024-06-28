from django.db import models
import uuid
from config import settings

class ActiveUserManager(models.Manager):
    def get_queryset(self):
        # This will return only the users where suspended_at, and suspended_by are NULL
        return (
            super()
            .get_queryset()
            .filter(
                suspended_at__isnull=True,
                suspended_by__isnull=True,
            )
        )

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    discord_id = models.CharField(unique=True, max_length=36, blank=True, null=True)
    muid = models.CharField(unique=True, max_length=100)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=200)
    password = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(unique=True, max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=[("Male", "Male"), ("Female", "Female")])
    dob = models.DateField(blank=True, null=True)
    admin = models.BooleanField(default=False)
    exist_in_guild = models.BooleanField(default=False)
    district = models.ForeignKey("District", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    suspended_at = models.DateTimeField(blank=True, null=True)
    suspended_by = models.ForeignKey("self", on_delete=models.SET(settings.SYSTEM_ADMIN_ID), blank=True, null=True,
                                     related_name="user_suspended_by_user", db_column="suspended_by", default=None)
    objects = ActiveUserManager()
    every = models.Manager()

    class Meta:
        managed = False
        db_table = 'user'
        
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to='projects/logos/', null=True, blank=True)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)
    link = models.URLField()
    contributors = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='created_projects', db_column='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='updated_projects', db_column='updated_by')

    class Meta:
        managed = False
        db_table = "projects"
        ordering = ["created_at"]
    
class ProjectImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_images"
        
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='created_comments', db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='updated_comments', db_column='updated_by')

    class Meta:
        managed = False
        db_table = "projects_comments"
        ordering = ["created_at"]
        
class Vote(models.Model):
    VOTE_CHOICES = [('upvote', 'Upvote'), ('downvote', 'Downvote')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='created_votes', db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET(settings.SYSTEM_ADMIN_ID), related_name='updated_votes', db_column='updated_by')

    class Meta:
        managed = False
        db_table = "projects_votes"
        ordering = ["created_at"]