# GitHub Policy Reports (PoC)

This repository contains a proof of concept (PoC) tool to produce markdown and PDF reports from GitHub Policy Data. The reports are generated from the data collected by the GitHub Policy Dashboard.

This repository contains the following components:
- **Lambda Function**: A serverless function that processes the GitHub Policy Data and generates markdown reports.
- **GitHub Action**: A workflow that converts the markdown reports to PDF and releases them to GitHub.
- **Markdown Reports**: The generated markdown reports that provide insights into the GitHub Policy Data.
- **MkDocs**: A static site generator that hosts the markdown reports on GitHub Pages (optional).
- 