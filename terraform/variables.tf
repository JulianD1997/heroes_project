variable "project_id" {
  description = "El ID del proyecto de Google Cloud."
  type        = string
}

variable "region" {
  description = "La región donde se desplegarán los recursos de GCP."
  type        = string
  default     = "us-central1"
}

variable "firestore_location" {
  description = "La ubicación de la base de datos de Firestore."
  type        = string
  default     = "nam5"
}

variable "type" {
  type        = string
  description = "(Optional) The Type of the Database. Defaults to `FIRESTORE_NATIVE`."

  validation {
    condition     = contains(["FIRESTORE_NATIVE", "DATASTORE_MODE"], var.type)
    error_message = "Allowed Types: [\"FIRESTORE_NATIVE\", \"DATASTORE_MODE\"]."
  }

  default = "FIRESTORE_NATIVE"
}

variable "concurrency_mode" {
  type        = string
  description = "(Optional) The Concurrency Control Mode to use for this Database. Defaults to `OPTIMISTIC`."

  validation {
    condition     = contains(["OPTIMISTIC", "PESSIMISTIC", "OPTIMISTIC_WITH_ENTITY_GROUPS"], var.concurrency_mode)
    error_message = "Allowed Concurrency Control Modes: [\"OPTIMISTIC\", \"PESSIMISTIC\", \"OPTIMISTIC_WITH_ENTITY_GROUPS\"]."
  }

  default = "OPTIMISTIC"
}

variable "delete_protection_state" {
  type        = string
  description = "(Optional) State of Delete Protection for this Database. Defaults to `DELETE_PROTECTION_ENABLED`."

  validation {
    condition     = contains(["DELETE_PROTECTION_STATE_UNSPECIFIED", "DELETE_PROTECTION_DISABLED", "DELETE_PROTECTION_ENABLED"], var.delete_protection_state)
    error_message = "Allowed Delete Protection States: [\"DELETE_PROTECTION_STATE_UNSPECIFIED\", \"DELETE_PROTECTION_DISABLED\", \"DELETE_PROTECTION_ENABLED\"]."
  }

  default = "DELETE_PROTECTION_ENABLED"
}

variable "service_account_email" {
  description = "La dirección de correo del servicio de cuenta"
  type        = string
  sensitive   = true
}

variable "google_credentials" {
  description = "Credenciales de Google en formato JSON"
  type        = string
  default     = ""
}