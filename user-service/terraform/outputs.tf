output "instance_public_ip" {
  value = aws_instance.fastapi_instance.public_ip
}