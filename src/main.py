"""A Python script to convert JSON policy data into a markdown report."""

import boto3
from botocore.exceptions import ClientError
import json
import os
import datetime
import pandas as pd
import github_api_toolkit
import requests
import base64

org = os.getenv('GITHUB_ORG', 'ONSdigital')
environment = os.getenv('ENVIRONMENT', 'sdp-prod')

session = boto3.Session()
s3 = session.client('s3')
secret_manager = session.client('secretsmanager', region_name='eu-west-2')

# Get JSON data from S3
try:
    repositories = s3.get_object(
        Bucket=f"{environment}-policy-dashboard",
        Key="repositories.json"
    )

    secret_scanning = s3.get_object(
        Bucket=f"{environment}-policy-dashboard",
        Key="secret_scanning.json"
    )

    dependabot = s3.get_object(
        Bucket=f"{environment}-policy-dashboard",
        Key="dependabot.json"
    )

except ClientError as e:
    print(f"An error occurred: {e}")
    exit(1)

# Convert JSON data to Python dictionaries
repositories = json.loads(repositories['Body'].read().decode('utf-8'))
secret_scanning = json.loads(secret_scanning['Body'].read().decode('utf-8'))
dependabot = json.loads(dependabot['Body'].read().decode('utf-8'))

# Convert JSON data to Pandas DataFrames (easier to manipulate and analyze)

df_repositories = pd.json_normalize(repositories)
df_secret_scanning = pd.json_normalize(secret_scanning)
df_dependabot = pd.json_normalize(dependabot)

# Add additional columns where necessary

df_repositories["is_compliant"] = df_repositories.any(axis="columns", bool_only=True)
df_repositories["is_compliant"] = df_repositories["is_compliant"].apply(lambda x: not x)

# Apply title case to type column in df_repositories
df_repositories["type"] = df_repositories["type"].str.title()

# Invert checks

## Since a check being True means that it has failed, we need to invert the checks
for column in df_repositories.columns[4:-1]:
    df_repositories[column] = df_repositories[column].apply(lambda x: not x if isinstance(x, bool) else x)

## We should also change the check names to match the inverted logic
maps = {
    "checklist.inactive": "active",
    "checklist.unprotected_branches": "protected_branches",
    "checklist.unsigned_commits": "signed_commits",
    "checklist.readme_missing": "has_readme",
    "checklist.license_missing": "has_license",
    "checklist.pirr_missing": "has_pirr",
    "checklist.gitignore_missing": "has_gitignore",
    "checklist.external_pr": "no_external_pr",
    "checklist.breaks_naming_convention": "follows_naming_convention",
    "checklist.secret_scanning_disabled": "secret_scanning_enabled",
    "checklist.push_protection_disabled": "push_protection_enabled",
    "checklist.dependabot_disabled": "dependabot_enabled",
    "checklist.codeowners_missing": "has_codeowners",
    "checklist.point_of_contact_missing": "has_point_of_contact"
}

df_repositories.rename(columns=maps, inplace=True)

# Make Markdown report

markdown_report = f"# {org} Audit Report ({datetime.datetime.now().strftime('%Y-%m-%d')})\n\n"

markdown_report += f"## Report Details\n\n"

markdown_report += f"- Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
markdown_report += f"- Organisation: {org}\n\n"

markdown_report += "## Contents\n\n"

markdown_report += "- [Organisation Overview](#organisation-overview)\n"
markdown_report += "- [Repository Compliance Breakdown](#repository-compliance-breakdown)\n"
markdown_report += "- [Secret Scanning Alerts Overview](#secret-scanning-alerts-overview)\n"
markdown_report += "- [Dependabot Alerts Overview](#dependabot-alerts-overview)\n"
markdown_report += "- [Repository Appendix](#repository-appendix)\n\n"

markdown_report += "\pagebreak\n\n"

markdown_report += "## Organisation Overview\n\n"

markdown_report += f"- Total Repositories: {len(repositories)}\n"
markdown_report += f"- Total Secret Scanning Alerts: {len(secret_scanning)}\n"
markdown_report += f"- Total Dependabot Alerts: {len(dependabot)}\n\n"

markdown_report += f"- Total Repository Compliance: {(df_repositories['is_compliant'].sum() / len(df_repositories))*100:.2f}%\n"
markdown_report += f"- Average Secret Scanning Alerts per Repository: {len(secret_scanning) / len(repositories):.2f}\n"
markdown_report += f"- Average Dependabot Alerts per Repository: {len(dependabot) / len(repositories):.2f}\n\n"

markdown_report += "\pagebreak\n\n"

markdown_report += "## Repository Compliance Breakdown\n\n"

least_complied_check = df_repositories.iloc[:, 4:-1].sum().idxmin()
markdown_report += f"- Least Complied to Check: {least_complied_check.replace('_', ' ').title()}\n\n"
markdown_report += "| Check Name | Total Compliant Repositories | Total Non-Compliant Repositories | Compliance Percentage |\n"
markdown_report += "|------------|------------------------------|----------------------------------|-----------------------|\n"

