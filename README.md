# GitHub Activity Generator

A Python script to generate GitHub activity with automated and scheduled commits, including fake commits. Ideal for maintaining consistent activity on GitHub.

## Features
- Automatic commits at regular intervals
- Scheduled commits using the `schedule` library
- Fake commits to simulate activity
- Commits for every day in the past year with random numbers of commits

## Requirements
- Python 3.x
- `GitPython` and `schedule` libraries

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/activity-generator.git
    cd activity-generator
    ```

2. **Install dependencies**:
    ```bash
    pip install gitpython schedule
    ```

## Usage

1. **Start Automatic Commits**:
    ```bash
    python github_activity_generator.py start
    ```

2. **Stop Automatic Commits**:
    - Press `Ctrl+C` in the terminal.

3. **Make Past Commits**:
    ```bash
    python github_activity_generator.py past <days_ago> <num_commits>
    ```
    Example:
    ```bash
    python github_activity_generator.py past 7 5
    ```

4. **Schedule Automatic Commits**:
    ```bash
    python github_activity_generator.py schedule
    ```

5. **Create Commits for Every Day in the Past Year**:
    ```bash
    python github_activity_generator.py yearly
    ```

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For questions or feedback, please contact [help.sid.dev@gmail.com](mailto:help.sid.dev@gmail.com).
