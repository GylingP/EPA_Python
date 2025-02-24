import json
from .req import K8sRequestOption, api_request
from .structure import RoleBinding

def getClusterRoleBindings():
    opts = K8sRequestOption(
        api="/apis/rbac.authorization.k8s.io/v1/clusterrolebindings",
        method="GET"
    )
    resp , _ = api_request(opts)

    if resp is None:
        return None

    try:
        clusterRoleBindings = json.loads(resp)["items"]
    except json.JSONDecodeError:
        return None

    clusterRoleBindingList = []

    for clusterRoleBinding in clusterRoleBindings:
        newClusterRoleBinding = RoleBinding(
            namespace="",
            name=clusterRoleBinding["metadata"]["name"],
            role_ref=clusterRoleBinding["roleRef"]["name"],
            subject=[]
        )

        if "subjects" in clusterRoleBinding:
            for sa in clusterRoleBinding["subjects"]:
                if sa["kind"] != "ServiceAccount":
                    continue
                newClusterRoleBinding.subject.append(f"{sa['namespace']}/{sa['name']}")

        clusterRoleBindingList.append(newClusterRoleBinding)

    return clusterRoleBindingList

def getRolesBindings():
    opts = K8sRequestOption(
        api="/apis/rbac.authorization.k8s.io/v1/rolebindings",
        method="GET"
    )
    resp , _ = api_request(opts)
    
    if resp is None:
        return None

    try:
        roleBindings = json.loads(resp)["items"]
    except json.JSONDecodeError:
        return None

    roleBindingList = []

    for roleBinding in roleBindings:
        newRoleBinding = RoleBinding(
            namespace=roleBinding["metadata"]["namespace"],
            name=roleBinding["metadata"]["name"],
            role_ref="",
            subject=[]
        )

        roleKind = roleBinding["roleRef"]["kind"]
        if roleKind == "Role":
            newRoleBinding.role_ref = newRoleBinding.namespace + "/"
        newRoleBinding.role_ref += roleBinding["roleRef"]["name"]

        if "subjects" in roleBinding:
            for sa in roleBinding["subjects"]:
                if sa["kind"] != "ServiceAccount":
                    continue
                newRoleBinding.subject.append(f"{sa.get('namespace','')}/{sa.get('name','')}")

        roleBindingList.append(newRoleBinding)

    return roleBindingList