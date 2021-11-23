import json
import subprocess
import argparse
import random
import string
import os

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str


def write_params(params):
    with open('./terraform/params.json', 'w+') as outfile:
        json.dump(params, outfile)

def write_testnet(params):
    with open('./terraform/testnet', 'w+') as outfile:
        json.dump(params, outfile)

def main_replace(print_string, nodes, access):
    print_string = print_string.replace("$gcp_node_count", str(nodes["gcp_node_count"]))
    print_string = print_string.replace("$aws_node_count", str(nodes["aws_node_count"]))
    print_string = print_string.replace("$credentials_file_path", access["gcp"]["credentials_file_path"])
    print_string = print_string.replace("$ssh_file_path", access["gcp"]["ssh_file_path"])
    print_string = print_string.replace("$ssh_user", access["gcp"]["ssh_user"])
    print_string = print_string.replace("$private_key_path", access["aws"]["private_key_path"])
    print_string = print_string.replace("$access_key", access["aws"]["access_key"])
    print_string = print_string.replace("$secret_key", access["aws"]["secret_key"])
    print_string = print_string.replace("$aws_key_name", access["aws"]["aws_key_name"])
    return print_string

def generate_main(nodes, access):
    print_string = ""
    initfile = ""


    with open ("./snippets/nodes", "r") as myfile:
        nodes_file =  myfile.read()

    if nodes["init_node"] == "aws":
        initfile = "./snippets/aws_init"

    if nodes["init_node"] == "gcp":
        initfile = "./snippets/gcp_init"
    
    with open (initfile, "r") as myfile:
        print_string = print_string + myfile.read()

    print_string = print_string + nodes_file

    print_string = main_replace(print_string, nodes, access)
    with open('./terraform/main.tf', 'w+') as outfile:
        outfile.write(print_string)





def terraform_bake():
    with open('./terraform/main.tf', "a+") as myfile:
        # if 'baker' not in myfile.read():
            with open('./snippets/baker') as baker_snippet:
                
                myfile.write(baker_snippet.read().replace("$random_hash", get_random_string(8)))
    terraform_deploy()

def terraform_config():

    with open('config.json') as json_file:
        config = json.load(json_file)
        
        config["params"]["bootstrap_accounts"] = [["key1", "4000000000000"]]

        write_params(config["params"])

        write_testnet(config["chain"])

        generate_main(config["nodes"], config["access"])



def terraform_clean():
    os.remove("./terraform/testnet")
    os.remove("./terraform/main.tf")
    os.remove("./terraform/params.json")

def terraform_show():
    p = subprocess.Popen(["cd terraform; terraform init; terraform show"], stdout=subprocess.PIPE, shell=True)

    for line in iter(p.stdout.readline, b''):
        print (line.decode('UTF-8').replace("\n", "")),
    p.stdout.close()
    p.wait()

def terraform_deploy():
    p = subprocess.Popen(["cd terraform; terraform init; terraform apply --auto-approve -lock=false"], stdout=subprocess.PIPE, shell=True)

    for line in iter(p.stdout.readline, b''):
        print (line.decode('UTF-8').replace("\n", "")),
    p.stdout.close()
    p.wait()

def terraform_fa2():
    with open('./terraform/main.tf', "a+") as myfile:
    # if 'baker' not in myfile.read():
        with open('./snippets/fa2') as baker_snippet:
            
            myfile.write(baker_snippet.read().replace("$random_hash", get_random_string(8)))
    terraform_deploy()

def terraform_contract():

    #terraform_config()

    with open('contract.json') as json_file:
        contract = json.load(json_file)
    with open('config.json') as config_json:
        config = json.load(config_json)


    with open('./terraform/main.tf', "a+") as myfile:
    # if 'baker' not in myfile.read():
        with open('./snippets/contract') as baker_snippet:
            userstr = ""
            for user in contract["user"]:
                userstr = userstr + "\"sudo docker exec node tezos-client import secret key " + user[0] + " " + user[1] + " --force\",\n      "
            
            print_string = baker_snippet.read()

            print_string = print_string.replace("$user", userstr)
            print_string = print_string.replace("$name", contract["contract"]["name"])
            print_string = print_string.replace("$init", contract["contract"]["init"])
            print_string = print_string.replace("$path", contract["contract"]["path"])
            print_string = print_string.replace("$transfer", contract["contract"]["transfer"])
            print_string = print_string.replace("$burn-cap", contract["contract"]["burn-cap"])


            print_string = main_replace(print_string, config["nodes"], config["access"])
            
            myfile.write(print_string.replace("$random_hash", get_random_string(8)))
    terraform_deploy()


def terraform_destroy():
    p = subprocess.Popen(["cd terraform; terraform destroy --auto-approve"], stdout=subprocess.PIPE, shell=True)

    for line in iter(p.stdout.readline, b''):
        print (line.decode('UTF-8').replace("\n", "")),
    p.stdout.close()
    p.wait()

def terraform_state_show():
    print("")

parser = argparse.ArgumentParser()
sp = parser.add_subparsers(dest='cmd')
for cmd in ['destroy', 'apply', 'show', 'init', 'bake', 'clean', 'contract']:
    sp.add_parser(cmd)
# for cmd in ['contract', 'MOVEREL']:
#     spp = sp.add_parser(cmd)
    # spp.add_argument('x', type=ascii)
    # spp.add_argument('y', type=float)
parser.print_help()
args = parser.parse_args()

print("Input: " +  args.cmd)

if args.cmd == "destroy":
    terraform_destroy()

if args.cmd == "apply":
    terraform_config()
    terraform_deploy()

if args.cmd == "init":
    terraform_config()

if args.cmd == "show":
    terraform_show()

if args.cmd == "bake":
    terraform_bake()

if args.cmd == "clean":
    terraform_clean()

if args.cmd == "contract":
    terraform_contract()






