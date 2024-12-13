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
def git_manage(c):
    "Managing Git: checking status, adding all files, committing, pulling, checkout and pushing"
    git_status(c)
    #git_checkout(c)
    git_add(c)
    git_commit(c)
    git_push(c)

def git_status(c):
    "Checking Git status"
    c.run("git status")

def git_add(c):
    "Adding all files to Git"
    c.run("git add --all")

def git_commit(c):
    "Committing to Git"
    commit_message = input("Enter commit message: ")
    c.run(f"git commit -m '{commit_message}'")

def git_push(c):
    "Pushing to Git"
    c.run("git push origin master")

#def git_checkout(c):
#    "Checking out to master branch"
#    branch = input("Enter branch name: ")
#    c.run("git checkout -b '{branch}'")
