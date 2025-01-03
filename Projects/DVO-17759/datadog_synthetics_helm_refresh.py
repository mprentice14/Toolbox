# --------------------- Imports --------------------- #
from datetime import datetime
from datetime import datetime as dt_now
import requests
import yaml
import os
import shutil
import logging

# --------------------- Constants --------------------- #
HELM_REPO_URL = "https://helm.datadoghq.com/index.yaml"
CHART_NAME = "synthetics-private-location"
CHART_YAML_PATH = "charts/datadog/Chart.yaml"
CHANGELOG_PATH = "charts/datadog/CHANGELOG.md"

# --------------------- Logging Configuration --------------------- #
logging.basicConfig(
    filename='charts/datadog/update_sythetic_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --------------------- Functions --------------------- #
def fetch_latest_chart_version():
    """
    Fetch the latest version of the specified chart from the Helm repository.
    """
    try:
        response = requests.get(HELM_REPO_URL)
        response.raise_for_status()
        index_yaml = yaml.safe_load(response.text)
        for entry in index_yaml['entries'][CHART_NAME]:
            return entry['version']
    except Exception as e:
        logging.error(f"Failed to fetch latest chart version: {e}")
        return None

def update_chart_yaml(new_version):
    """
    Update the Chart.yaml file with the new version for the specified dependency and increment the chart version.
    Returns True if the dependency version was updated, False otherwise.
    """
    backup_path = CHART_YAML_PATH + '.bak'
    try:
        # --------------------- Create Backup --------------------- #
        shutil.copyfile(CHART_YAML_PATH, backup_path)

        # --------------------- Read Chart.yaml --------------------- #
        with open(CHART_YAML_PATH, 'r') as file:
            lines = file.readlines()

        dependency_updated = False

        # --------------------- Update Dependency Version --------------------- #
        for idx, line in enumerate(lines):
            if 'dependencies:' in line:
                for dep_idx in range(idx + 1, len(lines)):
                    if 'version:' in lines[dep_idx]:
                        parts = lines[dep_idx].strip().split(':', 1)
                        current_version = parts[1].strip()
                        if current_version != new_version:
                            leading_space = lines[dep_idx][:len(lines[dep_idx]) - len(lines[dep_idx].lstrip())]
                            lines[dep_idx] = f"{leading_space}version: {new_version}\n"
                            logging.info(f"Updated {CHART_NAME} version from {current_version} to {new_version}")
                            dependency_updated = True
                        else:
                            logging.info(f"{CHART_NAME} is already up-to-date with version {current_version}")
                        break
                break

        # --------------------- Increment Chart Version --------------------- #
        if dependency_updated:
            for idx, line in enumerate(lines):
                if 'version:' in line and 'dependencies:' not in line:
                    parts = line.strip().split(':', 1)
                    try:
                        current_chart_version = parts[1].strip()
                        major, minor, patch = map(int, current_chart_version.split('.'))
                        new_chart_version = f"{major}.{minor}.{patch + 1}"
                    except ValueError:
                        logging.error(f"Error parsing chart version: {parts[1].strip()}")
                        return False
                    leading_space = line[:len(line) - len(line.lstrip())]
                    lines[idx] = f"{leading_space}version: {new_chart_version}\n"
                    logging.info(f"Updated chart version from {current_chart_version} to {new_chart_version}")
                    break

            # --------------------- Write Updates --------------------- #
            with open(CHART_YAML_PATH, 'w') as file:
                file.writelines(lines)
            logging.info("Updates applied successfully.")
            # Remove the backup after successful update
            os.remove(backup_path)
            return True
        else:
            logging.info("No updates were necessary.")
            os.remove(backup_path)
            return False
    except Exception as e:
        # --------------------- Error Handling --------------------- #
        shutil.copyfile(backup_path, CHART_YAML_PATH)
        logging.error(f"An error occurred during update: {e}")
        logging.info("Restored Chart.yaml from backup.")
        return False

def update_changelog(new_version):
    """
    Update the CHANGELOG.md file with the new version.
    """
    date_str = dt_now.now().strftime("%Y-%m-%d")
    changelog_entry = f"## {new_version} ({date_str})\n\n- Updated Datadog Synthetics {CHART_NAME} version to {new_version}\n\n"

    if os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, "r+") as changelog_file:
            content = changelog_file.read()
            changelog_file.seek(0, 0)
            changelog_file.write(changelog_entry + content)
    else:
        with open(CHANGELOG_PATH, "w") as changelog_file:
            changelog_file.write(changelog_entry)
    logging.info(f"CHANGELOG.md updated: Datadog Synthetics Helm Chart updated to {new_version}.")

# --------------------- Main Execution --------------------- #
if __name__ == "__main__":
    # Fetch the latest version and update the Chart.yaml file
    latest_version = fetch_latest_chart_version()
    if latest_version:
        if update_chart_yaml(latest_version):
            update_changelog(latest_version)
    else:
        logging.error("Failed to fetch the latest version.")