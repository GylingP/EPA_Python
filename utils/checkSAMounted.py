from getPods import get_pods

def check_sa_mounted(sas):
    result = sas
    # 获取 Pods
    pods, err = get_pods()
    if err:
        print(f"[Get pods] failed: {err}")
        return result

    # 遍历 Pods 并更新 SA 数据
    for pod in pods:
        sa_key = f"{pod.namespace}/{pod.service_account}"
        if sa_key in result:
            result[sa_key].is_mounted = True
            result[sa_key].sa_pod = pod

    return result