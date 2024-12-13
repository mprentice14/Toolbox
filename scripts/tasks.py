from invoke import tasks
import os
import sys

#------------------Brew Tasks------------------#

@task
def brew_outdated(c):
    "Checking Brew for outdated packages"
    c.run("brew outdated")

@task
def brew_update(c):
    "Updating Brew"
    c.run("brew update")

@task
def brew_upgrade(c):
    "Upgrading Brew packages"
    c.run("brew upgrade")

#------------------Git Tasks------------------#

@task
def git_status(c):
    "Checking Git status"
    c.run("git status")

@task
def git_pull(c):
    "Pulling from Git"
    c.run("git pull")

@task
def git_push(c):
    "Pushing to Git"
    c.run("git push")

@task
def git_add(c):
    "Adding all files to Git"
    c.run("git add --all")

@task
def git_commit(c):
    "Committing to Git"
    commit_message = input("Enter commit message: ")
    c.run(f"git commit -m '{commit_message}'")