# Tezos-Testnet-Multicloud

This README will describe how to deploy a Tezos test-network in a multicloud environment. 

Current supported cloud-providers are AWS and GCP.

## General overview

This project functions by creating a wrapper around the automated deployment of multicloud infrastructure via Terraform. `testnet.py` will generate terraform scripts based on the configuration in `config.json` and the code-snippets in the snippets folder. If you want to customize the testnet for your own needs, your starting point would be to alter the configuration in the config.json file. 

### Internal structure

If you want to run a Tezos testnet, you must deploy multiple nodes and connect them as peers. Next the protocol needs to be started at one of the nodes. This results in a hierarchical structure of Terraform modules. Each cloud providers is therefore split into two modules: One 'init-node' module and one 'node' module. Both modules will create VMs at the selected cloud provider, deploy a Tezos node (in a docker container). The public IP adress of the init-node is distributed to every other nodes, enabling them all to connect to each other in a P2P manner. Therefore only one init-node of only one cloud provider should exist. The number of 'normal' nodes by other cloud providers is not limited.

### Prerequisites

To deploy a (private) Tezos testnet, you need to [install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) on your local maschine. You will aso need to setup the access to the cloud providers you want to use. You will need at least one for the testnet to function properly.

## Setting up the cloud access

### AWS

### GCP


## Using this project


## Lifecycle

### Init

### Apply

### Show

### Bake

### Destroy

### Clean

## Bugs / ToDo()
* gcp_init_node does somehow not work really when constructed via config.json
* sometimes the init-node is connected to all nodes but the nodes are only connected to the init node. Expected behaviour is that the nodes automatically connect to every other node
