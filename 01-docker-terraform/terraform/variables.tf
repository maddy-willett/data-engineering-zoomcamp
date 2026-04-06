variable "project" {
    description = "Project"
    type = string
    default = "nytaxiproject-492423"
}

variable "region" {
    description = "Project Region"
    type = string
    default = "us-central1"
}

variable "location" {
    description = "Project Location"
    type = string
    default = "US"
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    type = string
    default = "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    type = string
    default = "nytaxiproject-492423-terra-bucket"
}

variable "gcs_storage_class" {
    description = "Bucket Storage Class"
    type = string
    default = "STANDARD"
}