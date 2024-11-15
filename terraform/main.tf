terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
}

# Configuración del proveedor de Google Cloud
provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Firestore Database
resource "google_firestore_database" "database" {
  provider                = google-beta
  name                    = "(default)"
  location_id             = var.firestore_location
  type                    = var.type
  concurrency_mode        = var.concurrency_mode
  delete_protection_state = var.delete_protection_state
}

# Storage Bucket
resource "google_storage_bucket" "firestore_bucket" {
  name                        = "autonomous-time-418513.firebasestorage.app"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true
}

# Subir Function
resource "google_storage_bucket_object" "object" {
  name   = "function.zip"
  bucket = google_storage_bucket.firestore_bucket.name
  source = "../cloud_functions/function.zip"
}

# Cloud Function
resource "google_cloudfunctions2_function" "function" {
  name        = "project-function"
  location    = var.region
  description = "test function"
  
  # Configuración del build
  build_config {
    runtime     = "python310"
    entry_point = "generate_thumbnail"
    source {
      storage_source {
        bucket = google_storage_bucket.firestore_bucket.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  # Configuración del evento
  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.storage.object.v1.finalized"
    retry_policy   = "RETRY_POLICY_RETRY"
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.firestore_bucket.name
    }
  }

  # Configuración de servicio
  service_config {
    max_instance_count            = 3
    min_instance_count            = 1
    available_memory              = "256M"
    timeout_seconds               = 60
    all_traffic_on_latest_revision = true
    service_account_email         = "804582757970-compute@developer.gserviceaccount.com"
  }
}

# IAM para invocación
resource "google_cloud_run_service_iam_member" "default" {
  location = google_cloudfunctions2_function.function.location
  service  = google_cloudfunctions2_function.function.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
