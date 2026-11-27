resource "aws_ecr_repository" "app" {
  name                 = var.project_name
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep the 20 newest and 5 tagged images"
      selection = {
        tagStatus     = "tagged"
        countType     = "imageCountMoreThan"
        countNumber   = 5
        tagPrefixList = ["sha-"]
      }
      action = { type = "expire" }
    }]
  })
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}"
  retention_in_days = 30
}

resource "aws_lambda_function" "app" {
  count = var.image_uri == "" ? 0 : 1

  function_name = var.project_name
  role          = aws_iam_role.lambda_execution.arn
  package_type  = "Image"
  image_uri     = var.image_uri
  architectures = ["x86_64"]
  timeout       = 30
  memory_size   = 512

  environment {
    variables = {
      APP_VERSION     = var.app_version
      ENVIRONMENT     = var.environment
      FORCE_UNHEALTHY = "false"
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
}

resource "aws_lambda_function_url" "app" {
  count = var.image_uri == "" ? 0 : 1

  function_name      = aws_lambda_function.app[0].function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["content-type"]
  }
}

resource "aws_lambda_permission" "function_url_invoke" {
  count = var.image_uri == "" ? 0 : 1

  statement_id             = "FunctionURLInvokeAllowPublicAccess"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.app[0].function_name
  principal                = "*"
  invoked_via_function_url = true
  depends_on               = [aws_lambda_function_url.app]
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "lambda_function_name" {
  value = var.image_uri == "" ? null : aws_lambda_function.app[0].function_name
}

output "function_url" {
  value = var.image_uri == "" ? null : aws_lambda_function_url.app[0].function_url
}
