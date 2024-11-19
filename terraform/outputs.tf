output "firestore_database_id" {
  value = google_firestore_database.database.name
  description = "El ID de la base de datos de Firestore creada."
}


output "function_url" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
  description = "La URL de la función de Google Cloud Functions desplegada."
}
