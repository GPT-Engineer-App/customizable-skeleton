from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project, UserProfile
from .forms import ProjectForm, UserProfileForm
from .portainer_integration import portainer_api
from .github_integration import connect_to_github, push_to_github
from .vercel_integration import deploy_to_vercel
from gpt_engineer.applications.cli.main import main as gpt_engineer_main
from gpt_engineer.core.default.steps import improve_fn
from gpt_engineer.core.ai import AI
from gpt_engineer.core.prompt import Prompt
import os

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'main/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    return render(request, 'main/project_detail.html', {'project': project})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'main/create_project.html', {'form': form})

@login_required
def run_gpt_engineer(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    prompt = request.POST.get('prompt')
    
    # Run GPT Engineer
    ai = AI(model_name=request.user.profile.default_llm)
    result = gpt_engineer_main(prompt, project.project_path, ai=ai)
    
    # Update project with generated code
    project.generated_code = result['files']
    project.save()
    
    return JsonResponse({'success': True, 'message': 'Code generated successfully'})

@login_required
def improve_code(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    prompt = request.POST.get('prompt')
    
    # Improve existing code
    ai = AI(model_name=request.user.profile.default_llm)
    improved_code = improve_fn(ai, Prompt(prompt), project.generated_code)
    
    # Update project with improved code
    project.generated_code = improved_code
    project.save()
    
    return JsonResponse({'success': True, 'message': 'Code improved successfully'})

@login_required
def run_in_portainer(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    
    # Create and start container in Portainer
    container = portainer_api.create_container(project.name, 'Dockerfile')
    if portainer_api.start_container(container['Id']):
        project.portainer_container_id = container['Id']
        project.save()
        return JsonResponse({'success': True, 'message': 'Project running in Portainer'})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to start container'})

@login_required
def connect_github(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    
    # Connect to GitHub
    clone_url, html_url = connect_to_github(project.name)
    project.github_repo = html_url
    project.save()
    
    # Push code to GitHub
    push_to_github(project.name, project.project_path)
    
    return JsonResponse({'success': True, 'message': 'Connected to GitHub and code pushed'})

@login_required
def deploy_vercel(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)
    
    # Deploy to Vercel
    deployment = deploy_to_vercel(project.github_repo)
    project.vercel_deployment_url = deployment['url']
    project.save()
    
    return JsonResponse({'success': True, 'message': 'Deployed to Vercel', 'url': deployment['url']})

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'main/settings.html', {'form': form})
