import os
import re
import urllib.request
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
        match = re.search(r'^##\s+(\d{4}-\d{2}-\d{2})\s+\[(.*?)\]\s+(.*)$', content, re.MULTILINE)
        if match:
            date_str = match.group(1)
            topic = match.group(2).strip()
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

def update_topic_indices(summaries):
    """
    Updates or creates topic index files in topics/
    """
    topics = defaultdict(list)
    for s in summaries:
        if s['topic']:
            topics[s['topic']].append(s)

    if not os.path.exists(TOPICS_DIR):
        os.makedirs(TOPICS_DIR)

    for topic, items in topics.items():
        # Sort by date descending
        items.sort(key=lambda x: x['date'] or "", reverse=True)
        
        topic_filename = f"{topic.lower().replace(' ', '-')}.md"
        topic_path = os.path.join(TOPICS_DIR, topic_filename)
        
        content = f"# {topic}\n\n[← Dashboard](../README.md)\n\n## 📚 학습 로그\n"
        for item in items:
            rel_path = get_relative_path(topic_path, item['filepath'])
            content += f"- [{item['date']} {item['title']}]({rel_path})\n"
            
        with open(topic_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    return sorted(topics.keys())

def update_monthly_indices(summaries):
    """
    Updates README.md in each archives/YYYY/MM/ directory
    """
    months = defaultdict(list)
    for s in summaries:
        if s['date']:
            # archives/2025/12
            d = datetime.strptime(s['date'], '%Y-%m-%d')
            key = (d.year, d.month)
            months[key].append(s)

    for (year, month), items in months.items():
        # Sort by date descending
        items.sort(key=lambda x: x['date'] or "", reverse=True)
        
        month_str = f"{month:02d}"
        month_dir = os.path.join(ARCHIVES_DIR, str(year), month_str)
        if not os.path.exists(month_dir):
            continue # Should exist since files are there
            
        readme_path = os.path.join(month_dir, "README.md")
        
        content = f"# {year}년 {month}월\n\n[← Dashboard](../../README.md)\n\n## 🗂️ 목록\n"
        for item in items:
            rel_path = item['filename'] # Same directory
            content += f"- [{item['date']} [{item['topic']}] {item['title']}]({rel_path})\n"
            
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

def update_main_readme(summaries, topic_list):
    """
    Updates the main README.md
    """
    # Sort all summaries by date descending
    summaries.sort(key=lambda x: x['date'] or "", reverse=True)
    recent = summaries[:RECENT_LIMIT]
    
    # Generate content
    content = "# 💡 메인 대시보드\n\n"
    
    # Recent
    content += "### ⚡ 최신 요약\n"
    for item in recent:
        rel_path = get_relative_path(README_PATH, item['filepath'])
        content += f"- [{item['date']} [{item['topic']}] {item['title']}]({rel_path})\n"
    
    # Topics
    content += "\n### 📂 토픽별 모아보기\n"
    for topic in topic_list:
        topic_filename = f"{topic.lower().replace(' ', '-')}.md"
        content += f"- [{topic}](topics/{topic_filename})\n"
        
    # Archives (Group by Year/Month logic could be added here, currently hardcoded in template or dynamic scan)
    # For now, let's keep the user's manual structure for Archives or generate it.
    # To keep it simple and safe, I will append the dynamic parts to a template or just rewrite sections if markers exist.
    # Since I am rewriting the whole file based on the user's previous request structure:
    
    content += "\n### 📅 월별 아카이브\n"
    # Find all year/month directories
    years = sorted([d for d in os.listdir(ARCHIVES_DIR) if d.isdigit() and os.path.isdir(os.path.join(ARCHIVES_DIR, d))], reverse=True)
    for year in years:
        year_path = os.path.join(ARCHIVES_DIR, year)
        months = sorted([d for d in os.listdir(year_path) if d.isdigit() and os.path.isdir(os.path.join(year_path, d))], reverse=True)
        for month in months:
            content += f"- [{year}년 {month}월](archives/{year}/{month}/)\n"

    content += f"\n### 🗄️ 연도별\n"
    for year in years:
        content += f"- [{year}년 전체](archives/{year}/)\n"

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def handle_raw_files(root_dir):
    """
    Moves *-original.md files to raw/ subdirectory and updates referencing summaries.
    """
    for root, dirs, files in os.walk(root_dir):
        # Skip if we are already in a raw directory
        if os.path.basename(root) == "raw" or "raw" in dirs:
             # If "raw" is in dirs, we are in the parent (e.g. 12/). We want to process this dir.
             # If basename is "raw", we are inside raw/. Skip.
             pass
        
        if os.path.basename(root) == "raw":
            continue

        raw_dir = os.path.join(root, "raw")
        
        # 1. Move original files
        for file in files:
            if file.endswith("-original.md"):
                if not os.path.exists(raw_dir):
                    os.makedirs(raw_dir)
                
                src = os.path.join(root, file)
                dst = os.path.join(raw_dir, file)
                
                # Avoid moving if already there (shouldn't happen due to walk check, but safety)
                if not os.path.exists(dst):
                    print(f"Moving raw file: {file} -> raw/")
                    os.rename(src, dst)
        
        # 2. Update links in summary files
        # We look for all summaries in this folder and check if they need a link update
        # Heuristic: match regex [📄 원본 파일 보기](...)
        if not os.path.exists(raw_dir):
            continue
            
        raw_files = os.listdir(raw_dir)
        summary_files = [f for f in files if f.endswith(".md") and not f.endswith("-original.md") and f != "README.md"]
        
        for summary_file in summary_files:
            summary_path = os.path.join(root, summary_file)
            
            # Expected raw filename: summary_filename without extension + -original.md?
            # Or just check if any raw file matches the common prefix?
            # Let's try to find a raw file that matches the summary filename pattern.
            # Check for frontmatter
            origin_doc = None
            doc_type = None
            doc_number = None
            
            with open(summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse YAML-like frontmatter manually or use a simple regex approach for flexibility
                # Match type: ... and number: ...
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
                # Type/Number mode
                # We don't know the full filename yet, we have to find it.
                # But we need a local filename to save it as.
                # If we fetch successfully, we will get the real filename.
                # For now, let's defer the local naming until we fetch?
                # Or we can prefer the fetched filename.
                search_mode = "type_number"
                expected_raw_name = None # Will determine after fetch (heuristic: if local exists, we need to know name)
            else:
                # Fallback
                base_name = os.path.splitext(summary_file)[0]
                expected_raw_name = f"{base_name}-original.md"
                target_fetch_name = summary_file
                search_mode = "filename"
            
            # If we know the expected name (Filename or Origin-doc mode), check existence
            if expected_raw_name:
                 expected_raw_path = os.path.join(raw_dir, expected_raw_name)
                 should_fetch = not os.path.exists(expected_raw_path)
            else:
                 # Type/Number mode: we check if we already have a raw file that "looks like" the number?
                 # Too complex. Let's simplfy: Always try to fetch/check if specific raw file is missing?
                 # Actually, if we don't know the filename, we can't check existence easily without scanning dir.
                 # Let's try to fetch if we are in Type/Number mode and haven't linked a raw file yet?
                 should_fetch = True 

            fetched_filename = None
            
            # Fetching Logic
            if should_fetch:
                content_text = None
                
                if search_mode == "type_number":
                     print(f"Searching for raw file: type={doc_type}, number={doc_number}...")
                     found_name, content_text = fetch_by_type_and_number(doc_type, doc_number)
                     if found_name:
                         fetched_filename = found_name
                         expected_raw_name = found_name # Now we know
                
                elif search_mode == "filename":
                    # Only fetch if not exists
                    if not os.path.exists(expected_raw_path):
                        print(f"Attempting to fetch original '{target_fetch_name}'...")
                        content_text = fetch_from_private_repo(target_fetch_name)
                        if content_text:
                            fetched_filename = expected_raw_name # We use the expected name

                # Save if we got content
                if content_text and expected_raw_name:
                    if not os.path.exists(raw_dir):
                        os.makedirs(raw_dir)
                    
                    save_path = os.path.join(raw_dir, expected_raw_name)
                    # Don't overwrite if exists (safety)
                    if not os.path.exists(save_path):
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(content_text)
                        print(f"Fetched and saved: {expected_raw_name}")
                        if expected_raw_name not in raw_files:
                            raw_files.append(expected_raw_name)
                    else:
                        # existed locally but maybe we didn't know the name mapping?
                        pass

            # Update link if we have a target raw file
            # In Type/Number mode, expected_raw_name is now set if fetch succeeded OR if we found a matching file locally?
            
            # If we failed to fetch (or offline), can we still link?
            # If we have Type/Number, we might want to scan local raw/ folder for matching number?
            # Heuristic: if raw/001. ... .md exists? 
            # Let's stick to: "If file exists in raw/, link it."
            
            # If we fetched, expected_raw_name is set.
            # If we didn't fetch (already exists), we rely on... existing logic? 
            # Existing logic was simple: expected_raw_name = base-original.md.
            # Now we have variable filenames.
            
            # Revised Linking Logic:
            # 1. If we have expected_raw_name (from fetch or origin-doc), use it.
            # 2. If not, scan raw_dir for a "best match"?
            #    Match: starts with number? (if type/number provided)
            
            target_raw_file = expected_raw_name
            
            if not target_raw_file and doc_number is not None and os.path.exists(raw_dir):
                 # Try to find local file starting with number
                 for f in os.listdir(raw_dir):
                     # Check for 001, 1, 01 prefixes
                     if f.startswith(f"{doc_number:03d}.") or f.startswith(f"{doc_number}.") or f.startswith(f"{doc_number:02d}."):
                         target_raw_file = f
                         break
            
            if target_raw_file and target_raw_file in os.listdir(raw_dir):
                # Do the linking
                expected_raw_name = target_raw_file # consistency
                 
                with open(summary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                link_text = f"[📄 원본 파일 보기](raw/{expected_raw_name})"
                placeholder_regex = r'\(raw/.*?-original\.md\)'
                 
                if f"(raw/{expected_raw_name})" in content:
                    continue

                # 1. Replace existing placeholder
                if re.search(placeholder_regex, content):
                    content = re.sub(placeholder_regex, f'(raw/{expected_raw_name})', content)
                else:
                    # 2. Inject if missing
                    # Insert after the first H2 header (## ...)
                    # Find the header line
                    header_match = re.search(r'^(##\s+.*)$', content, re.MULTILINE)
                    if header_match:
                        # Insert link after the header
                        header_end = header_match.end()
                        new_content = content[:header_end] + f"\n> {link_text}\n" + content[header_end:]
                        content = new_content
                    else:
                        pass
                
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(content)

def main():
    # 0. Organize Raw Files first
    handle_raw_files(ARCHIVES_DIR)

    summaries = []
    
    # Walk through archives
    for root, dirs, files in os.walk(ARCHIVES_DIR):
        for file in files:
            if file.endswith(".md") and file != "README.md" and not file.endswith("-original.md"):
                path = os.path.join(root, file)
                data = parse_summary_file(path)
                if data['date']: # Only add successfully parsed files
                    summaries.append(data)
    
    print(f"Found {len(summaries)} summaries.")
    
    topic_list = update_topic_indices(summaries)
    print(f"Updated {len(topic_list)} topics.")
    
    update_monthly_indices(summaries)
    print("Updated monthly indices.")
    
    update_main_readme(summaries, topic_list)
    print("Updated main README.")

if __name__ == "__main__":
    main()
