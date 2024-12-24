from invoke import task, UnexpectedExit
import os
import sys

#------------------Brew Tasks------------------#

@task
def brew_manage(c):
    "Managing Brew: checking for outdated packages, updating, and upgrading"
    try:
        c.run("brew outdated")
        c.run("brew update")
        c.run("brew upgrade")
    except UnexpectedExit as e:
        if "Cannot install terragrunt because conflicting formulae are installed" in e.result.stderr:
            print("Conflicting formulae detected. Unlinking tgenv...")
            c.run("brew unlink tgenv")
            c.run("brew upgrade")
        elif "Cannot install tgenv because conflicting formulae are installed" in e.result.stderr:
            print("Conflicting formulae detected. Unlinking terragrunt...")
            c.run("brew unlink terragrunt")
            c.run("brew upgrade")
        elif "Cannot install tfenv because conflicting formulae are installed" in e.result.stderr:
            print("Conflicting formulae detected. Unlinking terraform...")
            c.run("brew unlink terraform")
            c.run("brew upgrade")
        elif "Cannot install terraform because conflicting formulae are installed" in e.result.stderr:
            print("Conflicting formulae detected. Unlinking tfenv...")
            c.run("brew unlink tfenv")
            c.run("brew upgrade")
        else:
            raise e

#------------------Git Tasks------------------#

@task
def git_status(c):
    "Check the status of the git repository"
    c.run("git status")

@task
def git_pull(c):
    "Pull changes from the remote repository"
    c.run("git pull origin main")

@task
def git_add(c):
    "Add all files to the git repository"
    c.run("git add .")

@task
def git_commit(c):
    "Commit changes to the git repository"
    commit_message = input("Enter commit message: ")
    c.run(f'git commit -m "{commit_message}"')

@task
def git_push(c):
    "Push changes to the remote repository"
    push_message = input("Enter push branch:")
    c.run("git push origin {push_message}")

@task
def git_pull_request(c):
    "Create a new pull request"
    c.run("gh pr create")

@task
def git_manage(c):
    "Managing Git: checking status, adding all files, committing, and pushing"
    git_status(c)
    git_pull(c)
    git_add(c)
    git_commit(c)
    git_push(c)

    