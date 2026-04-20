import os
import shutil
import zipfile
import requests
from typing import Tuple

from config import GITHUB_TOKEN, SNAPSHOTS_DIR

def get_github_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_github_metadata(owner: str, repo: str) -> Tuple[str, str, str]:
    headers = get_github_headers()
    
    # 1. Fetch metadata (name, default_branch)
    repo_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    if not repo_resp.ok:
        raise ValueError(f"Failed to fetch repository metadata from GitHub. Status {repo_resp.status_code}: {repo_resp.text}")
    
    repo_data = repo_resp.json()
    name = repo_data["name"]
    default_branch = repo_data["default_branch"]

    # 2. Fetch latest commit SHA
    commit_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}", headers=headers)
    if not commit_resp.ok:
        raise ValueError(f"Failed to fetch latest commit from GitHub list. Status {commit_resp.status_code}")
    
    commit_sha = commit_resp.json()["sha"]
    return name, default_branch, commit_sha

def download_and_extract_zip(owner: str, repo: str, commit_sha: str, target_dir: str):
    headers = get_github_headers()
    zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{commit_sha}"
    
    print(f"Downloading {zip_url}...")
    resp = requests.get(zip_url, headers=headers, stream=True)
    resp.raise_for_status()
    
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    zip_path = target_dir + ".zip"
    with open(zip_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            
    # Extract
    print(f"Extracting to {target_dir}...")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)  # Clear contents before extraction
    
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # GitHub zips have a root wrapper folder
        members = zip_ref.namelist()
        if not members:
            raise ValueError("Empty zip downloaded")
        root_folder = members[0].split('/')[0] + '/'
        
        for member in members:
            if member.startswith(root_folder):
                # Strip the root folder when extracting
                target_path = os.path.join(target_dir, member[len(root_folder):])
                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                        
    os.remove(zip_path)
