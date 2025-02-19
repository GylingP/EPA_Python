from .getPods import get_pods

def check_sa_mounted(sas):
    result = sas
    pods, err = get_pods()
    if err:
        print(f"[Get pods] failed: {err}")
        return result

    for pod in pods:
        sa_key = f"{pod.namespace}/{pod.service_account}"
        if sa_key in result:
            result[sa_key].is_mounted = True
            result[sa_key].sa_pod = pod

    return result