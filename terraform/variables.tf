variable "default_tags" {
  type        = map(string)
  description = "list of default tags to apply to all resources"
  default     = {}
}

variable "assume_role_arn" {
  type        = list(string)
  description = "optional role arn to assume"
  default     = []
}

variable "profile" {
  type        = string
  description = "optional aws profile name to use"
  default     = null
}

variable "aemowem_url" {
  type        = string
  description = "URL to the root of the AEMO WA data website"
}

variable "duckdb_download_url" {
  type    = string
  default = "https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-aarch64.zip"
}

variable "ssm_name_github_token" {
  type    = string
  default = "/workload/aemowem/github-pat"
}