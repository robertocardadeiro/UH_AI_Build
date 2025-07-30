import os
import subprocess
import argparse
import datetime
import random  # For any sampling if needed
import datetime
import git  # pip install gitpython

REPO_PATH = '.'  # Current dir (your repo)
LOG_FILE = 'phase1_log.md'
ROADMAP_FILE = 'UH_AI_Build_Roadmap.md'

def update_log(entry):
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n## {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{entry}\n")
    print(f"Updated {LOG_FILE}")

def update_roadmap(status):
    with open(ROADMAP_FILE, 'a') as f:
        f.write(f"\n- Status Update: {status}\n")
    print(f"Updated {ROADMAP_FILE}")

def commit_changes(message="Auto-update logs and roadmap"):
    repo = git.Repo(REPO_PATH)
    repo.index.add([LOG_FILE, ROADMAP_FILE, 'README.md'])
    repo.index.commit(message)
    origin = repo.remote(name='origin')
    origin.push()
    print("Committed and pushed changes")

if __name__ == '__main__':
    # Example usage: python uh_ai_project_tracker.py
    update_log("Test entry: Baseline nanoGPT run complete. VRAM usage: 8GB.")
    update_roadmap("Phase 1: Data collection started with Gutenberg.")
    commit_changes("Tracker auto-update: Phase 1 progress")

def run_git_command(command):
    """Helper to run Git commands and capture output."""
    try:
        return subprocess.check_output(command, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running Git command: {e}")
        return ""

def pull_latest():
    """Pull latest changes from origin/main."""
    run_git_command("git pull origin main")

def list_files_recursive(directory="."):
    """List all files recursively with size and modified time."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            size = os.path.getsize(filepath)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
            files.append((filepath, size, mtime))
    return sorted(files)

def get_recent_commits(limit=10):
    """Get last N commits with date, hash, message, and author."""
    commits = run_git_command(f"git log --pretty=format:'%cd [%h]: %s (by %an)' -n {limit}")
    return commits.splitlines()

def check_roadmap_phases(files):
    """Check for files/logs indicating roadmap phase completion."""
    phases = {
        "Phase 1: Setup and Data Foundation": {
            "items": [
                "Logs: phase1_log.md",
                "Environment setup (e.g., requirements.txt, venv)",
                "Data collection scripts (e.g., gutenberg_downloader.py, oscar_loader.py)",
                "Processed data files (e.g., train_data.pt, uh_ai_gutenberg_texts/)"
            ],
            "found": 0
        },
        "Phase 2: Model Architecture": {
            "items": [
                "Config files (e.g., gpt_config.py)",
                "Model code (e.g., model.py with MoE modifications)",
                "Test scripts (e.g., forward_pass_test.py)",
                "Logs: phase2_log.md"
            ],
            "found": 0
        },
        "Phase 3: Training Pipeline": {
            "items": [
                "Training scripts (e.g., train.py mods)",
                "Checkpoints (e.g., uh_ai_checkpoint.pt)",
                "TensorBoard logs or loss curves",
                "Logs: phase3_log.md"
            ],
            "found": 0
        },
        "Phase 4: Fine-Tuning and Alignment": {
            "items": [
                "Fine-tune scripts (e.g., sft.py, rlaif.py)",
                "CAI constitution (e.g., cai_rules.json)",
                "Aligned checkpoints",
                "Logs: phase4_log.md"
            ],
            "found": 0
        },
        "Phase 5: Deployment and UI": {
            "items": [
                "API/UI code (e.g., api.py, ui.py with Gradio/FastAPI)",
                "Deployment configs (e.g., Dockerfile)",
                "Inference scripts (e.g., generate.py)",
                "Logs: phase5_log.md"
            ],
            "found": 0
        },
        "Phase 6: Evaluation, Iteration, and Expansion": {
            "items": [
                "Eval scripts (e.g., benchmark.py for MMLU/perplexity)",
                "Research summaries (e.g., 2025_AI_Advances_Summary.md)",
                "Multimodal/voice extensions (e.g., clip_integration.py)",
                "Iteration logs (e.g., eval_results.md)"
            ],
            "found": 0
        },
        "General": {
            "items": [
                "README.md (project overview)",
                "UH_AI_Build_Roadmap.md (detailed plan/logs)",
                ".gitignore"
            ],
            "found": 0
        }
    }

    existing_files = [f[0] for f in files]  # List of file paths
    for phase, data in phases.items():
        for item in data["items"]:
            # Simple fuzzy match: Check if any file contains the key phrase (e.g., 'phase1_log.md')
            if any(item.lower() in filepath.lower() for filepath in existing_files):
                data["found"] += 1

    return phases

def generate_suggestions(phases):
    """Generate suggestions based on missing items."""
    suggestions = []
    for phase, data in phases.items():
        completion = data["found"] / len(data["items"])
        if completion < 1.0:
            suggestions.append(f"- For {phase}, focus on: {', '.join([item for item in data['items'] if not any(item.lower() in f[0].lower() for f in files)])}")
    if not suggestions:
        suggestions.append("- All phases complete! Consider expanding with new features.")
    return "\n".join(suggestions)

def build_report(files, commits, phases):
    """Build the full Markdown report."""
    report = "=== UH AI Build Repo Report ===\n\n"

    # Files section
    report += "Files Found:\n"
    for filepath, size, mtime in files:
        report += f"- {filepath} (Size: {size} bytes, Modified: {mtime})\n"
    report += "\n"

    # Commits section
    report += f"Recent Commits (Last {len(commits)}):\n"
    for commit in commits:
        report += f"- {commit}\n"
    report += "\n"

    # Roadmap check
    report += "Roadmap Process Check:\n"
    for phase, data in phases.items():
        report += f"{phase}: {data['found']}/{len(data['items'])} items found\n"
        report += f"  Completed: {', '.join([item for item in data['items'] if any(item.lower() in f[0].lower() for f in files)]) or 'None'}\n"
        report += f"  Missing/Lacking Logs: {', '.join([item for item in data['items'] if not any(item.lower() in f[0].lower() for f in files)]) or 'None'}\n"
    report += "\n"

    # Suggestions
    report += "Suggestions:\n"
    report += generate_suggestions(phases) + "\n"

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track UH AI Build repo progress.")
    parser.add_argument("--no-clone", action="store_true", help="Skip pulling latest changes.")
    parser.add_argument("--output-file", default="tracker_log.md", help="Output Markdown file.")
    args = parser.parse_args()

    if not args.no_clone:
        print("Pulling latest changes...")
        pull_latest()
    else:
        print("Skipping pull (using local state).")

    files = list_files_recursive()
    commits = get_recent_commits(limit=10)
    phases = check_roadmap_phases(files)

    report = build_report(files, commits, phases)
    with open(args.output_file, "w") as f:
        f.write(report)
    print(f"Report saved to {args.output_file}")

    # Add to script (after imports)
entry = input("Enter log entry (e.g., 'Baseline run: Loss 2.5'): ")
status = input("Roadmap status update: ")
update_log(entry)
update_roadmap(status)
commit_changes()