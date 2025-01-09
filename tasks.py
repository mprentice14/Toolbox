from invoke import task, UnexpectedExit
import os
import sys

#-------------------Dictionary mapping cluster names to their ARNs-------------------#
CLUSTERS = {
    "eks-ap-south-1-non-prod": "arn:aws:eks:ap-south-1:442501350342:cluster/eks-ap-south-1-non-prod",
    "eks-ap-south-1-prod": "arn:aws:eks:ap-south-1:442501350342:cluster/eks-ap-south-1-prod",
    "eks-ap-south-1-testing": "arn:aws:eks:ap-south-1:442501350342:cluster/eks-ap-south-1-testing",
    "eks-ap-south-2-non-prod": "arn:aws:eks:ap-south-2:442501350342:cluster/eks-ap-south-2-non-prod",
    "eks-ap-south-2-prod": "arn:aws:eks:ap-south-2:442501350342:cluster/eks-ap-south-2-prod",
    "eks-cn-north-1-non-prod": "arn:aws-cn:eks:cn-north-1:474022772791:cluster/eks-cn-north-1-non-prod",
    "eks-cn-north-1-prod": "arn:aws-cn:eks:cn-north-1:474022772791:cluster/eks-cn-north-1-prod",
    "eks-us-east-1-dr": "arn:aws:eks:us-east-1:442501350342:cluster/eks-us-east-1-dr",
    "eks-us-west-2-non-prod": "arn:aws:eks:us-west-2:442501350342:cluster/eks-us-west-2-non-prod",
    "eks-us-west-2-prod": "arn:aws:eks:us-west-2:442501350342:cluster/eks-us-west-2-prod",
    "eks-us-west-2-testing": "arn:aws:eks:us-west-2:442501350342:cluster/eks-us-west-2-testing",
    "gke_c2fo-application_asia-south1_gke-asia-south1-non-prod": "gke_c2fo-application_asia-south1_gke-asia-south1-non-prod",
    "gke_c2fo-application_asia-south1_gke-asia-south1-prod": "gke_c2fo-application_asia-south1_gke-asia-south1-prod",
    "gke_c2fo-application_europe-west1_europe-dr": "gke_c2fo-application_europe-west1_europe-dr",
    "gke_c2fo-application_europe-west3_gke-europe-west3-non-prod": "gke_c2fo-application_europe-west3_gke-europe-west3-non-prod",
    "gke_c2fo-application_europe-west3_gke-europe-west3-prod": "gke_c2fo-application_europe-west3_gke-europe-west3-prod",
    "gke_c2fo-application_us-central1_us-central1-dr": "gke_c2fo-application_us-central1_us-central1-dr",
    "gke_c2fo-application_us-west1_gke-us-west1-non-prod": "gke_c2fo-application_us-west1_gke-us-west1-non-prod",
    "gke_c2fo-application_us-west1_gke-us-west1-prod": "gke_c2fo-application_us-west1_gke-us-west1-prod",
    "gke_c2fo-application_us-west1_gke-us-west1-testing": "gke_c2fo-application_us-west1_gke-us-west1-testing",
}

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
    c.run("git pull origin master")

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
def git_pr(c):
    "Create a new pull request"
    c.run("gh pr create -d -f -a mprentice14 -r C@FO/devops,tbplayer7,jacob-m-barnes,travisfennel,rontoc2,kuldeep14327,someshsharma21,mprentice14")

@task
def git_manage(c):
    "Managing Git: checking status, adding all files, committing, and pushing"
    git_status(c)
    git_add(c)
    git_commit(c)
    git_push(c)
    git_pr(c)

@task
def switch_cluster(c, cluster_name):
    "Switch to the specified EKS or GKE cluster"
    if cluster_name not in CLUSTERS:
        print(f"Cluster {cluster_name} not found.")
        return

    cluster_arn = CLUSTERS[cluster_name]
    print(f"Switching to cluster: {cluster_name} ({cluster_arn})")

    # Set the context for EKS clusters
    if cluster_arn.startswith("arn:aws:eks"):
        c.run(f"aws eks update-kubeconfig --name {cluster_name.split('/')[-1]} --region {cluster_arn.split(':')[3]}")
    # Set the context for GKE clusters
    elif cluster_arn.startswith("gke_"):
        project, location, cluster = cluster_arn.split('_')[1:]
        c.run(f"gcloud container clusters get-credentials {cluster} --zone {location} --project {project}")
    else:
        print(f"Unsupported cluster type for {cluster_name}")
