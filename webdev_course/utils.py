import subprocess


def get_git_version():
    try:
        git_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
        return git_tag
    except subprocess.CalledProcessError:
        return "Unknown"
