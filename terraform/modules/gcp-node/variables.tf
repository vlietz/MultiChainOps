variable "network_ip" {
  type        = string
  description = "Public IP of the init-node"

}
variable "is_init_node" {
  type        = bool
  description = "Bool if the node shall function as init node"
  default     = false

}
variable "project_name" {
  type        = string
  description = "GCP Project Name"
  default     = "test1resinfra"
}
variable "region" {
  type        = string
  description = "Instance Region"
  default     = "us-west1-a"
}
variable "machine_type" {
  type        = string
  description = "Instance Machine Type"
  default     = "e2-medium"
}
variable "image" {
  type        = string
  description = "Instance Image"
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
}
variable "ssh_user" {
  type        = string
  description = "SSH User"
}
variable "private_key_file" {
  type        = string
  description = "Path to the private key file for ssh login"
}
variable "credentials_file" {
  type        = string
  description = "Path to the credentials file"
}
variable "node_count" {
  type        = number
  description = "Node count"
  default     = 1
}


