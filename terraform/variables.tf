locals {
  data_lake_bucket = "prj-redfin-housing-markt-data"
}

variable "project" {
  description = "Project-ID"
  default = "omega-byte-447718-e2"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "US"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "redfin_housing_market"
}
