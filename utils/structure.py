class Pod:
    def __init__(self, namespace, name, uid, node_name, service_account, controll_by, token_mounted=False):
        self.namespace = namespace
        self.name = name
        self.uid = uid
        self.node_name = node_name
        self.service_account = service_account  # SaName
        self.controll_by = controll_by  # type
        self.token_mounted = token_mounted


class SA:
    def __init__(self, name, is_mounted=False, sa_pod=None, permission=None, roles=None, role_bindings=None):
        self.is_mounted = is_mounted
        self.name = name  # The full name: namespace/name
        self.sa_pod = sa_pod  # Pod instance
        self.permission = permission if permission else {}
        self.roles = roles if roles else {}
        self.role_bindings = role_bindings if role_bindings else []


class CriticalSA:
    def __init__(self, in_node, type, level, sa0, namespace='', resource_name='', roles=[]):
        self.in_node = in_node  # Whether the corresponding Pod is in node1
        self.type = type  # The type of the high permissions
        self.level = level  # cluster, namespace
        self.sa0 = sa0  # SA instance
        self.namespace = namespace
        self.resource_name = resource_name
        self.roles = roles


class CriticalSAWrapper:
    def __init__(self, crisa, type_):
        self.crisa = crisa  # CriticalSA instance
        self.type = type_


class RoleBinding:
    def __init__(self, namespace, name, role_ref, subject):
        self.namespace = namespace
        self.name = name
        self.role_ref = role_ref
        self.subject = subject


class Rule:
    def __init__(self, resources=None, verbs=None):
        self.resources = resources if resources else []
        self.verbs = verbs if verbs else []


class Role:
    def __init__(self, namespace, name, rules):
        self.namespace = namespace
        self.name = name
        self.rules = rules  # Rule instance


class SAtoken:
    def __init__(self, sa_name, permission_type, token):
        self.sa_name = sa_name
        self.permission_type = permission_type
        self.token = token


class CriticalSASet:
    def __init__(self, token_set=None):
        self.token_set = token_set if token_set else []


class SSHConfig:
    def __init__(self, ip, port, username, password, private_key_file, nodename):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.private_key_file = private_key_file
        self.nodename = nodename
