resource "aws_sfn_state_machine" "sfn_inventory_refresh" {
  name       = "aemo-inventory-refresh"
  role_arn   = aws_iam_role.sfn_refresh_role.arn
  definition = <<EOF
{  
   "StartAt":"CallLambda",
   "States":{  
      "CallLambda":{  
         "Type":"Task",
         "Resource":"arn:aws:states:::lambda:invoke",
         "Parameters":{  
            "FunctionName":"${aws_lambda_function.aemo_inventory_function.arn}"
         },
         "Next": "CallCodebuild"
      },
      "CallCodebuild": {
        "Type": "Task",
        "Resource": "arn:aws:states:::codebuild:startBuild.sync",
        "Parameters": {
            "ProjectName": "${aws_codebuild_project.duckdb_maker.name}"
        },
        "End": true
      }
   }
}
EOF
}

data "aws_iam_policy_document" "sfn_policy_document" {
  statement {
    effect    = "Allow"
    resources = [aws_codebuild_project.duckdb_maker.arn]
    actions   = ["codebuild:StartBuild", "codebuild:BatchGetBuilds"]
  }
  statement {
    effect    = "Allow"
    resources = [aws_lambda_function.aemo_inventory_function.arn]
    actions   = ["lambda:Invoke*"]
  }
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule"
    ]
  }
}

data "aws_iam_policy_document" "sfn_assume_role_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["states.${local.region}.amazonaws.com"]
    }
    condition {
      variable = "aws:SourceAccount"
      test     = "StringEquals"
      values   = [local.account_id]
    }
  }
}

resource "aws_iam_role" "sfn_refresh_role" {
  name                 = "aemowem-sfn-refresh"
  path                 = "/aemowem/"
  assume_role_policy   = data.aws_iam_policy_document.sfn_assume_role_policy_document.json
  permissions_boundary = local.permission_boundary_arn
  inline_policy {
    name   = "sfn_refresh_policy"
    policy = data.aws_iam_policy_document.sfn_policy_document.json
  }
}



# make lambda run on 5 min schedule temporarily
resource "aws_cloudwatch_event_rule" "inventory_schedule_4timesdaily" {
  name                = "aemowem-inventory"
  description         = "Execute AEMO WEM inventory scrape"
  schedule_expression = "rate(6 hours)"
  state               = "ENABLED"

}

resource "aws_cloudwatch_event_target" "inventory_schedule_target" {
  rule      = aws_cloudwatch_event_rule.inventory_schedule_4timesdaily.name
  target_id = "SendToStepFunction"
  arn       = aws_sfn_state_machine.sfn_inventory_refresh.arn
  input     = "{}"
  role_arn  = aws_iam_role.sfn_target_role.arn
}

data "aws_iam_policy_document" "sfn_target_policy_document" {
  statement {
    effect    = "Allow"
    resources = [aws_sfn_state_machine.sfn_inventory_refresh.arn]
    actions = [
      "states:StartExecution"
    ]
  }
}

data "aws_iam_policy_document" "sfn_target_assume_role_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    condition {
      variable = "aws:SourceAccount"
      test     = "StringEquals"
      values   = [local.account_id]
    }
  }
}

resource "aws_iam_role" "sfn_target_role" {
  name                 = "aemowem-sfn-refresh-target-schedule"
  path                 = "/aemowem/"
  assume_role_policy   = data.aws_iam_policy_document.sfn_target_assume_role_policy_document.json
  permissions_boundary = local.permission_boundary_arn
  inline_policy {
    name   = "sfn_target_policy"
    policy = data.aws_iam_policy_document.sfn_target_policy_document.json
  }
}