#general settings
provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key =  var.secret_key
}



#create node
resource "aws_instance" "init_node" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.aws_key_name
  vpc_security_group_ids = ["${aws_security_group.webSG.id}"]

  tags = {
    Name = "aws_init_node"
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
  #  provisioner "file" {
  #   source      = "./baker.sh"
  #   destination = "./baker.sh"
  # }
  provisioner "file" {
    source      = "./params.json"
    destination = "./params.json"
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
      # "sudo apt-get install -y tezos-baker-010-ptgranad",
      # "sudo apt-get install -y tezos-endorser-010-ptgranad",
      # "sudo apt-get install -y tezos-accuser-010-ptgranad",

      "sudo docker run --network host -t -d --name node tezos/tezos-bare:master",
      "sudo docker cp ./testnet node:/home/tezos/testnet",
      "sudo docker exec node tezos-node identity generate",
      "sudo docker exec node sed -i \"s/127.0.0.1//\" ./testnet",
      "sudo docker exec node cat testnet",
      "sudo docker exec node tezos-node config init --network=./testnet",
      "nohup sudo docker exec node tezos-node run --rpc-addr localhost:8732 --bootstrap-threshold=1 --rpc-addr :8733 &",
      "sleep 10",
      "cat nohup.out",

      "sudo docker exec node tezos-client import secret key activator unencrypted:edsk31vznjHSSpGExDMHYASz45VZqXN4DPxvsa4hAyY8dHM28cZzp6",
      "sudo docker exec node tezos-client gen keys baker",
      "sudo docker exec node tezos-client show address baker",
      "genesis_key=\"$( sudo docker exec node tezos-client show address baker  | sed --quiet --expression='s/^.*Public Key: //p')\"",
      "sed -i \"s/key1/$${genesis_key}/\" ./params.json",
      "cat params.json",
      "sudo docker cp ./params.json node:/home/tezos/params.json",

      "sudo docker exec node tezos-client activate protocol PtGRANADsDU8R9daYKAgWnQYAJ64omN1o3KMGVCykShA97vQbvV with fitness 1 and key activator and parameters params.json",

      "sleep 10",
      "cat nohup.out",
      # "sudo docker cp ./baker.sh node:/home/tezos/baker.sh",
      # "nohup sudo docker exec node /bin/sh baker.sh &> baker.out &",
      # "sleep 5",
      # "cat baker.out"
    ]
  }




}













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