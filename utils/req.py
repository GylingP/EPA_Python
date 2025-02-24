import requests
import os

class K8sRequestOption:
    def __init__(self, token="", cert="", key="", server="", api="", method="GET", post_data="", header=None):
        self.token = token
        self.cert = cert
        self.key = key
        self.server = server
        self.api = api
        self.method = method
        self.post_data = post_data
        self.header = header or {}

def api_request(opts: K8sRequestOption):
    if not opts.server:
        opts.server = os.getenv('API_SERVER')  

    opts.method = opts.method.upper()
    url = f"https://{opts.server}{opts.api}"
    headers = opts.header

    data = opts.post_data.encode('utf-8') if opts.method == "POST" else None

    session = requests.Session()
    
    token = opts.token or ""
    token_file = os.getenv('TOKEN_FILE')
    if not token and token_file:
        with open(token_file, 'r') as file:
            token = file.read().strip()

    cert = None
    if not token:
        if not opts.cert:
            opts.cert = os.getenv('ADMIN_CERT')  
        if not opts.key:
            opts.key = os.getenv('ADMIN_CERT_KEY') 
        cert = (opts.cert, opts.key) if opts.cert and opts.key else None

    proxy_address = os.getenv('PROXY_ADDRESS')  
    if proxy_address:
        proxies = {"https": proxy_address}
        session.proxies.update(proxies)

    if token:
        headers['Authorization'] = f"Bearer {token}"

    verify = os.getenv('VERIFY_SSL', 'false').lower() == 'true'
    if not verify:
        session.verify = False

    requests.packages.urllib3.disable_warnings()

    try:
        if opts.method == "POST":
            response = session.post(url, headers=headers, data=data, cert=cert, verify=verify)
        elif opts.method == "GET":
            response = session.get(url, headers=headers, cert=cert, verify=verify)
        else:
            return "", f"Unsupported method {opts.method}"

        response.raise_for_status()

        return response.text, None

    except requests.exceptions.RequestException as err:
        return "", str(err)
