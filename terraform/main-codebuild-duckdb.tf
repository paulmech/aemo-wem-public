resource "aws_codebuild_project" "duckdb_maker" {
  name         = "aemo-inventory-duckdb-maker"
  service_role = aws_iam_role.aemo_inventory_codebuild_service.arn
  source {
    type      = "NO_SOURCE"
    buildspec = file("scripts/codebuild-buildspec.yaml")
  }
  artifacts {
    type = "NO_ARTIFACTS"
  }
  environment {
    image        = "aws/codebuild/amazonlinux2-aarch64-standard:3.0"
    compute_type = "BUILD_GENERAL1_SMALL"
    type         = "ARM_CONTAINER"
    environment_variable {
      name  = "DUCKDB_DOWNLOAD_URL"
      value = var.duckdb_download_url
    }
    environment_variable {
      name  = "MIGRATION_SCRIPT"
      value = "s3://${aws_s3_bucket.aemowem_data_bucket.id}/${local.migration_script_location_key}"
    }
    environment_variable {
      name  = "DUCKDB_DATABASE_NAME"
      value = local.duckdb_database_name
    }
    environment_variable {
      name  = "S3_DUCKDB_OUTPUT_BASE"
      value = "s3://${aws_s3_bucket.aemowem_data_bucket.id}/${local.aemowem_inventory_prefix_duckdb}"
    }
    environment_variable {
      name = "GITHUB_REPO"
      value = "paulmech/aemo-wem"
    }
    environment_variable {
      name = "GITHUB_WORKFLOW"
      value = "deploy-evidence.yaml"
    }
    environment_variable {
      name = "GITHUB_BRANCH"
      value = "main"
    }
    environment_variable {
      name = "GITHUB_TOKEN"
      value = "${var.ssm_name_github_token}"
      type = "PARAMETER_STORE"
    }
  }
}

resource "aws_s3_object" "migration_script" {
  bucket  = aws_s3_bucket.aemowem_data_bucket.id
  key     = local.migration_script_location_key
  content = templatefile("scripts/duckdb.sql.tftpl", { s3_location = "s3://${aws_s3_bucket.aemowem_data_bucket.id}/${local.aemowem_inventory_prefix_jsonl}" })
  etag    = filemd5("scripts/duckdb.sql.tftpl")
}

data "aws_iam_policy_document" "codebuild_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
    condition {
      test     = "StringEquals"
      values   = [local.account_id]
      variable = "aws:SourceAccount"
    }
  }
}

resource "aws_iam_role" "aemo_inventory_codebuild_service" {
  name                 = "aemowem-inventory-codebuild"
  path                 = "/aemowem/"
  permissions_boundary = local.permission_boundary_arn
  assume_role_policy   = data.aws_iam_policy_document.codebuild_assume_role.json
  inline_policy {
    policy = data.aws_iam_policy_document.codebuild_policy.json
    name   = "codebuild-inline-policy"
  }
}

data "aws_iam_policy_document" "codebuild_policy" {
  statement {
    sid       = "AllowFetchS3Scripts"
    effect    = "Allow"
    resources = ["${aws_s3_bucket.aemowem_data_bucket.arn}/${local.aemowem_inventory_prefix_base}/*"]
    actions   = ["s3:GetObject"]
  }

  statement {
    sid       = "AllowListData"
    effect    = "Allow"
    resources = [aws_s3_bucket.aemowem_data_bucket.arn]
    actions   = ["s3:ListBucket"]
  }
  statement {
    sid       = "AllowPutDuckdb"
    effect    = "Allow"
    resources = ["${aws_s3_bucket.aemowem_data_bucket.arn}/${local.aemowem_inventory_prefix_duckdb}/*"]
    actions   = ["s3:PutObject"]
  }
  statement {
    sid       = "AllowLogs"
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
  }

  statement {
    sid = "AllowSSMGetParameter"
    effect = "Allow"
    actions = ["ssm:GetParameter*"]
    resources = [
      "arn:aws:ssm:${local.region}:${local.account_id}:parameter${var.ssm_name_github_token}"
    ] 
  }
}

