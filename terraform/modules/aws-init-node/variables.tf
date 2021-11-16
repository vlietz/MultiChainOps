variable "node-count"{
    type = number
    description = "Count of the nodes to create"
    default = 1

}

variable "ami"{
    type = string
    default = "ami-09d9c897fc36713bf"
    description = "AMI Type"
}



variable "instance_type"{
    type = string
    default = "t4g.micro"
    description = "Instance Type"
}
variable "region"{
    type = string
    default = "us-west-2"
    description = "Instance Type"
}
variable "access_key"{
    type = string
    description = "AWS Access Key"
}
variable "secret_key"{
    type = string
    description = "AWS Secret Key"
}


variable "ssh_user"{
    type = string
    default = "ubuntu"
    description = "SSH User"
}
variable "private_key_path"{
    type = string
    description = "Path to .pem private key"
}
variable "aws_key_name"{
    type = string
}