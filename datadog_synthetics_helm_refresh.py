import requests
import yaml

# URL to fetch the latest chart version
HELM_REPO_URL = "https://helm.datadoghq.com/index.yaml"
CHART_NAME = "synthetics-private-location"
CHART_YAML_PATH = "Chart.yaml"

def fetch_latest_chart_version():
    response = requests.get(HELM_REPO_URL)
    response.raise_for_status()
    index_yaml = yaml.safe_load(response.text)
    
    for entry in index_yaml['entries'][CHART_NAME]:
        return entry['version']

def update_chart_yaml(new_version):
    with open(CHART_YAML_PATH, 'r') as file:
        chart_yaml = yaml.safe_load(file)
    
    for dependency in chart_yaml['dependencies']:
        if dependency['name'] == CHART_NAME:
            current_version = dependency['version']
            if current_version != new_version:
                dependency['version'] = new_version
                with open(CHART_YAML_PATH, 'w') as file:
                    yaml.safe_dump(chart_yaml, file)
                print(f"Updated {CHART_NAME} version from {current_version} to {new_version}")
            else:
                print(f"{CHART_NAME} is already up-to-date with version {current_version}")
            break

if __name__ == "__main__":
    latest_version = fetch_latest_chart_version()
    update_chart_yaml(latest_version)