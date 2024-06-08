resource "aws_s3_bucket" "aemowem_data_bucket" {
  bucket = "aemowem-data-${local.region}-${local.account_id}"
}

resource "aws_s3_bucket_lifecycle_configuration" "aemowem_data_bucket_lifecycle" {
  bucket = aws_s3_bucket.aemowem_data_bucket.id
  rule {
    id = "RemoveInventoryDataOlderThan1Days"
    expiration {
      days = 1
    }
    status = "Enabled"
    filter {
      prefix = local.aemowem_inventory_prefix_jsonl
    }
  }
  rule {
    id = "RemoveDuckDbOlderThan1Days"
    expiration {
      days = 1
    }
    status = "Enabled"
    filter {
      prefix = local.aemowem_inventory_prefix_duckdb
    }
  }
}
