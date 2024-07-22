from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_llm = models.CharField(max_length=50, default='gpt-4')
    openai_api_key = models.CharField(max_length=100, blank=True)
    anthropic_api_key = models.CharField(max_length=100, blank=True)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_path = models.CharField(max_length=255)
    generated_code = models.TextField(blank=True)
    github_repo = models.URLField(blank=True)
    vercel_deployment_url = models.URLField(blank=True)
    portainer_container_id = models.CharField(max_length=100, blank=True)
