from django import forms
from .models import Project, UserProfile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['default_llm', 'openai_api_key', 'anthropic_api_key']
