"""A Python script to convert JSON policy data into a markdown report."""

import boto3
from botocore.exceptions import ClientError
import json

session = boto3.Session()
s3 = session.client('s3')
secret_manager = session.client('secretsmanager', region_name='eu-west-2')

# Get JSON data from S3
try:
    repositories = s3.get_object(
        Bucket="sdp-prod-policy-dashboard",
        Key="repositories.json"
    )

    secret_scanning = s3.get_object(
        Bucket="sdp-prod-policy-dashboard",
        Key="secret_scanning.json"
    )

    dependabot = s3.get_object(
        Bucket="sdp-prod-policy-dashboard",
        Key="dependabot.json"
    )

except ClientError as e:
    print(f"An error occurred: {e}")
    exit(1)

# Convert JSON data to Python dictionaries
repositories = json.loads(repositories['Body'].read().decode('utf-8'))
secret_scanning = json.loads(secret_scanning['Body'].read().decode('utf-8'))
dependabot = json.loads(dependabot['Body'].read().decode('utf-8'))

# Make Markdown report


# Push to GitHub Repository

