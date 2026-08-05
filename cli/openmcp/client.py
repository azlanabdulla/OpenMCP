import httpx
from openmcp import config

class OpenMCPClient:
    def __init__(self):
        self.base_url = config.get_registry_url()
        self.token = config.get_token()

    def _get_headers(self) -> dict:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle_response(self, response: httpx.Response) -> dict:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise Exception(f"API Error: {error_detail}")
        
        # Some endpoints might not return JSON (e.g. file downloads)
        try:
            return response.json()
        except Exception:
            return {}

    def login(self, email: str, password: str) -> str:
        url = f"{self.base_url}/auth/login/access-token"
        data = {"username": email, "password": password}
        response = httpx.post(url, data=data)
        data = self._handle_response(response)
        return data.get("access_token")

    def search_packages(self, query: str = "") -> list:
        url = f"{self.base_url}/packages"
        response = httpx.get(url, headers=self._get_headers())
        return self._handle_response(response)

    def publish_package(self, package_name: str, manifest: str, tarball_path: str) -> dict:
        url = f"{self.base_url}/packages/{package_name}/versions"
        with open(tarball_path, "rb") as f:
            files = {"tarball": (tarball_path, f, "application/gzip")}
            data = {"manifest": manifest}
            response = httpx.post(url, data=data, files=files, headers=self._get_headers(), timeout=60.0)
        return self._handle_response(response)

    def register_package(self, name: str, description: str = "") -> dict:
        url = f"{self.base_url}/packages"
        data = {"name": name, "description": description}
        response = httpx.post(url, json=data, headers=self._get_headers())
        return self._handle_response(response)

    def get_package(self, name: str) -> dict:
        url = f"{self.base_url}/packages/{name}"
        response = httpx.get(url, headers=self._get_headers())
        return self._handle_response(response)

    def download_file(self, url: str, dest_path: str):
        with httpx.stream("GET", url) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in r.iter_bytes():
                    f.write(chunk)
