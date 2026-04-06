terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.26.0"
    }
  }
}

provider "google" {
  project = "nytaxiproject-492423"
  region  = "us-central1"
}

resource "google_storage_bucket" "project-bucket" {
  name                        = "nytaxiproject-492423-terra-bucket"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}