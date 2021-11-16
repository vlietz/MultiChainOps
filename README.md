# Tezos-Testnet-Multicloud

This README will describe how to deploy a Tezos test-network in a multicloud environment. 

Current supported cloud-providers are AWS and GCP.

## General overview

This project functions by creating a wrapper around the automated deployment of multicloud infrastructure via Terraform. `testnet.py` will generate terraform scripts based on the configuration in `config.json` and the code-snippets in the snippets folder. If you want to customize the testnet for your own needs, your starting point would be to alter the configuration in the config.json file. 

### Internal structure

If you want to run a Tezos testnet, you must deploy multiple nodes and connect them as peers. Next the protocol needs to be started at one of the nodes. This results in a hierarchical structure of Terraform modules. Each cloud providers is therefore split into two modules: One 'init-node' module and one 'node' module. Both modules will create VMs at the selected cloud provider, deploy a Tezos node (in a docker container). The public IP adress of the init-node is distributed to every other nodes, enabling them all to connect to each other in a P2P manner. The init-node will also start the protocol and set the chain parameters. Therefore only one init-node of only one cloud provider should exist. The number of 'normal' nodes by other cloud providers is not limited.

### Prerequisites

To deploy a (private) Tezos testnet, you need to [install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) on your local maschine. You will aso need to setup the access to the cloud providers you want to use. You will need at least one for the testnet to function properly.
Also you will need Python3 installed.

## Setting up the cloud access

### AWS

### GCP


## Using this project


## Lifecycle

`testnet.py` has multiple command-line arguments to interact with the testnet. For example

```python3 testnet.py init
python3 testnet.py apply
python3 testnet.py destroy 
```



### init

The `init` argument will generate terraform scripts based on the current configuration in config.json.

### apply

The argument `apply` will start the deployment of the current state. If the current deployment is running and no changes to the infrastrucure are made, this will not change anything. If the structure of the infrastrucure is changed, this may apply those changes. It is important to understand that this will not apply changes to the configuration of the chain. If you want those to apply, you must destroy the deployment at first and reinitialize everything. 

### show

`show` will give you informations about the current deployment like IP adresses and provider configurations.

### Bake

### Destroy

`destroy` will stop the current deployment and remove all virtual machines from the cloud providers.


### Clean

By running `clean` you can remove all generated files. 

## Bugs / ToDo()
* gcp_init_node does somehow not work really when constructed via config.json
* sometimes the init-node is connected to all nodes but the nodes are only connected to the init node. Expected behaviour is that the nodes automatically connect to every other node
* maybe find a "cleaner" way to run the baker





