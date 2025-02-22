import json
from .req import K8sRequestOption, api_request
from .structure import Rule

def getRulesFromRole(role):
    api = "/apis/rbac.authorization.k8s.io/v1"
    if "/" in role:
        # role 类型
        namespace, name = role.split("/", 1)
        api += f"/namespaces/{namespace}/roles/{name}"
    else:
        # clusterrole 类型
        name = role
        api += f"/clusterroles/{name}"

    opts = K8sRequestOption(
        api=api,
        method="GET"
    )
    resp , _  = api_request(opts)

    if resp is None:
        return None

    try:
        rules = json.loads(resp)["rules"]
    except json.JSONDecodeError:
        return None

    ruleList = []

    for rule in rules:
        newRule = Rule(
            resources=[],  
            verbs=[]   
        )

        resources = rule.get("resources", [])
        resourceNames = rule.get("resourceNames")

        for res in resources:
            if resourceNames:
                for resName in resourceNames:
                    newRule.resources.append(f"{res}({resName})")
            else:
                newRule.resources.append(res)

        verbs = rule.get("verbs", [])
        for verb in verbs:
            newRule.verbs.append(verb)
        ruleList.append(newRule)

    return ruleList
