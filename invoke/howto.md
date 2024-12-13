# How to Use Invoke with `tasks.py` for Automation

This guide will help you use Invoke with the provided `tasks.py` script to automate common tasks like managing Homebrew packages and Git operations.

## Prerequisites

- **Python 3.x** installed (I use the latests 3.13)
- **Invoke** library installed (`pip install invoke`)
- `tasks.py` script in your project directory

## Installing Invoke

If you haven't installed Invoke yet, run:

```bash
pip install invoke
```

## Available Tasks

The `tasks.py` script includes the following tasks:

- `brew_manage`: Manages Homebrew packages (checks for outdated packages, updates, and upgrades)
- `git_manage`: Automates Git operations (status, add, commit, push, and checkout)

## Using Invoke

### List All Tasks

To see all available tasks, run:

```bash
invoke -l
```

### Execute a Task

Replace `<task_name>` with the name of the task you want to run:

```bash
invoke <task_name>
```

For example, to manage Homebrew packages:

```bash
invoke brew_manage
```

## Task Details

### `brew_manage`

Manages Homebrew packages:

- Checks for outdated packages
- Runs `brew update`
- Runs `brew upgrade`
- Handles conflicts by unlinking conflicting formulae if necessary

### `git_manage`

Automates Git operations:

1. **Status**: Shows the current status (`git status`)
2. **Checkout**: Prompts for a branch name and checks out to it (`git checkout -b 'branch_name'`)
3. **Add**: Stages all changes (`git add --all`)
4. **Commit**: Prompts for a commit message and commits (`git commit -m 'message'`)
5. **Push**: Pushes to the `master` branch (`git push origin master`)

## Running Git Operations

When you run:

```bash
invoke git_manage
```

You'll be prompted to:

- Enter the branch name
- Enter the commit message

## Notes

- Ensure you have the necessary permissions for Git operations.
- Make sure your local branch is up to date with the remote to avoid conflicts.
