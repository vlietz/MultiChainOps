provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key =  var.secret_key
}



#create node
resource "aws_instance" "node" {
  count = var.node_count
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.aws_key_name
  vpc_security_group_ids = ["${aws_security_group.webSG.id}"]
  //  vpc_security_group_ids = ["${aws_security_group.webSG.id}"]

  tags = {
    Name = "node-${count.index}"
  }




  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = var.ssh_user
    private_key = file(var.private_key_path)
  }

  provisioner "file" {
    source      = "./testnet"
    destination = "./testnet"
  }
  provisioner "remote-exec" {
    inline = [
      "set -x",
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install docker.io -y",
      "sudo add-apt-repository ppa:serokell/tezos -y && sudo apt-get update",
      "sudo apt-get install -y tezos-client",
      "sudo apt-get install -y tezos-node",
      "sudo apt-get install -y tezos-baker-010-ptgranad",
      "sudo apt-get install -y tezos-endorser-010-ptgranad",
      "sudo apt-get install -y tezos-accuser-010-ptgranad",

      "sudo docker run --network host -t -d --name node tezos/tezos-bare:master",
      "sudo docker cp ./testnet node:/home/tezos/testnet",
      "sudo docker exec node tezos-node identity generate",
      "sudo docker exec node sed -i \"s/127.0.0.1/${var.network_ip}/\" ./testnet",
      "sudo docker exec node cat testnet",
      "sudo docker exec node tezos-node config init --network=./testnet",
      "nohup sudo docker exec node tezos-node run --rpc-addr localhost:8732 --bootstrap-threshold=1 --rpc-addr :8733 &",
      "sleep 10",
      "cat nohup.out"
    ]
  }




}












// Terraform plugin for creating random ids
resource "random_id" "instance_id" {
  byte_length = 8
}

resource "aws_security_group" "webSG" {
  name        = "webSG-${random_id.instance_id.hex}"
  description = "Allow ssh  inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 9732
    to_port     = 9732
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 8732
    to_port     = 8732
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 8733
    to_port     = 8733
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
egress {
    from_port   = 8732
    to_port     = 8732
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 8733
    to_port     = 8733
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 80
    to_port     = 80
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