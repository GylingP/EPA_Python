from collections import defaultdict
from .getBinding import getClusterRoleBindings, getRolesBindings
from .getRulesFromBinding import getRulesFromRole
from .structure import SA

def get_sa_binding():
    SaBindingMap = defaultdict(lambda: defaultdict(list))
    result = {}

    clusterrolebindingList = getClusterRoleBindings()
    rolebindingList = getRolesBindings()

    for clusterrolebinding in clusterrolebindingList:
        rules = getRulesFromRole(clusterrolebinding.role_ref)
        for sa in clusterrolebinding.subject:
            if sa not in SaBindingMap:
                SaBindingMap[sa] = defaultdict(list)
            if sa not in result:
                result[sa] = SA(
                    name=sa,
                    role_bindings=[],
                    roles={},
                )
            result[sa].role_bindings.append(clusterrolebinding.name)
            for rule in rules:
                for res in rule.resources:
                    if clusterrolebinding.role_ref not in result[sa].roles:
                        result[sa].roles[clusterrolebinding.role_ref] = defaultdict(list)
                    for verb in rule.verbs:
                        result[sa].roles[clusterrolebinding.role_ref][res].append(verb)
                        SaBindingMap[sa][res].append(verb)
            result[sa].permission = dict(SaBindingMap[sa])

    for rolebinding in rolebindingList:
        rules = getRulesFromRole(rolebinding.role_ref)
        for sa in rolebinding.subject:
            if sa not in SaBindingMap:
                SaBindingMap[sa] = defaultdict(list)
            if sa not in result:
                result[sa] = SA(
                    name=sa,
                    role_bindings=[],
                    roles={},
                )
            result[sa].role_bindings.append(rolebinding.name)
            for rule in rules:
                for res in rule.resources:
                    res = f"{res}[{rolebinding.namespace}]" 
                    if rolebinding.role_ref not in result[sa].roles:
                        result[sa].roles[rolebinding.role_ref] = defaultdict(list)
                    for verb in rule.verbs:
                        result[sa].roles[rolebinding.role_ref][res].append(verb)
                        SaBindingMap[sa][res].append(verb)
            result[sa].permission = dict(SaBindingMap[sa])

    return result
