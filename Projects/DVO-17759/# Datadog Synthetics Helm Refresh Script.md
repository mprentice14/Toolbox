# Datadog Synthetics Helm Refresh Script

This Python script automates the process of fetching the latest Datadog Synthetics Private Location Helm chart version and updating a local Helm chart repository accordingly. It provides the following functionalities:

## Overview

1. **Fetch Latest Chart Version**  
    - Retrieves the newest version of the “synthetics-private-location” chart from Datadog’s Helm repository.

2. **Update Chart.yaml**  
    - Checks the `Chart.yaml` file for the chart dependency version.  
    - If a new version is found, updates the dependency version.  
    - Increments the Helm chart’s own version to reflect this change.

3. **Update CHANGELOG.md**  
    - Adds a new entry at the top of the `CHANGELOG.md` indicating the updated chart version and the current date.

4. **Logging and Error Handling**  
    - Writes logs to a dedicated log file.  
    - Backs up `Chart.yaml` before making changes and reverts to the backup if any error occurs during the update process.

## How It Works

1. **Fetching the Version**  
    - An HTTP GET request is sent to the Helm repository URL.  
    - The response is parsed to find the most recent chart version.  

2. **Updating Files**  
    - The script reads `Chart.yaml` to locate the dependencies section.  
    - It compares the current version with the newly fetched version and updates if different.  
    - The script then increments the local chart’s version (e.g., from 1.2.3 to 1.2.4).  
    - A new entry is prepended to `CHANGELOG.md` describing the update.

3. **Execution Flow**  
    - If the script can fetch the latest version successfully and then updates `Chart.yaml`, it proceeds to update `CHANGELOG.md`.  
    - If fetching the version fails, it logs an error and stops.  
    - If any update step fails, the script logs the error and restores the backup of `Chart.yaml`.

## Use Case

- **CI/CD Pipeline**: This script can be integrated into a continuous integration process to ensure automatic updates whenever a new Datadog Synthetics Private Location Helm chart version becomes available.
- **Local Development**: Developers maintaining custom Helm charts that depend on Datadog Synthetics can run this script to keep their local charts up to date without manually tracking releases.
