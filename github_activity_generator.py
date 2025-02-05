import os
import sys
import time
import random
import schedule
from datetime import datetime, timedelta
from git import Repo, GitCommandError

# Configuration
# Set the path to your local Git repository here
REPO_PATH = "E:/pro/activity-generator"  # Change this to your repository path
BRANCH_NAME = "auto-commits"             # Name of the sub-branch for fake commits
COMMIT_INTERVAL = 60                     # Interval between commits in seconds
SCHEDULE_INTERVAL = 5                    # Interval between scheduled commits in minutes
FAKE_FILE_PATH = "notes.txt"             # Path to the fake file for commits

# Initialize repository
repo = Repo(REPO_PATH)

# Checkout or create the sub-branch
def checkout_or_create_branch():
    git = repo.git
    branches = [head.name for head in repo.heads]
    if BRANCH_NAME in branches:
        git.checkout(BRANCH_NAME)
        print(f"Checked out existing branch '{BRANCH_NAME}'")
    else:
        git.checkout('-b', BRANCH_NAME)
        git.push('-u', 'origin', BRANCH_NAME)  # Set upstream tracking
        print(f"Created and checked out new branch '{BRANCH_NAME}'")

checkout_or_create_branch()

def generate_fake_content():
    """Generate random content for fake commits."""
    contents = [
        "Updated documentation for the API endpoints.",
        "Refactored the user authentication module.",
        "Fixed a bug in the payment processing function.",
        "Improved performance of the database queries.",
        "Added unit tests for the new feature.",
        "Enhanced security for the application.",
        "Optimized image loading on the homepage.",
        "Updated dependencies to the latest versions.",
        "Fixed typos in the README file.",
        "Implemented caching for faster load times."
    ]
    return random.choice(contents)

def create_fake_commit(commit_time):
    """Create a fake commit with legitimate-looking messages at a specific time."""
    fake_content = generate_fake_content()
    file_path = os.path.join(REPO_PATH, FAKE_FILE_PATH)
    with open(file_path, 'a') as fake_file:
        fake_file.write(f"{fake_content}\n")
    repo.git.add(FAKE_FILE_PATH)
    commit_message = fake_content  # Use the fake content as the commit message
    os.environ['GIT_COMMITTER_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        repo.git.commit(
            m=commit_message,
            author="Siddh Patel <siddhp1024@gail.com>",
            date=commit_time.strftime('%Y-%m-%d %H:%M:%S')
        )
        # Pull the latest changes to avoid non-fast-forward errors
        repo.git.fetch()
        repo.git.pull('origin', BRANCH_NAME, '--rebase')
        # Push the commit to the remote repository on the sub-branch
        repo.git.push('origin', BRANCH_NAME)
        print(f"Committed: {commit_message} at {commit_time}")
    except GitCommandError as e:
        print(f"Error committing changes: {e}")

def make_past_commits(start_date, max_commits_per_day):
    """Create commits from the start date to today with random numbers of commits per day."""
    end_date = datetime.now()
    current_date = start_date

    while current_date <= end_date:
        num_commits = random.randint(1, max_commits_per_day)
        for _ in range(num_commits):
            commit_time = current_date + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            create_fake_commit(commit_time)
            time.sleep(1)  # Small delay to prevent overwhelming Git
        current_date += timedelta(days=1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_activity_generator.py <start|stop|past|schedule> [options]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "past":
        if len(sys.argv) != 4:
            print("Usage: python github_activity_generator.py past <start_date> <max_commits_per_day>")
            sys.exit(1)
        start_date_str = sys.argv[2]
        max_commits_per_day = int(sys.argv[3])
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        make_past_commits(start_date, max_commits_per_day)
    else:
        print(f"Command '{command}' is not supported in this script.")
