provider "aws" {
  region = "us-west-2"  # Set your desired region
}

resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "my-frontend-bucket"  # Replace with a unique bucket name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

resource "aws_s3_bucket_object" "frontend_files" {
  for_each = fileset("./build", "**")

  bucket = aws_s3_bucket.frontend_bucket.bucket
  key    = each.value
  source = "./build/${each.value}"
  acl    = "public-read"
}

resource "aws_cloudfront_distribution" "frontend_distribution" {
  origin {
    domain_name = aws_s3_bucket.frontend_bucket.bucket_regional_domain_name
    origin_id   = "S3-frontend"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.frontend_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Frontend distribution"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-frontend"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_All"

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_cloudfront_origin_access_identity" "frontend_identity" {
  comment = "OAI for frontend S3 bucket"
}

output "frontend_url" {
  value = aws_cloudfront_distribution.frontend_distribution.domain_name
}
