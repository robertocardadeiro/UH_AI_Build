import subprocess
import os
from datetime import datetime

# Config: Add your log files from roadmap
LOG_FILES = ["phase1_log.md", "UH_AI_Build_Roadmap.md"]  # Expand for phases
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def auto_commit(message="Auto-commit: Updated logs", push=False):
    os.chdir(REPO_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Optional: Append example summary (customize, e.g., read from training output)
    for log_file in LOG_FILES:
        if os.path.exists(log_file):
            with open(log_file, "a") as f:
                f.write(f"\n## Auto-Update at {timestamp}\n")
                f.write("- Progress: [e.g., Phase 2 MoE trained on Gutenberg subset; Perplexity: 4.5]\n")
                f.write("- Hardware: RTX 5090 used ~12GB VRAM (from dxdiag_specs.txt).\n")  # Pull from files if needed

    # Git add/commit
    subprocess.run(["git", "add"] + LOG_FILES)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        commit_msg = f"{message} at {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg])
        print("Committed logs.")
        if push:
            subprocess.run(["git", "pull", "origin", "main", "--rebase"])  # Safe pull
            subprocess.run(["git", "push", "origin", "main"])
            print("Pushed to main.")
    else:
        print("No changes to commit.")

if __name__ == "__main__":
    auto_commit(push=False)  # Run with push=True for auto-push (use sparingly to review changes)