Certainly! 
Here’s a cheat sheet of essential Git commands for fetching, pushing, and managing a repository during development.
This includes commands for basic setup, syncing changes, managing branches, and inspecting the repository status.

### Initial Setup

1. **Clone a Repository** (to fetch code from an existing GitHub repo):
   ```bash
   git clone https://github.com/YourUsername/YourRepo.git
   ```
   This will create a local copy of the GitHub repository on your computer.

2. **Initialize a New Repository** (if you don’t have a repo yet):
   ```bash
   git init
   git remote add origin https://github.com/YourUsername/YourRepo.git
   ```

### Committing and Pushing Changes

1. **Check Status** (to see modified files):
   ```bash
   git status
   ```

2. **Stage Files for Commit**:
   - To stage all modified files:
     ```bash
     git add .
     ```
   - To stage a specific file:
     ```bash
     git add filename
     ```

3. **Commit Changes** (create a snapshot of your changes):
   ```bash
   git commit -m "Your commit message here"
   ```

4. **Push Changes to GitHub**:
   ```bash
   git push origin main
   ```

### Fetching Updates and Syncing with GitHub

1. **Pull Changes from GitHub** (to get the latest changes from the remote repo):
   ```bash
   git pull origin main
   ```

2. **Fetch Without Merging** (get updates from the remote repo without merging them into your code):
   ```bash
   git fetch origin
   ```

### Branch Management

1. **Create a New Branch** (useful for developing new features or making changes):
   ```bash
   git checkout -b branch-name
   ```

2. **Switch to an Existing Branch**:
   ```bash
   git checkout branch-name
   ```

3. **Push a New Branch to GitHub**:
   ```bash
   git push -u origin branch-name
   ```

4. **Merge a Branch into Main** (after finishing changes in a branch, merge them back to main):
   - First, switch to the `main` branch:
     ```bash
     git checkout main
     ```
   - Then, merge the changes:
     ```bash
     git merge branch-name
     ```

5. **Delete a Branch** (after it’s merged or no longer needed):
   - Locally:
     ```bash
     git branch -d branch-name
     ```
   - On GitHub:
     ```bash
     git push origin --delete branch-name
     ```

### Inspecting Commit History

1. **View Commit History**:
   ```bash
   git log
   ```

2. **View Commit History as a Graph**:
   ```bash
   git log --oneline --graph --all
   ```

### Undoing Changes

1. **Undo Changes in a File** (revert the file back to the last committed state):
   ```bash
   git checkout -- filename
   ```

2. **Unstage Files** (remove from the staging area without deleting the changes):
   ```bash
   git reset filename
   ```

3. **Undo Last Commit** (keep the changes unstaged):
   ```bash
   git reset --soft HEAD~1
   ```

### Other Helpful Commands

1. **View Configurations**:
   ```bash
   git config --list
   ```

2. **Set Global Username and Email** (only needed once per setup):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

3. **Remove Remote and Re-add** (if you need to reset the connection to GitHub):
   ```bash
   git remote remove origin
   git remote add origin https://github.com/YourUsername/YourRepo.git
   ```

These commands cover most tasks you’ll need for development with Git. Let me know if you need more specific details on any command!