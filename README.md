# Organisation Snapshotting Lambda
A PoC tool to produce a PDF report from GitHub Policy Data.

## Contents

- [Contents](#contents)
- [Getting Started](#getting-started)
- [Design](#design)
  - [Process Flow](#process-flow)

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
    ```
6. Run the application:
    ```bash
    poetry run src/main.py
    ```

Go to `http://localhost:8501` in your web browser to view the application.

## Design

![Designs](./org_snapshotting_PoC.drawio.png)

### Process Flow

1. Get JSON Data from AWS S3.
2. Process the JSON data to produce a markdown report.
3. Push the markdown report to a GitHub repository.
4. Setup a GitHub Action to convert the markdown report to PDF (Pandoc).
5. Release the PDF report to a GitHub release.
6. MkDocs Setup to host the markdown report on GitHub Pages (Optional).
