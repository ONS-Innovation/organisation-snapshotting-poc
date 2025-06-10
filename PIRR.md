# Private/Internal Repository Reasoning Record (PIRR)
<!-- This template provides a structured format for documenting the rationale behind the requirement for a private or internal repository, ensuring that the decision-making process is transparent and well-documented. -->

## Repository Name
<!-- Specify the name of the repository for which this PIRR is being created -->
github-policy-reports

## Reason for Private/Internal Repository
<!-- Clearly state the specific reasons or requirements necessitating the use of a private or internal repository for this project -->
This repository contains markdown reports for ONSdigital's GitHub Usage Policy adherence. Although mainly insensitive, it does highlight some security flaws in repositories (i.e., the number of security alerts for the repository and if it has protected branches). Therefore, it is not suitable for public access.

## Sensitivity of Information
<!-- Describe the sensitivity of the information contained in the repository and why it requires restricted access -->
This repository contains markdown reports that highlight flaws in ONSdigital's GitHub Usage Policy adherence. While the information is not highly sensitive, it may expose certain security aspects of ONSdigital's repositories, such as the number of security alerts, giving threats a potential indication of which repositories to target.

## Access Control Needs
<!-- Explain the specific access control needs or restrictions that justify the use of a private or internal repository -->
ONS staff only.

## Collaboration Requirements
<!-- Outline any collaboration requirements that are better addressed through a private or internal repository as opposed to a public one -->
Ensure that this repository is not publicly accessible.

## Security and Compliance Considerations
<!-- Address any security or compliance considerations that influence the decision to use a private or internal repository -->
The repository is internal to avoid exposing the reports to the public.

## Additional Notes
<!-- Include any additional context, considerations, or relevant details pertaining to the need for a private or internal repository -->
There are no secrets or sensitive information within this repository, only the reports which may hint at where to look for flaws.