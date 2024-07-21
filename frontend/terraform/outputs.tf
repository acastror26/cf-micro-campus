output "frontend_url" {
  description = "The URL of the frontend application"
  value       = aws_cloudfront_distribution.frontend_distribution.domain_name
}
