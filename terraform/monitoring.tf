resource "google_monitoring_uptime_check_config" "health_check" {
  display_name = "${var.project_name}-health-uptime-check"
  timeout      = "10s"
  period       = "60s"

  http_check {
    path    = "/api/v1/health"
    port    = 443
    use_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = "finguard-ai-283915220530.us-central1.run.app"
    }
  }
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "${var.project_name}-alert-email"
  type         = "email"

  labels = {
    email_address = var.alert_email
  }
}

resource "google_monitoring_alert_policy" "health_check_failure" {
  display_name = "${var.project_name} - Health check failing"
  combiner      = "OR"

  conditions {
    display_name = "Uptime check failure"

    condition_threshold {
      filter          = "resource.type=\"uptime_url\" AND metric.type=\"monitoring.googleapis.com/uptime_check/check_passed\""
      comparison      = "COMPARISON_LT"
      threshold_value = 1
      duration        = "0s"

      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_FRACTION_TRUE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]

  alert_strategy {
    auto_close = "1800s"
  }
}
