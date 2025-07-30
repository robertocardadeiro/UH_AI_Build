import os
import git  # From gitpython
import requests
from datetime import datetime
import sys
import argparse

# Add arg parser at top
parser = argparse.ArgumentParser()
parser.add_argument('--no-clone', action='store_true', help='Skip cloning if already in repo')
parser.add_argument('--output-file', default=None, help='File to write output to')
args = parser.parse_args()

# Your GitHub repo URL (update if needed)
REPO_URL = "https://github.com/robertocardadeiro/UH_AI_Build.git"
LOCAL_DIR = "uh_ai_build_clone"  # Temp clone dir
GITHUB_API_URL = "https://api.github.com/repos/robertocardadeiro/UH_AI_Build/contents"  # For file listing without clone

# Hardcoded roadmap checklist (from "UH AI - Roadmap and Plan.txt" phases)
ROADMAP_CHECKLIST = {
    "Phase 1: Setup and Data Foundation": [
        "Environment setup (e.g., requirements.txt, venv)",
        "Data collection scripts (e.g., gutenberg_downloader.py, oscar_loader.py)",
        "Processed data files (e.g., train_data.pt, uh_ai_gutenberg_texts/)",
        "Logs: phase1_log.md"
    ],
    "Phase 2: Model Architecture": [
        "Model code (e.g., model.py with MoE modifications)",
        "Config files (e.g., gpt_config.py)",
        "Test scripts (e.g., forward_pass_test.py)",
        "Logs: phase2_log.md"
    ],
    "Phase 3: Training Pipeline": [
        "Training scripts (e.g., train.py mods)",
        "Checkpoints (e.g., uh_ai_checkpoint.pt)",
        "TensorBoard logs or loss curves",
        "Logs: phase3_log.md"
    ],
    "Phase 4: Fine-Tuning and Alignment": [
        "Fine-tune scripts (e.g., sft.py, rlaif.py)",
        "CAI constitution (e.g., cai_rules.json)",
        "Aligned checkpoints",
        "Logs: phase4_log.md"
    ],
    "Phase 5: Deployment and UI": [
        "API/UI code (e.g., api.py, ui.py with Gradio/FastAPI)",
        "Deployment configs (e.g., Dockerfile)",
        "Inference scripts (e.g., generate.py)",
        "Logs: phase5_log.md"
    ],
    "Phase 6: Evaluation, Iteration, and Expansion": [
        "Eval scripts (e.g., benchmark.py for MMLU/perplexity)",
        "Research summaries (e.g., 2025_AI_Advances_Summary.md)",
        "Iteration logs (e.g., eval_results.md)",
        "Multimodal/voice extensions (e.g., clip_integration.py)"
    ],
    "General": [
        "README.md (project overview)",
        "UH_AI_Build_Roadmap.md (detailed plan/logs)",
        ".gitignore"
    ]
}

def clone_repo():
    """Clone or pull the repo locally."""
    if os.path.exists(LOCAL_DIR):
        repo = git.Repo(LOCAL_DIR)
        repo.remotes.origin.pull()
        print("Pulled latest changes.")
    else:
        git.Repo.clone_from(REPO_URL, LOCAL_DIR)
        print("Cloned repo.")
    return LOCAL_DIR

def list_repo_files_via_api():
    """List files using GitHub API (no clone needed; public repo)."""
    files = []
    try:
        response = requests.get(GITHUB_API_URL)
        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                files.append({
                    "name": item["name"],
                    "type": item["type"],
                    "size": item["size"],
                    "last_modified": "N/A"  # API doesn't give mod time; use clone for that
                })
        else:
            print(f"API error: {response.status_code}")
    except Exception as e:
        print(f"Error listing via API: {e}")
    return files

def list_repo_files_local(repo_dir):
    """List all files in cloned repo with details."""
    files = []
    for root, dirs, file_list in os.walk(repo_dir):
        for file in file_list:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
            files.append({
                "name": os.path.relpath(full_path, repo_dir),
                "size": size,
                "last_modified": mod_time
            })
    return files

def get_commit_history(repo_dir):
    """Get recent commits (last 10)."""
    repo = git.Repo(repo_dir)
    commits = []
    for commit in repo.iter_commits(max_count=10):
        commits.append({
            "hash": commit.hexsha[:7],
            "message": commit.message.strip(),
            "author": commit.author.name,
            "date": commit.authored_datetime.strftime("%Y-%m-%d %H:%M:%S")
        })
    return commits

def check_roadmap(files):
    """Check against roadmap: Flag completed/missing processes."""
    report = {}
    all_file_names = [f["name"].lower() for f in files]
    for phase, items in ROADMAP_CHECKLIST.items():
        completed = []
        missing = []
        for item in items:
            # Simple keyword match (e.g., look for 'phase1_log.md' or 'model.py')
            if any(keyword.lower() in name for name in all_file_names for keyword in item.lower().split()):
                completed.append(item)
            else:
                missing.append(item)
        report[phase] = {
            "completed": completed,
            "missing": missing,
            "status": f"{len(completed)}/{len(items)} items found"
        }
    return report

def generate_report(files, commits, roadmap_report):
    """Print a summary report."""
    print("\n=== UH AI Build Repo Report ===")
    print("\nFiles Found:")
    for f in files:
        print(f"- {f['name']} (Size: {f['size']} bytes, Modified: {f.get('last_modified', 'N/A')})")
    
    print("\nRecent Commits (Last 10):")
    if commits:
        for c in commits:
            print(f"- {c['date']} [{c['hash']}]: {c['message']} (by {c['author']})")
    else:
        print("No commits found—repo may be empty or new.")
    
    print("\nRoadmap Process Check:")
    for phase, details in roadmap_report.items():
        print(f"{phase}: {details['status']}")
        if details['completed']:
            print("  Completed: " + ", ".join(details['completed']))
        if details['missing']:
            print("  Missing/Lacking Logs: " + ", ".join(details['missing']))
    
    print("\nSuggestions:")
    if len(files) < 5:
        print("- Repo is sparse: Start by adding README.md and UH_AI_Build_Roadmap.md.")
    print("- If gaps in phases, commit logs/artifacts (e.g., for Phase 1: Add data scripts and phase1_log.md).")
    print("- Rerun script after updates for follow-up.")

# Main execution
if __name__ == "__main__":
    # Option 1: Clone locally for full details (recommended for accuracy)
    repo_dir = clone_repo()
    files = list_repo_files_local(repo_dir)
    commits = get_commit_history(repo_dir)
    
    # Option 2: Use API for quick list (uncomment if no clone wanted)
    # files = list_repo_files_via_api()
    # commits = []  # API doesn't give commits; use clone for that
    
    roadmap_report = check_roadmap(files)
    generate_report(files, commits, roadmap_report)

# At end: Instead of print, collect output as string
report = "=== UH AI Build Repo Report ===\n\n" + ...  # Build full report str
if args.output_file:
    with open(args.output_file, 'w') as f:
        f.write(report)
else:
    print(report)