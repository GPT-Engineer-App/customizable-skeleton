from django.conf import settings
import requests
from functools import wraps
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed for this context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ignore_ssl_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        original_post = requests.post

        def new_post(*args, **kwargs):
            kwargs['verify'] = False
            return original_post(*args, **kwargs)

        requests.post = new_post
        try:
            return func(*args, **kwargs)
        finally:
            requests.post = original_post

    return wrapper

class PortainerAPI:
    def __init__(self):
        self.url = settings.PORTAINER_URL
        self.username = settings.PORTAINER_USERNAME
        self.password = settings.PORTAINER_PASSWORD
        self.token = self._get_auth_token()

    @ignore_ssl_errors
    def _get_auth_token(self):
        response = requests.post(f"{self.url}/api/auth", json={
            "Username": self.username,
            "Password": self.password
        })
        return response.json()["jwt"]

    @ignore_ssl_errors
    def create_container(self, project_name, dockerfile_path):
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "Image": project_name,
            "name": project_name,
            "Cmd": ["/bin/sh", "-c", f"cd /app && docker build -t {project_name} -f {dockerfile_path} . && docker run {project_name}"]
        }
        response = requests.post(f"{self.url}/api/endpoints/1/docker/containers/create", headers=headers, json=data)
        return response.json()

    @ignore_ssl_errors
    def start_container(self, container_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.url}/api/endpoints/1/docker/containers/{container_id}/start", headers=headers)
        return response.status_code == 204

portainer_api = PortainerAPI()
