# Organisation Snapshotting Lambda
A PoC script to produce a Markdown Report using GitHub Policy Data and push it to a GitHub Repository.

## Contents

- [Contents](#contents)
- [Getting Started](#getting-started)
- [Generating the PDF Report](#generating-the-pdf-report)
- [Design](#design)
  - [Process Flow](#process-flow)
- [Next Steps](#next-steps)

## Getting Started

1. Clone the repository:
   
    ```bash
    git clone https://github.com/ONS-Innovation/org-snapshotting-poc
    ```

2. Navigate to the project directory:
   
    ```bash
    cd org-snapshotting-poc
    ```

3. Create and activate a virtual environment:
   
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required packages:
   
    ```bash
    poetry install
    ```

5. Set up the environment variables:
   
    ```bash
    export AWS_ACCESS_KEY_ID=<aws_access_key_id> 
    export AWS_SECRET_ACCESS_KEY=<aws_secret_access_key_id>
    export AWS_SECRET_NAME=<path_to_pem_file>
    export GITHUB_ORG=<github_org>
    export GITHUB_APP_CLIENT_ID=<github_app_client_id>
    export ENVIRONMENT=<sdp-prod|sdp-dev>
    ```

6. Choose whether you want the script to push the report to the GitHub repository or not. If you want to push the report, set the following environment variable:
   
    ```bash
    export GITHUB_PUSH_REPORT=True
    ```
   If you do not want to push the report, set it to `False` or leave it unset.

7. Run the application:
   
    ```bash
    python3 src/main.py
    ```

This will generate a markdown report and push it to the specified GitHub repository (if enabled).

The repository containing the report is available at: [GitHub Policy Reports](https://github.com/ONS-Innovation/github-policy-reports) (Internal Only).

## Generating the PDF Report

Once the script has been executed, `report.md` will be created and, if enabled, pushed to the GitHub repository. Once the report is in the repository, a GitHub Action will automatically convert the markdown report to a PDF using Pandoc.

To simulate the PDF generation locally, you can run the following command:

```bash
docker run --rm \
    --volume "$(pwd):/data" \
    --user $(id -u):$(id -g) \
    pandoc/extra report.md -o output.pdf --template eisvogel
```

**Please Note:** This command requires Docker/Colima to be installed and running on your machine.

This will convert the `report.md` file to `output.pdf` in the same manner as the GitHub Action does.

You can view the generated PDF report in the `output.pdf` file.

## Design

![Designs](./design/org_snapshotting_PoC.drawio.png)

### Process Flow

1. Get JSON Data from AWS S3.
2. Process the JSON data to produce a markdown report.
3. Push the markdown report to a GitHub repository.
4. Setup a GitHub Action to convert the markdown report to PDF (Pandoc).
5. Release the PDF report to a GitHub release.
6. MkDocs Setup to host the markdown report on GitHub Pages (Optional).

## Next Steps

- Convert the Python script to a Lambda function.
- Create Terraform scripts to deploy the Lambda function and other resources.
- Linting + Testing.
- Update report to be of an agreed format:
    - Diagrams / Charts?
    - A3 or A4?
    - More information?
- Make which GitHub repository the report is pushed to configurable.
- Another markdown report to be generated excluding any Latex formatting so that it can be used as an output.
