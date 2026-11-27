# CloudRescue

CloudRescue is a self-healing FastAPI web application designed for deployment to AWS
Lambda using a container image. The project will demonstrate automated deployments,
health verification, and rollback using GitHub Actions, Terraform, ECR, CloudWatch,
GitHub OIDC, and Lambda versions and aliases.

## Technology

- Python and FastAPI
- Docker
- AWS Lambda container image and Function URL
- Amazon ECR
- Terraform
- GitHub Actions
- GitHub OIDC
- AWS CloudWatch

## Project structure

```text
app/                    FastAPI application
tests/                  Automated application tests
docker/                 Container image definition
terraform/              AWS infrastructure
scripts/                Deployment, health-check and rollback scripts
.github/workflows/      CI/CD workflows
```

## Local setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The application and test implementation will be added in subsequent project tasks.