for column in df_repositories.columns[4:-1]:
    compliant_count = df_repositories[column].sum()

    markdown_report += f"| {column.replace("_"," ").title()} | {compliant_count} | {len(repositories) - compliant_count} | {compliant_count / len(repositories) * 100:.2f}% |\n"

markdown_report += "\n\pagebreak\n\n"

markdown_report += "## Secret Scanning Alerts Overview\n\n"

markdown_report += f"- Total Secret Scanning Alerts: {len(secret_scanning)}\n"

if len(secret_scanning) != 0:

    markdown_report += f"- Total Repositories with Secret Scanning Alerts: {df_secret_scanning['repository'].nunique()}\n"
    markdown_report += f"- Average Alerts per Repository: {len(secret_scanning) / df_secret_scanning['repository'].nunique():.2f}\n\n"

    markdown_report += "Top 5 Repositories with Most Secret Scanning Alerts:\n\n"

    markdown_report += "| Repository | Total Alerts |\n"
    markdown_report += "|------------|--------------|\n"

    top_secret_scanning_repos = df_secret_scanning['repository'].value_counts().head(5)
    for repo, count in top_secret_scanning_repos.items():
        markdown_report += f"| {repo} | {count} |\n"

markdown_report += "\n\pagebreak\n\n"

markdown_report += "## Dependabot Alerts Overview\n\n"

markdown_report += f"- Total Dependabot Alerts: {len(dependabot)}\n"

if len(dependabot) != 0:

    markdown_report += f"- Total Repositories with Dependabot Alerts: {df_dependabot['repository'].nunique()}\n"
    markdown_report += f"- Average Alerts per Repository: {len(dependabot) / df_dependabot['repository'].nunique():.2f}\n\n"

    markdown_report += "Top 5 Repositories with Most Dependabot Alerts:\n\n"

    markdown_report += "| Repository | Total Alerts |\n"
    markdown_report += "|------------|--------------|\n"

    top_dependabot_repos = df_dependabot['repository'].value_counts().head(5)
    for repo, count in top_dependabot_repos.items():
        markdown_report += f"| {repo} | {count} |\n"

    markdown_report += "\n### Alerts by Severity\n\n"

    markdown_report += "| Severity | Total Alerts | Percentage of Alerts |\n"
    markdown_report += "|----------|--------------|----------------------|\n"

    severity_counts = df_dependabot['severity'].value_counts()

    # Order severity counts by severity level
    severity_order = ["critical", "high", "medium", "low"]
    severity_counts = severity_counts.reindex(severity_order, fill_value=0)

    for severity, count in severity_counts.items():
        percentage = (count / len(dependabot)) * 100
        markdown_report += f"| {severity} | {count} | {percentage:.2f}% |\n"

markdown_report += "\n\pagebreak\n\n"

markdown_report += "## Repository Appendix\n\n"

count = 0

for repo_type in df_repositories["type"].unique():

    count += 1

    if count > 1:
        markdown_report += "\pagebreak\n\n"

    markdown_report += f"### {repo_type.title()} Repositories\n\n"
    
    df_type = df_repositories[df_repositories["type"] == repo_type]
    
    for compliance in df_repositories["is_compliant"].unique():

        markdown_report += f"#### {'Compliant' if compliance else 'Non-Compliant'} Repositories\n\n"

        df_type_compliance = df_type[df_type["is_compliant"] == compliance]

        # Remove columns that are not relevant for the report
        df_type_compliance = df_type_compliance.drop(columns=["created_at", "url", "is_compliant"])

        for column in df_type_compliance.columns:
            markdown_report += f" | {column.replace('_', ' ').title()}"

        markdown_report += " |\n"
        markdown_report += "|---------------" # Manually add separator for the first column to ensure larger width
        markdown_report += "|---" * (len(df_type_compliance.columns)-1) + "|\n"

        df_type_compliance = df_type_compliance.sort_values(by=["name"])
        for index, row in df_type_compliance.iterrows():
            markdown_report += "| " + " | ".join(str(row[col]) for col in df_type_compliance.columns) + " |\n"
        markdown_report += "\n"

with open("report.md", "w") as f:
    f.write(markdown_report)

# Push to GitHub Repository

secret_name = os.getenv("AWS_SECRET_NAME")
github_app_client_id = os.getenv("GITHUB_APP_CLIENT_ID")

secret = secret_manager.get_secret_value(SecretId=secret_name).get("SecretString")

token = github_api_toolkit.get_token_as_installation(org, secret, github_app_client_id)
rest = github_api_toolkit.github_interface(token[0])

response = rest.get(f"/repos/{org}/github-policy-reports/contents/report.md")
json = response.json()

sha = json.get("sha", None)

new_file_content = base64.b64encode(markdown_report.encode('utf-8'))

if sha:
    response = requests.put(
        url=f"https://api.github.com/repos/{org}/github-policy-reports/contents/report.md",
        headers={
            "Authorization": "token " + token[0]
        },
        json={
            "message": f"Update report for {org} on {datetime.datetime.now().strftime('%Y-%m-%d @ %H:%M')}",
            "content": new_file_content.decode('utf-8'),
            "sha": sha
        }
    )
