from conf.conf import load_config
from utils import get_sa_binding,check_sa_mounted,get_critical_sa
import json
import os

print("reading conf.yaml")
conf = load_config()
print("scannning")

sa_binding_map = {}
critical_sas = []

if len(sa_binding_map) == 0:
    sa_binding_map = get_sa_binding()

if len(critical_sas) == 0:
    critical_sas = get_critical_sa(check_sa_mounted(sa_binding_map), json.loads(os.environ.get("SSH_CONFIG")).get("nodeName",""))

print()  # Print an empty line

for critical_sa in critical_sas:
    if not critical_sa.sa0.is_mounted:
        continue
    
    print(f"[app]: {critical_sa.sa0.sa_pod.namespace}")
    print(f"[component]: {critical_sa.sa0.sa_pod.name}")
    print(f"[SA]: {critical_sa.sa0.name}")
    print(f"[permission]: {critical_sa.type}")
    print(f"[node]: {critical_sa.sa0.sa_pod.node_name}")
    print(f"[roles/clusterRoles]: {critical_sa.roles}")
    print(f"[roleBindings]: {critical_sa.sa0.role_bindings}")
    print("-------------------------------------------")
    print()  # Print an empty line
