resource "aws_instance" "lulu_django_server" {
  ami                    = var.instance_ami
  instance_type          = var.instance_type
  vpc_security_group_ids = [var.sg_id]

  tags = {
    AppCode = var.app_code
  }
}