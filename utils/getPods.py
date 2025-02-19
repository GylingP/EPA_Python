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

        # 假设返回的响应是 JSON 格式
        pods_data = json.loads(resp)
        pods = pods_data.get("items", [])
        pod_list = []

        for pod in pods:
            # 创建 Pod 实例
            print(pod["spec"])
            new_pod = Pod(
                namespace=pod["metadata"]["namespace"],
                name=pod["metadata"]["name"],
                uid=pod["metadata"]["uid"],
                node_name=pod["spec"]["nodeName"],
                service_account=pod["spec"].get("serviceAccountName", ""),
                controll_by=[]
            )

            # 检查 automountServiceAccountToken 字段
            token_mounted = pod["spec"].get("automountServiceAccountToken", True)
            new_pod.token_mounted = token_mounted

            # 如果 ownerReferences 存在，添加控制者类型
            if "ownerReferences" in pod["metadata"]:
                for owner in pod["metadata"]["ownerReferences"]:
                    new_pod.controll_by.append(owner["kind"])

            # 将 Pod 添加到 pod_list
            pod_list.append(new_pod)

        return pod_list, None  # 返回 Pod 列表和错误（此处无错误）
    except Exception as e:
        return None, str(e)  # 出现错误时返回错误信息
