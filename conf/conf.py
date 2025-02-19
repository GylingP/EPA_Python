import os
import yaml

def load_config():
    with open("./conf/conf.yaml", 'r') as f:
        config = yaml.safe_load(f)

        os.environ['API_SERVER'] = config.get('apiServer', '')
        os.environ['PROXY_ADDRESS'] = config.get('proxyAddress', '')

        os.environ['TOKEN_FILE'] = config.get('auth', {})[0].get('tokenFile', '')
        os.environ['KUBE_CONFIG'] = config.get('auth', {})[1].get('kubeconfig', '')
        os.environ['ADMIN_CERT'] = config.get('auth', {})[2].get('crt', '')
        os.environ['ADMIN_CERT_KEY'] = config.get('auth', {})[2].get('key', '')

        ssh_config = config.get('ssh', {})[0]
        if ssh_config:
            os.environ['SSH_CONFIG'] = str(ssh_config).replace("'", "\"")  
        else:
            print("Error loading SSH config")
