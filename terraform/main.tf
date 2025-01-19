provider "google" {
  project = "uoftha"
  region  = "us-central1"
}

resource "google_cloud_run_service" "flask_app" {
  name     = "flask-app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/uoftha/flask-container-repo/flask-app"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service  = google_cloud_run_service.flask_app.name
  location = google_cloud_run_service.flask_app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "url" {
  value = google_cloud_run_service.flask_app.status[0].url
}