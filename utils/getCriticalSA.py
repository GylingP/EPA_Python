from .structure import CriticalSA

def get_critical_sa(SAs, controlled_node):
    result = []
    for sa_key, sa in SAs.items():
        clusterrolebind_flag_1 = 0
        clusterrolebind_flag_2 = 0
        rolebind_flag_1 = 0
        rolebind_flag_2 = 0
        clusterroleescalate_flag = 0
        roleescalate_flag = 0

        critical_sa = CriticalSA(
            in_node=False,
            type=[],
            level="namespace",
            sa0=sa,
        )
        
        for role_name, role in sa.roles.items():
            critical_sa.roles.append(role_name)
            
            for k, v in role.items():
                if sa.sa_pod and sa.sa_pod.node_name== controlled_node:
                    critical_sa.in_node = True

                raw_type = ""
                
                if 'get' in v or '*' in v:
                    if 'secrets' in k or '*' in k:
                        raw_type = "getsecrets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                
                if 'watch' in v or '*' in v:
                    if 'secrets' in k or '*' in k:
                        raw_type = "watchsecrets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

                if 'patch' in v or '*' in v:
                    if k == "nodes" or k == "*":
                        critical_sa.type.append("patchnodes")
                    if 'clusterroles' in k or '*' in k:
                        clusterroleescalate_flag += 1
                        if clusterroleescalate_flag == 2:
                            critical_sa.type.append("patchclusterroles")
                    if 'roles' in k or '*' in k:
                        roleescalate_flag += 1
                        if roleescalate_flag == 2:
                            raw_type = "patchroles"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'clusterrolebindings' in k or '*' in k:
                        clusterrolebind_flag_2 += 1
                        if clusterrolebind_flag_2 == 2:
                            critical_sa.type.append("patchclusterrolebindings")
                    if 'rolebindings' in k or '*' in k:
                        rolebind_flag_2 += 1
                        if rolebind_flag_2 == 2:
                            raw_type = "patchrolebindings"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'pods' in k or '*' in k:
                        raw_type = "patchpods"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'daemonsets' in k or '*' in k:
                        raw_type = "patchdaemonsets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'deployments' in k or '*' in k:
                        raw_type = "patchdeployments"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'statefulsets' in k or '*' in k:
                        raw_type = "patchstatefulsets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'replicasets' in k or '*' in k:
                        raw_type = "patchreplicasets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'cronjobs' in k or '*' in k:
                        raw_type = "patchcronjobs"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    elif 'jobs' in k or '*' in k:
                        raw_type = "patchjobs"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'replicationcontrollers' in k or '*' in k:
                        raw_type = "patchreplicationcontrollers"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'mutatingwebhookconfigurations' in k or k == "*":
                        critical_sa.type.append("patchmutatingwebhookconfigurations")
                    if 'validatingwebhookconfigurations' in k or k == "*":
                        critical_sa.type.append("patchvalidatingwebhookconfigurations")

                if 'create' in v or '*' in v:
                    if 'secrets' in k or '*' in k:
                        raw_type = "createsecrets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'clusterrolebindings' in k or '*' in k:
                        clusterrolebind_flag_1 += 1
                        if clusterrolebind_flag_1 == 2:
                            critical_sa.type.append("createclusterrolebindings")
                    if 'rolebindings' in k or '*' in k:
                        rolebind_flag_1 += 1
                        if rolebind_flag_1 == 2:
                            raw_type = "createrolebindings"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'serviceaccounts/token' in k or '*' in k:
                        raw_type = "createtokens"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'pods' in k or '*' in k:
                        raw_type = "createpods"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'pods/exec' in k or '*' in k:
                        raw_type = "execpods"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'pods/ephemeralcontainers' in k or '*' in k:
                        raw_type = "execpods2"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'daemonsets' in k or '*' in k:
                        raw_type = "createdaemonsets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'deployments' in k or '*' in k:
                        raw_type = "createdeployments"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'statefulsets' in k or '*' in k:
                        raw_type = "createstatefulsets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'replicasets' in k or '*' in k:
                        raw_type = "createreplicasets"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'cronjobs' in k or '*' in k:
                        raw_type = "createcronjobs"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    elif 'jobs' in k or '*' in k:
                        raw_type = "createjobs"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'replicationcontrollers' in k or '*' in k:
                        raw_type = "createreplicationcontrollers"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                    if 'mutatingwebhookconfigurations' in k or '*' in k:
                        critical_sa.type.append("createmutatingwebhookconfigurations")
                    if 'validatingwebhookconfigurations' in k or '*' in k:
                        critical_sa.type.append("createvalidatingwebhookconfigurations")
                    if 'nodes' in k or '*' in k:
                        critical_sa.type.append("createnodes")

                if 'bind' in v or '*' in v:
                    if 'clusterroles' in k or '*' in k:
                        clusterrolebind_flag_1 += 1
                        clusterrolebind_flag_2 += 1
                        if clusterrolebind_flag_1 == 2:
                            critical_sa.type.append("createclusterrolebindings")
                        if clusterrolebind_flag_2 == 2:
                            critical_sa.type.append("patchclusterrolebindings")
                    if 'roles' in k or '*' in k:
                        rolebind_flag_1 += 1
                        rolebind_flag_2 += 1
                        if rolebind_flag_1 == 2:
                            raw_type = "createrolebindings"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))
                        if rolebind_flag_2 == 2:
                            raw_type = "patchrolebindings"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

                if 'delete' in v or '*' in v:
                    if 'pods' in k or '*' in k:
                        raw_type = "deletepods"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

                    if 'nodes' in k or '*' in k:
                        raw_type = "deletenodes"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

                    if 'validatingwebhookconfigurations' in k or '*' in k:
                        raw_type = "deletevalidatingwebhookconfigurations"
                        critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

                if 'escalate' in v or '*' in v:
                    if 'clusterroles' in k or '*' in k:
                        clusterroleescalate_flag += 1
                        if clusterroleescalate_flag == 2:
                            critical_sa.type.append("escalateclusterroles")
                    if 'roles' in k or '*' in k:
                        roleescalate_flag += 1
                        if roleescalate_flag == 2:
                            raw_type = "escalateroles"
                            critical_sa.type.append(check_restrict(k, raw_type, critical_sa))

        result.append(critical_sa)

    return result


def check_restrict(k, rawType, criticalSA):
    result = rawType
    if "(" in k:
        result = rawType + k[k.index("("):]
    elif "[" in k:
        result = rawType + k[k.index("["):]

    else:
        criticalSA.level = "cluster"

    if "(" in k:
        criticalSA.resource_name = k[k.index("(")+1:k.index(")")]
    if "[" in k:
        criticalSA.namespace = k[k.index("[")+1:k.index("]")]
        
    return result
