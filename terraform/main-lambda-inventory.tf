data "aws_iam_policy_document" "aemo_inventory_deploy_role_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    condition {
      variable = "aws:SourceAccount"
      test     = "StringEquals"
      values   = [local.account_id]
    }
  }
}

data "aws_iam_policy_document" "aemo_inventory_deploy_role_policy_document" {
  statement {
    sid = "s3DeployPermissions"
    actions = [
      "s3:GetObject*",
      "s3:ListBucket",
      "s3:PutObject",
      "s3:GetBucketLocation"
    ]
    effect = "Allow"
    resources = [
      aws_s3_bucket.aemowem_data_bucket.arn,
      "${aws_s3_bucket.aemowem_data_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_role" "aemo_inventory_deploy_role" {
  name_prefix        = "lambda-aemo-inventory-"
  path               = "/aemowem/"
  assume_role_policy = data.aws_iam_policy_document.aemo_inventory_deploy_role_assume_policy.json
  inline_policy {
    name   = "s3-restrictions"
    policy = data.aws_iam_policy_document.aemo_inventory_deploy_role_policy_document.json
  }
  permissions_boundary = local.permission_boundary_arn
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  ]
}

resource "aws_lambda_function" "aemo_inventory_function" {
  filename         = local.lambda_local_file
  source_code_hash = filebase64sha256(local.lambda_local_file)
  function_name    = "aemo-inventory"
  role             = aws_iam_role.aemo_inventory_deploy_role.arn
  handler          = "function.lambda_handler"
  runtime          = "python3.10"
  environment {
    variables = {
      AEMOWEM_URL    = var.aemowem_url
      AEMOWEM_BUCKET = aws_s3_bucket.aemowem_data_bucket.id
      AEMOWEM_PREFIX = local.aemowem_inventory_prefix_jsonl
    }
  }
  timeout = 300
}



output "role_lambda_aemo_inventory" {
  value = aws_iam_role.aemo_inventory_deploy_role.arn
}