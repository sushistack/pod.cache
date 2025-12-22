import os
import re
import urllib.request
import urllib.parse
import json
from datetime import datetime
from collections import defaultdict

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVES_DIR = os.path.join(BASE_DIR, "archives")
TOPICS_DIR = os.path.join(BASE_DIR, "topics")
README_PATH = os.path.join(BASE_DIR, "README.md")
TOPICS_SIDEBAR_LIMIT = 10
RECENT_LIMIT = 5

# Private Repo Config
PRIVATE_REPO = os.environ.get("PRIVATE_REPO") # Format: owner/repo
GH_PAT = os.environ.get("GH_PAT")

def fetch_from_private_repo(filename):
    """
    Fetches file content from the private repository.
    """
    if not PRIVATE_REPO or not GH_PAT:
        print("Skipping private repo fetch: Missing configuration.")
        return None

    # Search pattern: We assume the file in private repo has the SAME name
    # OR we search for it. For now, try direct path if user provided a base path,
    # or simple search if not.
    # To keep it simple: Assume flat structure or recursively find it?
    # Let's try to find the file by filename in the private repo.
    
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/"
    headers = {
        "Authorization": f"token {GH_PAT}",
        "Accept": "application/vnd.github.v3.raw"
    }

    # Strategy: Recursive search or assume path?
    # Recursive search via Tree API is efficient.
    # GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1
    
    try:
        # Get default branch sha first, or just use 'main'/'master'
        # Let's look up the tree recursively
        tree_url = f"https://api.github.com/repos/{PRIVATE_REPO}/git/trees/main?recursive=1"
        req = urllib.request.Request(tree_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        target_path = None
        for item in data.get('tree', []):
            if item['path'].endswith(filename):
                target_path = item['path']
                break
        
        if not target_path:
            # Try 'master' if main failed or file not found?
            # For now return None
            print(f"File {filename} not found in {PRIVATE_REPO}")
            return None

        # Download content
        raw_url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{target_path}"
        req = urllib.request.Request(raw_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
            
    except Exception as e:
        print(f"Error fetching from private repo: {e}")
        return None

def fetch_by_type_and_number(doc_type, doc_number):
    """
    Fetches file content from private repo using type mapping and number.
    Path: files/udemy_{type}/markdowns/{number}. {Title}.md
    """
    if not PRIVATE_REPO or not GH_PAT:
        return None, None

    # Construct directory path
    # Mapping: type 'terraform' -> 'files/udemy_terraform/markdowns'
    # Assume prefix is 'udemy_'
    target_dir = f"files/udemy_{doc_type}/markdowns"
    
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{target_dir}"
    headers = {
        "Authorization": f"token {GH_PAT}",
        "Accept": "application/vnd.github.v3.json" # Get JSON tree first
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            files_list = json.loads(response.read().decode())
            
        # Find file starting with number
        # Prefix could be "001.", "01.", "1."
        prefixes = [f"{doc_number:03d}.", f"{doc_number:02d}.", f"{doc_number}."]
        
        found_file = None
        for item in files_list:
            name = item['name']
            for p in prefixes:
                if name.startswith(p):
                    found_file = item
                    break
            if found_file:
                break
        
        if not found_file:
            print(f"File not found for #{doc_number} in {target_dir}")
            return None, None
            
        # Download content
        raw_url = found_file['download_url']
        # If download_url is present, use it directly? 
        # API returns 'download_url'. Or we can use raw content API.
        
        # We can just fetch the raw_url directly
        req = urllib.request.Request(raw_url, headers={"Authorization": f"token {GH_PAT}"}) # Auth header just in case private
        with urllib.request.urlopen(req) as response:
            return found_file['name'], response.read().decode('utf-8')
            
    except Exception as e:
        print(f"Error fetching by type/number: {e}")
        return None, None

def parse_summary_file(filepath):
    """
    Parses a summary markdown file to extract metadata.
    Expected Header: ## YYYY-MM-DD [Topic] Title
    """
    filename = os.path.basename(filepath)
    date_str = None
    topic = None
    title = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Regex to find the header: ## 2025-12-19 [Marketing] Brand Story
        # Relaxed: ## 2025-12-19 Title (Topic might be missing)
        match = re.search(r'^##\s+(\d{4}-\d{2}-\d{2})\s+(?:\[(.*?)\]\s+)?(.*)$', content, re.MULTILINE)
        if match:
            date_str = match.group(1)
            topic = match.group(2).strip() if match.group(2) else None
            title = match.group(3).strip()
        else:
            # Fallback for filenames if header is missing/malformed: YYYY-MM-DD-Topic-Title.md
            # This is a heuristic and might need adjustment based on user's actual filenames
            pass

    return {
        "filepath": filepath,
        "filename": filename,
        "date": date_str,
        "topic": topic,
        "title": title
    }

def get_relative_path(from_path, to_path):
    return os.path.relpath(to_path, os.path.dirname(from_path))

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def handle_raw_files(root_dir):
    """
    Moves *-original.md files to raw/ subdirectory and updates referencing summaries.
    """
    for root, dirs, files in os.walk(root_dir):
        # Skip weird directories or the old '2025' style if desired, but general walk is fine.
        # But we must ensure we don't process raw folder itself.
        if os.path.basename(root) == "raw":
            continue
            
        # We only want to process "Type" directories (e.g. archives/terraform).
        # But recursively it's fine as long as we put raw in the same folder.
        
        raw_dir = os.path.join(root, "raw")
        
        # 1. Move original files
        for file in files:
            if file.endswith("-original.md"):
                if not os.path.exists(raw_dir):
                    os.makedirs(raw_dir)
                
                src = os.path.join(root, file)
                dst = os.path.join(raw_dir, file)
                
                if not os.path.exists(dst):
                    print(f"Moving raw file: {file} -> raw/")
                    os.rename(src, dst)
        
        # 2. Update links in summary files
        # Check files in this directory
        summary_files = [f for f in files if f.endswith(".md") and not f.endswith("-original.md") and f != "README.md"]
        
        if not summary_files:
            continue
            
        # Ensure raw_dir exists if we are going to use it for fetching
        # (It will be created on save)
        raw_files = os.listdir(raw_dir) if os.path.exists(raw_dir) else []
        
        for summary_file in summary_files:
            summary_path = os.path.join(root, summary_file)
            
            # Check for frontmatter
            origin_doc = None
            doc_type = None
            doc_number = None
            
            with open(summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse YAML-like frontmatter
                type_match = re.search(r"^type:\s*(.+)$", content, re.MULTILINE)
                num_match = re.search(r"^number:\s*(\d+)$", content, re.MULTILINE)
                origin_match = re.search(r"^origin-doc:\s*['\"]?(.*?)['\"]?$", content, re.MULTILINE)

                if type_match:
                    doc_type = type_match.group(1).strip()
                if num_match:
                    doc_number = int(num_match.group(1).strip())
                if origin_match:
                    origin_doc = origin_match.group(1).strip()
            
            # Determine expected raw filename and path
            if origin_doc:
                expected_raw_name = origin_doc
                target_fetch_name = origin_doc
                search_mode = "filename"
            elif doc_type and doc_number is not None:
                search_mode = "type_number"
                expected_raw_name = None 
            else:
                base_name = os.path.splitext(summary_file)[0]
                expected_raw_name = f"{base_name}-original.md"
                target_fetch_name = summary_file
                search_mode = "filename"
            
            # If we know the expected name
            should_fetch = True
            if expected_raw_name:
                 expected_raw_path = os.path.join(raw_dir, expected_raw_name)
                 should_fetch = not os.path.exists(expected_raw_path)

            fetched_filename = None
            
            # Fetching Logic
            if should_fetch:
                content_text = None
                
                if search_mode == "type_number":
                     print(f"Searching for raw file: type={doc_type}, number={doc_number}...")
                     found_name, content_text = fetch_by_type_and_number(doc_type, doc_number)
                     if found_name:
                         fetched_filename = found_name
                         expected_raw_name = found_name 
                
                elif search_mode == "filename":
                    if not os.path.exists(os.path.join(raw_dir, expected_raw_name)):
                        print(f"Attempting to fetch original '{target_fetch_name}'...")
                        content_text = fetch_from_private_repo(target_fetch_name)
                        if content_text:
                            fetched_filename = expected_raw_name 

                # Save if we got content
                if content_text and expected_raw_name:
                    if not os.path.exists(raw_dir):
                        os.makedirs(raw_dir)
                    
                    save_path = os.path.join(raw_dir, expected_raw_name)
                    if not os.path.exists(save_path):
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(content_text)
                        print(f"Fetched and saved: {expected_raw_name}")
                        if expected_raw_name not in raw_files:
                            raw_files.append(expected_raw_name)

            # Link Logic
            target_raw_file = expected_raw_name
            
            # If still null, try finding match in local raw dir by number prefix
            if not target_raw_file and doc_number is not None and os.path.exists(raw_dir):
                 for f in os.listdir(raw_dir):
                     if f.startswith(f"{doc_number:03d}.") or f.startswith(f"{doc_number}.") or f.startswith(f"{doc_number:02d}."):
                         target_raw_file = f
                         break
            
            if target_raw_file and os.path.exists(raw_dir) and target_raw_file in os.listdir(raw_dir):
                expected_raw_name = target_raw_file # consistency
                 
                with open(summary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                encoded_name = urllib.parse.quote(expected_raw_name)
                link_text = f"[📄 원본 파일 보기](raw/{encoded_name})"
                placeholder_regex = r'\(raw/.*?-original\.md\)'
                 
                if f"(raw/{encoded_name})" in content:
                    continue

                if f"(raw/{expected_raw_name})" in content:
                     content = content.replace(f"(raw/{expected_raw_name})", f"(raw/{encoded_name})")
                     with open(summary_path, 'w', encoding='utf-8') as f:
                         f.write(content)
                     continue

                if re.search(placeholder_regex, content):
                    content = re.sub(placeholder_regex, f'(raw/{encoded_name})', content)
                else:
                    # Inject after header
                    header_match = re.search(r'^(##\s+.*)$', content, re.MULTILINE)
                    if header_match:
                        header_end = header_match.end()
                        new_content = content[:header_end] + f"\n\n{link_text}\n" + content[header_end:]
                        content = new_content
                    else:
                        pass
                
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(content)

def update_type_readme(type_name, summaries, readme_path):
    """
    Generates README.md for a type directory.
    """
    # Sort summaries
    summaries.sort(key=lambda x: x['date'] or "", reverse=True)
    
    content = f"# {type_name.capitalize()}\n\n[← Dashboard](../../README.md)\n\n## 📚 학습 로그\n"
    for item in summaries:
        # Link to the file (it's in the same directory)
        link = item['filename']
        content += f"- [{item['date']} {item['title']}]({link})\n"
        
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # 0. Organize Raw Files first
    handle_raw_files(ARCHIVES_DIR)

    summaries = []
    
    # Walk through archives
    # We expect archives/{type}/*.md
    # We want to group by type to generate type READMEs
    
    type_groups = defaultdict(list)
    
    for root, dirs, files in os.walk(ARCHIVES_DIR):
        # Determine type from directory name?
        # root = archives/terraform
        rel_path = os.path.relpath(root, ARCHIVES_DIR)
        
        if rel_path == ".":
            continue
        
        # If deeply nested, take the first component as type?
        # e.g. terraform/subdir -> type=terraform
        parts = rel_path.split(os.sep)
        current_type = parts[0]
        
        # Skip numeric folders (old archives) just in case
        if current_type.isdigit():
             continue
             
        for file in files:
            if file.endswith(".md") and file != "README.md" and not file.endswith("-original.md"):
                path = os.path.join(root, file)
                data = parse_summary_file(path)
                if data['date']:
                    # Enforce type from directory if frontmatter is missing?
                    # Or trust directory more?
                    # Let's trust directory as the grouping key.
                    data['type'] = current_type # Override/Set type based on folder
                    summaries.append(data)
                    type_groups[current_type].append(data)

    print(f"Found {len(summaries)} summaries.")
    
    # Update Type READMEs
    for type_name, items in type_groups.items():
        type_dir = os.path.join(ARCHIVES_DIR, type_name)
        readme_path = os.path.join(type_dir, "README.md")
        update_type_readme(type_name, items, readme_path)
        print(f"Updated README for {type_name}")

    # No more monthly indices
    
    # Update Main README
    # Reuse update_main_readme logic but adapted
    
    summaries.sort(key=lambda x: x['date'] or "", reverse=True)
    recent = summaries[:RECENT_LIMIT]
    
    content = "# 💡 메인 대시보드\n\n"
    content += "### ⚡ 최신 요약\n"
    for item in recent:
        rel_path = get_relative_path(README_PATH, item['filepath'])
        content += f"- [{item['date']} [{item['type']}] {item['title']}]({rel_path})\n"
    
    content += "\n### 📂 토픽별 모아보기\n"
    for type_name in sorted(type_groups.keys()):
        # Link to archives/{type_name}/
        content += f"- [{type_name.capitalize()}](archives/{type_name}/)\n"
        
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated main README.")

if __name__ == "__main__":
    main()
