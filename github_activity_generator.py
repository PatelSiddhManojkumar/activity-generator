import os
import sys
import time
import random
import schedule
from datetime import datetime, timedelta
from git import Repo, GitCommandError

# Configuration
REPO_PATH = "E:/pro/activity-generator"  # Path to your Git repository
COMMIT_INTERVAL = 60  # Interval between commits in seconds
SCHEDULE_INTERVAL = 1  # Interval between scheduled commits in minutes
FAKE_FILE_PATH = "fake_file.txt"  # Path to the fake file for commits

# Initialize repository
repo = Repo(REPO_PATH)

def generate_fake_content():
    """Generate random content for fake commits."""
    contents = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Vivamus lacinia odio vitae vestibulum vestibulum.",
        "Cras vehicula, mi vitae semper vehicula, lectus quam ullamcorper dui.",
        "Curabitur fringilla tortor orci, nec cursus arcu ultrices nec.",
        "Nam tristique justo vitae est suscipit, nec laoreet felis porttitor."
    ]
    return random.choice(contents)

def create_fake_commit():
    """Create a fake commit with random content."""
    with open(os.path.join(REPO_PATH, FAKE_FILE_PATH), 'a') as fake_file:
        fake_content = generate_fake_content()
        fake_file.write(f"{fake_content}\n")
    repo.git.add(FAKE_FILE_PATH)
    commit_message = f"Fake commit at {datetime.now()}: {fake_content[:30]}..."
    try:
        repo.git.commit(m=commit_message)
        repo.git.push()  # Push the commit to the remote repository
        print(f"Committed: {commit_message}")
    except GitCommandError as e:
        print(f"Error committing changes: {e}")

def start_commits():
    try:
        while True:
            if repo.is_dirty(untracked_files=True):
                repo.git.add(A=True)
                commit_message = f"Automated commit at {datetime.now()}"
                try:
                    repo.git.commit(m=commit_message)
                    repo.git.push()  # Push the commit to the remote repository
                    print(f"Committed: {commit_message}")
                except GitCommandError as e:
                    print(f"Error committing changes: {e}")
            else:
                print("No real changes to commit. Creating a fake commit...")
                create_fake_commit()
            time.sleep(COMMIT_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping commits...")

def make_past_commit(days_ago, num_commits):
    for _ in range(num_commits):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        commit_time = datetime.now() - timedelta(days=days_ago, hours=random_hour, minutes=random_minute)
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            commit_message = f"Past commit at {commit_time}"
        else:
            with open(os.path.join(REPO_PATH, FAKE_FILE_PATH), 'a') as fake_file:
                fake_content = generate_fake_content()
                fake_file.write(f"{fake_content}\n")
            repo.git.add(FAKE_FILE_PATH)
            commit_message = f"Past fake commit at {commit_time}: {fake_content[:30]}..."
        os.environ['GIT_COMMITTER_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            repo.git.commit(m=commit_message, date=commit_time)
            repo.git.push()  # Push the commit to the remote repository
            print(f"Committed: {commit_message}")
        except GitCommandError as e:
            print(f"Error committing changes: {e}")

def schedule_commit():
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        commit_message = f"Scheduled commit at {datetime.now()}"
        try:
            repo.git.commit(m=commit_message)
            repo.git.push()  # Push the commit to the remote repository
            print(f"Committed: {commit_message}")
        except GitCommandError as e:
            print(f"Error committing changes: {e}")
    else:
        print("No real changes to commit. Creating a fake commit...")
        create_fake_commit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_activity_generator.py <start|stop|past|schedule> [options]")
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "start":
        start_commits()
    elif command == "stop":
        print("To stop the script, use Ctrl+C.")
    elif command == "past":
        if len(sys.argv) != 4:
            print("Usage: python github_activity_generator.py past <days_ago> <num_commits>")
            sys.exit(1)
        days_ago = int(sys.argv[2])
        num_commits = int(sys.argv[3])
        make_past_commit(days_ago, num_commits)
    elif command == "schedule":
        schedule.every(SCHEDULE_INTERVAL).minutes.do(schedule_commit)
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping scheduled commits...")
    else:
        print(f"Unknown command: {command}")
