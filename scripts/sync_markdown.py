import os
import json
import urllib.request
import urllib.parse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_JSON = os.path.join(PROJECT_ROOT, 'data', 'projects.json')
MARKDOWN_DIR = os.path.join(PROJECT_ROOT, 'markdown')
INDEX_JSON = os.path.join(PROJECT_ROOT, 'data', 'markdown_index.json')

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
CODEBERG_USER = "Yosskavo"
GITHUB_USER = "Yosskavo"

def get_github_headers():
    headers = {'User-Agent': 'Mozilla/5.0'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f"token {GITHUB_TOKEN}"
    return headers

def discover_user_repos():
    discovered = []
    seen_urls = set()

    # 1. Discover Codeberg Repositories
    try:
        cb_url = f"https://codeberg.org/api/v1/users/{CODEBERG_USER}/repos?limit=100"
        req = urllib.request.Request(cb_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            repos = json.loads(resp.read().decode('utf-8'))
            for r in repos:
                if r.get('private'):
                    continue
                repo_name = r.get('name')
                repo_url = r.get('html_url')
                if repo_url in seen_urls:
                    continue
                seen_urls.add(repo_url)
                
                desc = r.get('description') or f"Project repository for {repo_name}."
                created_at = (r.get('created_at') or '')[:10]
                updated_at = (r.get('updated_at') or '')[:10]
                lang = r.get('language') or ''

                discovered.append({
                    "id": repo_name.lower(),
                    "title": repo_name,
                    "repo_folder": repo_name,
                    "description": desc,
                    "tech": lang if lang else "Software Project",
                    "github": repo_url,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "language": lang
                })
    except Exception as e:
        print(f"Could not fetch Codeberg repos: {e}")

    # 2. Discover GitHub Repositories
    try:
        gh_url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
        req = urllib.request.Request(gh_url, headers=get_github_headers())
        with urllib.request.urlopen(req) as resp:
            repos = json.loads(resp.read().decode('utf-8'))
            for r in repos:
                if r.get('private'):
                    continue
                repo_name = r.get('name')
                repo_url = r.get('html_url')
                if repo_url.lower() in [u.lower() for u in seen_urls]:
                    continue
                seen_urls.add(repo_url)

                desc = r.get('description') or f"Project repository for {repo_name}."
                created_at = (r.get('created_at') or '')[:10]
                updated_at = (r.get('pushed_at') or r.get('updated_at') or '')[:10]
                lang = r.get('language') or ''

                discovered.append({
                    "id": repo_name.lower(),
                    "title": repo_name,
                    "repo_folder": repo_name,
                    "description": desc,
                    "tech": lang if lang else "Software Project",
                    "github": repo_url,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "language": lang
                })
    except Exception as e:
        print(f"Could not fetch GitHub repos: {e}")

    return discovered

def sync_github(owner, repo):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    req = urllib.request.Request(api_url, headers=get_github_headers())
    md_files = {}

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        tree = data.get('tree', [])

        for item in tree:
            path = item.get('path', '')
            if item.get('type') == 'blob' and path.lower().endswith('.md'):
                quoted_path = urllib.parse.quote(path)
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{quoted_path}"
                file_req = urllib.request.Request(raw_url, headers=get_github_headers())
                with urllib.request.urlopen(file_req) as f_resp:
                    content = f_resp.read().decode('utf-8')
                    md_files[path] = content

    return md_files

def sync_codeberg(owner, repo):
    md_files = {}
    for branch in ['main', 'master', 'HEAD']:
        api_url = f"https://codeberg.org/api/v1/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                tree = data.get('tree', [])

                for item in tree:
                    path = item.get('path', '')
                    if item.get('type') == 'blob' and path.lower().endswith('.md'):
                        quoted_path = urllib.parse.quote(path)
                        raw_url = f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/{quoted_path}"
                        file_req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(file_req) as f_resp:
                            content = f_resp.read().decode('utf-8')
                            md_files[path] = content
                if md_files:
                    break
        except Exception:
            continue

    return md_files

def sync():
    print(f"Starting automatic repo discovery and Markdown sync for {CODEBERG_USER}...")
    
    projects = []
    if os.path.exists(PROJECTS_JSON):
        with open(PROJECTS_JSON, 'r', encoding='utf-8') as f:
            projects = json.load(f)

    # 1. Discover any new public repos on Codeberg or GitHub
    discovered_repos = discover_user_repos()
    existing_urls = {p.get('github', '').lower().rstrip('/') for p in projects}
    existing_folders = {p.get('repo_folder', '').lower() for p in projects}

    added_count = 0
    for disc in discovered_repos:
        disc_url = disc.get('github', '').lower().rstrip('/')
        disc_folder = disc.get('repo_folder', '').lower()
        if disc_url not in existing_urls and disc_folder not in existing_folders:
            projects.append(disc)
            existing_urls.add(disc_url)
            existing_folders.add(disc_folder)
            added_count += 1
            print(f"Discovered new repository: {disc['title']} ({disc['github']})")

    if added_count > 0:
        print(f"Added {added_count} new repository/repositories to projects.")

    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    md_index = {}

    # 2. Sync Markdown files for all projects
    for project in projects:
        repo_url = project.get('github') or project.get('codeberg') or project.get('repo_url', '')
        if not repo_url:
            continue
        
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            continue

        owner = parts[-2]
        repo = parts[-1]
        repo_folder = project.get('repo_folder', repo)
        out_dir = os.path.join(MARKDOWN_DIR, repo_folder)
        os.makedirs(out_dir, exist_ok=True)

        md_files_data = {}
        try:
            if 'codeberg.org' in repo_url:
                md_files_data = sync_codeberg(owner, repo)
            else:
                md_files_data = sync_github(owner, repo)

            if md_files_data:
                file_paths = list(md_files_data.keys())
                for path, content in md_files_data.items():
                    target_file = os.path.join(out_dir, path)
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    with open(target_file, 'w', encoding='utf-8') as out_f:
                        out_f.write(content)

                file_paths.sort(key=lambda x: (0 if x == 'README.md' else 1, x))
                md_index[repo_folder] = file_paths
                project['repo_folder'] = repo_folder
                print(f"[{repo_folder}] Synced {len(file_paths)} markdown file(s).")
            else:
                if os.path.exists(out_dir) and not os.listdir(out_dir):
                    os.rmdir(out_dir)

        except Exception as e:
            print(f"Could not sync {repo}: {e}")

    with open(PROJECTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

    with open(INDEX_JSON, 'w', encoding='utf-8') as f:
        json.dump(md_index, f, indent=2)

    print("Sync complete! Updated data/markdown_index.json and data/projects.json.")

if __name__ == '__main__':
    sync()
