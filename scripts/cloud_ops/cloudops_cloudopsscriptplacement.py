import os
import shutil

# Base repo path
BASE_PATH = r"C:\Users\buche\docs\Desktop\REPOS\CloudOpsLab"

# Mapping of subfolders to files that belong there
FOLDER_MAPPING = {
    "scripts/portfolio_ops": [
        "commit_autofixer.py",
        "deep_repo_auditor.py",
        "repo_autofixer.py",
        "repo_lint_fixer.py",
        "repo_safe_autofixer.py",
        "repo_scanner.py",
        "repo_string_fixer.py",
        "ultimate_repo_validator.py",
    ],
    # You can add more folders here if needed
    # "scripts/monitoring": ["health_check.py", "alerts.py", "guardduty-enable.py"],
    # "scripts/self_healing": ["EC2-Auto-Recovery.py", "EC2_Start_Stop_Scheduler.py", "remediation.py"]
}

def move_files():
    for folder, files in FOLDER_MAPPING.items():
        target_folder = os.path.join(BASE_PATH, folder)
        os.makedirs(target_folder, exist_ok=True)

        for file_name in files:
            source_file = os.path.join(BASE_PATH, "scripts", file_name)
            target_file = os.path.join(target_folder, file_name)

            if os.path.exists(source_file):
                print(f"Moving {file_name} -> {folder}")
                shutil.move(source_file, target_file)
            else:
                print(f"WARNING: {file_name} not found in scripts/")

if __name__ == "__main__":
    move_files()
    print("File organization complete.")
