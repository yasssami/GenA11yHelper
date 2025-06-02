provider "aws" {  
  access_key = var.aws_access_key  
  secret_key = var.aws_secret_key  
  region     = var.region  
}  

# prompt versioning w/ s3 buckets
resource "aws_s3_bucket" "prompts" {

  bucket = "gena11yhelper-prompts-${random_id.suffix.hex}"

  acl    = "private"  
  versioning { enabled = true }  
}  

data "aws_ami" "ubuntu" {
  most_recent = truell
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# free tier e2c instance
resource "aws_instance" "app" {  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"  
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
	#!/bin/bash
	sudo apt update
	sudo apt install -y docker.io
	sudo systemctl start docker
  sudo usermod -aG docker ubuntu
EOF

}  

resource "aws_security_group" "app_sg" {  

  name = "gena11y-sg-${random_id.suffix.hex}"

  # streamlit ingress
  ingress {  
    from_port   = 8501 
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # deployment ingress
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {  
    from_port   = 0  
    to_port     = 0  
    protocol    = "-1"  
    cidr_blocks = ["0.0.0.0/0"]  
  }  
}  

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "deployer" {
  key_name   = "gena11y-deploy-key-${random_id.suffix.hex}"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

output "public_ip" {
  value = aws_instance.app.public_ip
}

output "ssh_private_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}

resource "random_id" "suffix" {
  byte_length = 4
}