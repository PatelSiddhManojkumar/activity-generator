import os
import sys
import time
import random
import schedule
from datetime import datetime, timedelta
from git import Repo

# Configuration
REPO_PATH = "E:/pro/activity-generator"  # Path to your Git repository
COMMIT_INTERVAL = 60  # Interval between commits in seconds
SCHEDULE_INTERVAL = 1  # Interval between scheduled commits in minutes

# Initialize repository
repo = Repo(REPO_PATH)

def start_commits():
    try:
        while True:
            repo.git.add(A=True)
            commit_message = f"Automated commit at {datetime.now()}"
            repo.git.commit(m=commit_message)
            repo.git.push()  # Push the commit to the remote repository
            print(f"Committed: {commit_message}")
            time.sleep(COMMIT_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping commits...")

def make_past_commit(days_ago, num_commits):
    for _ in range(num_commits):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        commit_time = datetime.now() - timedelta(days=days_ago, hours=random_hour, minutes=random_minute)
        repo.git.add(A=True)
        commit_message = f"Past commit at {commit_time}"
        os.environ['GIT_COMMITTER_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
        repo.git.commit(m=commit_message, date=commit_time)
        repo.git.push()  # Push the commit to the remote repository
        print(f"Committed: {commit_message}")

def schedule_commit():
    repo.git.add(A=True)
    commit_message = f"Scheduled commit at {datetime.now()}"
    repo.git.commit(m=commit_message)
    repo.git.push()  # Push the commit to the remote repository
    print(f"Committed: {commit_message}")

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
