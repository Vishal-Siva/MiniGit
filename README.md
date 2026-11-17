# MiniGit – A Simple Version Control System in Python

## About the Project

MiniGit is a small version control system that I built using Python.

I started this project to understand how Git works internally instead of just using Git commands. While building it, I learned how files are tracked, how commits are stored, and how branches work.

It is a beginner-level project, but I tried to implement the basic ideas behind version control on my own.

## Features

- Initialize a MiniGit repository.
- Add files to the staging area.
- Track file contents using SHA-1 hashing.
- Store file contents as objects.
- Create commits with messages and timestamps.
- View commit history.
- Restore files from previous commits.
- Create new branches.
- Switch between branches.
- Check for uncommitted changes before switching branches.
- Handle common errors such as missing files and corrupted JSON data.

## Technologies Used

- Python
- JSON
- Hashing (SHA-1)
- Python standard library

## Project Structure

```text
MiniGit Project/
│
├── .minigit/
│   ├── objects/
│   ├── commit/
│   ├── branches/
│   ├── HEAD
│   └── index.json
│
├── minigit/
│   ├── __init__.py
│   ├── hashing.py
│   └── commit.py
│
├── tests/
│   └── test_minigit.py
│
├── main.py
└── README.md
```

## How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/MiniGit.git
   ```

2. Open the project folder:

   ```bash
   cd MiniGit
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Select an option from the menu to use MiniGit.

## Available Operations

| Option | Operation |
|---|---|
| 1 | Initialize repository |
| 2 | Add a file |
| 3 | Create a commit |
| 4 | Show commit history |
| 5 | Restore a file |
| 6 | Create a branch |
| 7 | Switch branch |
| 8 | Exit |

Run `python main.py` again whenever you want to perform another operation.

## What I Learned

Building MiniGit helped me understand several concepts that I had previously only used through Git:

- How hashing can identify file contents.
- How a staging area keeps track of files.
- How commits store snapshots of tracked files.
- How branches maintain references to commits.
- How file restoration works.
- How to handle errors and test different situations in Python.

## Current Limitations

- MiniGit is designed for text-based files.
- Only selected file extensions are accepted through the application.
- It works locally and does not support remote repositories.
- It is a learning project and is not intended to replace Git.

## Author

Built independently as a Python learning project to understand the basic working principles of version control systems.

