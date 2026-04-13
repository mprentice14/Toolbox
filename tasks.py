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
def git_clone(c):
    "Clone a repository"
    repository_url = input("Enter the repository URL: ")
    c.run(f"git clone {repository_url}")

@task
def git_checkout(c):
    "Checkout a branch"
    branch_name = input("Enter the branch name: ")
    c.run(f"git checkout {branch_name}")

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
    c.run("gh pr create -d -f -a mprentice14 -r C@FO/devops,tbplayer7,jacob-m-barnes,MonaFraise,rontoc2,kuldeep14327,someshsharma21,mprentice14")

@task
def git_manage(c):
    "Managing Git: checking status, adding all files, committing, and pushing"
    git_status(c)
    git_add(c)
    git_commit(c)
    git_push(c)
    git_pr(c)

#------------------Kubectl Tasks------------------#

@task
def kubectl_get_configs(c):
    "Get the Kubernetes configurations"
    c.run("kubectl config get-contexts")


@task
def kubectl_use_config(c):
    "Use a Kubernetes configuration"
    result = c.run("kubectl config get-contexts -o name", hide=True)
    contexts = result.stdout.splitlines()
    
    if not contexts:
        print("No contexts found.")
        return
    
    print("Available contexts:")
    for i, context in enumerate(contexts):
        print(f"{i}: {context}")
    
    selected_index = int(input("Enter the number of the context you want to use: "))
    
    if selected_index < 0 or selected_index >= len(contexts):
        print("Invalid selection.")
        return
    
    selected_context = contexts[selected_index]
    c.run(f"kubectl config use-context {selected_context}")

@task
def kubectl_get_namespaces(c):
    "Get the namespaces in the Kubernetes cluster"
    c.run("kubectl get namespaces")

@task
def kubectl_delete_namespace(c):
    "Delete a namespace in the Kubernetes cluster"
    namespace_name = input("Enter the namespace name: ")
    c.run(f"kubectl delete namespace {namespace_name}")

@task
def kubectl_get_nodes(c):
    "Get the nodes in the Kubernetes cluster"
    c.run("kubectl get nodes")

@task
def kubectl_clear_context(c):
    "Clear the current Kubernetes context"
    c.run("kubectl config unset current-context")
    print("Kubernetes context has been cleared.")

#------------------K9s Tasks------------------#

@task
def k9s_launch(c):
    "Launch k9s for the current Kubernetes context"
    c.run("k9s")

@task
def k9s_with_context(c):
    "Select a Kubernetes context and launch k9s"
    result = c.run("kubectl config get-contexts -o name", hide=True)
    contexts = result.stdout.splitlines()
    
    if not contexts:
        print("No contexts found.")
        return
    
    print("Available contexts:")
    for i, context in enumerate(contexts):
        print(f"{i}: {context}")
    
    selected_index = int(input("Enter the number of the context you want to use: "))
    
    if selected_index < 0 or selected_index >= len(contexts):
        print("Invalid selection.")
        return
    
    selected_context = contexts[selected_index]
    c.run(f"kubectl config use-context {selected_context}")
    print(f"Switched to context: {selected_context}")
    print("Launching k9s...")
    c.run("k9s")

@task
def k9s_with_namespace(c):
    "Select a namespace and launch k9s"
    result = c.run("kubectl get namespaces -o name", hide=True)
    namespaces = [ns.replace('namespace/', '') for ns in result.stdout.splitlines()]
    
    if not namespaces:
        print("No namespaces found.")
        return
    
    print("Available namespaces:")
    for i, namespace in enumerate(namespaces):
        print(f"{i}: {namespace}")
    
    selected_index = int(input("Enter the number of the namespace you want to use: "))
    
    if selected_index < 0 or selected_index >= len(namespaces):
        print("Invalid selection.")
        return
    
    selected_namespace = namespaces[selected_index]
    print(f"Launching k9s in namespace: {selected_namespace}")
    c.run(f"k9s -n {selected_namespace}")

@task
def k9s_full(c):
    "Select context and namespace, then launch k9s"
    # Select context
    result = c.run("kubectl config get-contexts -o name", hide=True)
    contexts = result.stdout.splitlines()
    
    if not contexts:
        print("No contexts found.")
        return
    
    print("Available contexts:")
    for i, context in enumerate(contexts):
        print(f"{i}: {context}")
    
    selected_index = int(input("Enter the number of the context you want to use: "))
    
    if selected_index < 0 or selected_index >= len(contexts):
        print("Invalid selection.")
        return
    
    selected_context = contexts[selected_index]
    c.run(f"kubectl config use-context {selected_context}")
    print(f"Switched to context: {selected_context}")
    
    # Select namespace
    result = c.run("kubectl get namespaces -o name", hide=True)
    namespaces = [ns.replace('namespace/', '') for ns in result.stdout.splitlines()]
    
    if not namespaces:
        print("No namespaces found. Launching k9s with default namespace...")
        c.run("k9s")
        return
    
    print("\nAvailable namespaces:")
    for i, namespace in enumerate(namespaces):
        print(f"{i}: {namespace}")
    
    selected_index = int(input("Enter the number of the namespace you want to use (or -1 for all): "))
    
    if selected_index == -1:
        print("Launching k9s for all namespaces...")
        c.run("k9s")
    elif selected_index < 0 or selected_index >= len(namespaces):
        print("Invalid selection.")
        return
    else:
        selected_namespace = namespaces[selected_index]
        print(f"Launching k9s in namespace: {selected_namespace}")
        c.run(f"k9s -n {selected_namespace}")

#------------------Vault Tasks------------------#

@task
def vault_test(c):
    "Login to Vault testing environment (us-west-2)"
    vault_addr = 'https://vault-us-west-2-testing.c2fo.com'
    print(f"Setting VAULT_ADDR to {vault_addr}")
    c.run(f'VAULT_ADDR="{vault_addr}" vault login -no-print', pty=True)

@task
def vault_non(c):
    "Login to Vault non-prod environment (us-west-2)"
    vault_addr = 'https://vault-us-west-2-non-prod.c2fo.com'
    print(f"Setting VAULT_ADDR to {vault_addr}")
    c.run(f'VAULT_ADDR="{vault_addr}" vault login -no-print', pty=True)

@task
def vault_prod(c):
    "Login to Vault production environment (us-west-2)"
    vault_addr = 'https://vault-us-west-2.c2fo.com'
    print(f"Setting VAULT_ADDR to {vault_addr}")
    c.run(f'VAULT_ADDR="{vault_addr}" vault login -no-print', pty=True)

@task
def vault_east_non(c):
    "Login to Vault non-prod environment (us-east-1)"
    vault_addr = 'https://vault-us-east-1-non-prod.c2fo.com'
    print(f"Setting VAULT_ADDR to {vault_addr}")
    c.run(f'VAULT_ADDR="{vault_addr}" vault login -no-print', pty=True)

@task
def vault_east(c):
    "Login to Vault production environment (us-east-1)"
    vault_addr = 'https://vault-us-east-1-prod.c2fo.com'
    print(f"Setting VAULT_ADDR to {vault_addr}")
    c.run(f'VAULT_ADDR="{vault_addr}" vault login -no-print', pty=True)

