import requests
from django.conf import settings

def deploy_to_vercel(github_repo_url):
    headers = {
        "Authorization": f"Bearer {settings.VERCEL_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": github_repo_url.split("/")[-1],
        "gitRepository": {
            "type": "github",
            "repo": github_repo_url
        }
    }
    response = requests.post("https://api.vercel.com/v9/projects", headers=headers, json=data)
    return response.json()
