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


def generate_main(params, access):
    print_string = ""
    initfile = ""
    with open ("./snippets/nodes", "r") as myfile:
        nodes =  myfile.read()

    if params["init_node"] == "aws":
        initfile = "./snippets/aws_init"

    if params["init_node"] == "gcp":
        initfile = "./snippets/gcp_init"
    
    with open (initfile, "r") as myfile:
        print_string = print_string + myfile.read()

    print_string = print_string + nodes

    print_string = print_string.replace("$gcp_node_count", str(params["gcp_node_count"]))
    print_string = print_string.replace("$aws_node_count", str(params["aws_node_count"]))
    print_string = print_string.replace("$credentials_file_path", access["gcp"]["credentials_file_path"])
    print_string = print_string.replace("$ssh_file_path", access["gcp"]["ssh_file_path"])
    print_string = print_string.replace("$ssh_user", access["gcp"]["ssh_user"])
    print_string = print_string.replace("$private_key_path", access["aws"]["private_key_path"])
    print_string = print_string.replace("$access_key", access["aws"]["access_key"])
    print_string = print_string.replace("$secret_key", access["aws"]["secret_key"])
    print_string = print_string.replace("$aws_key_name", access["aws"]["aws_key_name"])
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
        data = json.load(json_file)
        
        data["params"]["bootstrap_accounts"] = [["key1", "4000000000000"]]

        write_params(data["params"])

        write_testnet(data["chain"])



        generate_main(data["nodes"], data["access"])



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
    p = subprocess.Popen(["cd terraform; terraform init; terraform apply --auto-approve"], stdout=subprocess.PIPE, shell=True)

    for line in iter(p.stdout.readline, b''):
        print (line.decode('UTF-8').replace("\n", "")),
    p.stdout.close()
    p.wait()


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
for cmd in ['destroy', 'apply', 'show', 'init', 'bake', 'clean']:
    sp.add_parser(cmd)
# for cmd in ['MOVEABS', 'MOVEREL']:
#     spp = sp.add_parser(cmd)
#     spp.add_argument('x', type=float)
#     spp.add_argument('y', type=float)
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


exit()



#kommandos einfügen für destroy/deploy/view(aktive config anzeigen)/status holen/
#ggf einige interessante informationen parsen, zB IPs

#bake hinzufügen
#baking in python script (threading)
#baking ins deployment unabhängig vom python script
p = subprocess.Popen(["cd terraform; terraform init; terraform apply --auto-approve"], stdout=subprocess.PIPE, shell=True)

for line in iter(p.stdout.readline, b''):
    print (line.decode('UTF-8')),
p.stdout.close()
p.wait()


