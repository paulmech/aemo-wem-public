#!/usr/bin/env bash

set -eu

cat <<__EOF__
provider "aws" {
  region  = "$AWS_DEPLOY_REGION"

  default_tags {
    tags = var.default_tags
  }
}

terraform {
  backend "s3" {
    bucket         = "$TFSTATE_BUCKET"
    key            = "$TFSTATE_KEY"
    region         = "$TFSTATE_REGION"
    dynamodb_table = "$TFSTATE_DDB_TABLE"
  }
}
__EOF__
