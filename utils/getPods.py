from .req import K8sRequestOption,api_request
from .structure import Pod
import json

def get_pods():

    opts = K8sRequestOption(
        api="/api/v1/pods",
        method="GET"
    )

    try:
        resp , _ = api_request(opts)
        if resp is None:
            raise ValueError("API request failed")

        pods_data = json.loads(resp)
        pods = pods_data.get("items", [])
        pod_list = []

        for pod in pods:
            new_pod = Pod(
                namespace=pod["metadata"]["namespace"],
                name=pod["metadata"]["name"],
                uid=pod["metadata"]["uid"],
                node_name=pod["spec"].get("nodeName", "None"),
                service_account=pod["spec"].get("serviceAccountName", ""),
                controll_by=[]
            )

            token_mounted = pod["spec"].get("automountServiceAccountToken", True)
            new_pod.token_mounted = token_mounted

            if "ownerReferences" in pod["metadata"]:
                for owner in pod["metadata"]["ownerReferences"]:
                    new_pod.controll_by.append(owner["kind"])

            pod_list.append(new_pod)

        return pod_list, None  
    except Exception as e:
        return None, str(e) 
