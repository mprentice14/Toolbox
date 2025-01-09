# **How to Use Invoke for Automation**

This guide will help you set up and use **Invoke** to streamline repetitive tasks like managing Git, Homebrew, or any custom workflows using a `tasks.py` file.

---

## **1. Install Invoke**

Ensure you have `invoke` installed in your Python environment.

Run:

```bash
pip install invoke
```

To verify:

```bash
invoke --version
```

---

## **2. Create Your `tasks.py` File**

The `tasks.py` file contains all the commands you want to automate. Place it somewhere convenient (e.g., in your `~/Documents/Toolbox`).

Example `tasks.py`:

```python
from invoke import task

@task
def git_status(c):
    """Check the status of the git repository"""
    c.run("git status")

@task
def brew_manage(c):
    """Manage Homebrew: check outdated, update, and upgrade"""
    c.run("brew outdated")
    c.run("brew update")
    c.run("brew upgrade")
```

---

## **3. Add `tasks.py` to Your Search Path**

To ensure Invoke knows where to find your `tasks.py` file:

- Add the directory containing `tasks.py` to your `PYTHONPATH`:

   ```bash
   export PYTHONPATH="$PYTHONPATH:/path/to/your/tasks_directory"
   ```

   Example:

   ```bash
   export PYTHONPATH="$PYTHONPATH:/Users/username/Documents/Toolbox"
   ```

- (Optional) Add the line to your `~/.zshrc` or `~/.bashrc` for persistence.

---

## **4. Run Tasks Using Invoke**

Invoke lets you run tasks by name.

1. **List available tasks**:

   ```bash
   invoke --search-root=/path/to/your/tasks_directory --list
   ```

2. **Run a specific task**:

   ```bash
   invoke --search-root=/path/to/your/tasks_directory git-status
   ```

---

## **5. Simplify with an Alias**

To make it easier, add an alias to your shell configuration:

1. Open `~/.zshrc` or `~/.bashrc`:

   ```bash
   nano ~/.zshrc
   ```

2. Add the alias:

   ```bash
   alias invoke-toolbox='invoke --search-root=/path/to/your/tasks_directory'
   ```

3. Reload your shell:

   ```bash
   source ~/.zshrc
   ```

Now you can use:

```bash
invoke-toolbox --list
invoke-toolbox git-status
```

---

## **6. Share Your Tasks File**

1. Copy your `tasks.py` file to their preferred directory.
2. Set up their `PYTHONPATH` and alias following this guide.
3. Enjoy running automated tasks with **one simple command**.

---

### Example Workflow

Imagine you need to:

1. Check Git status.
2. Pull the latest changes.
3. Push your changes.

You can define tasks like this:

```python
@task
def git_pull(c):
    """Pull changes from the remote repository"""
    c.run("git pull")

@task
def git_push(c):
    """Push changes to the remote repository"""
    c.run("git push")

@task
def git_manage(c):
    """Manage Git: status, pull, and push"""
    git_status(c)
    git_pull(c)
    git_push(c)
```

Then, just run:

```bash
invoke-toolbox git-manage
```

---

Now you and your teammates can automate tasks easily! 🚀
