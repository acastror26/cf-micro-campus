provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "fastapi_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              docker run -d -p 80:8000 your_docker_image
              EOF

  tags = {
    Name = "fastapi-instance"
  }
}

output "instance_ip" {
  value = aws_instance.fastapi_instance.public_ip
}