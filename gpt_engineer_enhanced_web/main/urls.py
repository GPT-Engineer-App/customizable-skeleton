from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    # path('settings/', views.settings_view, name='settings'),
    path('api/run-gpt-engineer/', views.run_gpt_engineer, name='run_gpt_engineer'),
    path('api/connect-to-github/', views.connect_to_github, name='connect_to_github'),
    # path('api/update-api-keys/', views.update_api_keys, name='update_api_keys'),
    # path('api/get-user-projects/', views.get_user_projects, name='get_user_projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/run/', views.run_gpt_engineer, name='run_gpt_engineer'),
    path('project/<int:project_id>/improve/', views.improve_code, name='improve_code'),
    path('project/<int:project_id>/run-portainer/', views.run_in_portainer, name='run_in_portainer'),
    path('project/<int:project_id>/connect-github/', views.connect_github, name='connect_github'),
    path('project/<int:project_id>/deploy-vercel/', views.deploy_vercel, name='deploy_vercel'),
    path('settings/', views.settings, name='settings'),
]
