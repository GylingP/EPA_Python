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
        opts.server = os.getenv('API_SERVER')  # Assuming conf.ApiServer is set as an environment variable

    opts.method = opts.method.upper()
    url = f"https://{opts.server}{opts.api}"
    headers = opts.header

    # Prepare the request body (if it's a POST request)
    data = opts.post_data.encode('utf-8') if opts.method == "POST" else None

    # Setup the session
    session = requests.Session()
    
    # Priority: opts.token => token file => cert file
    token = opts.token or ""
    token_file = os.getenv('TOKEN_FILE')
    if not token and token_file:
        with open(token_file, 'r') as file:
            token = file.read().strip()

    cert = None
    if not token:
        if not opts.cert:
            opts.cert = os.getenv('ADMIN_CERT')  # Assuming conf.AdminCert is set as an environment variable
        if not opts.key:
            opts.key = os.getenv('ADMIN_CERT_KEY')  # Assuming conf.AdminCertKey is set as an environment variable
        cert = (opts.cert, opts.key) if opts.cert and opts.key else None

    # Setup proxy if configured
    proxy_address = os.getenv('PROXY_ADDRESS')  # Assuming conf.ProxyAddress is set as an environment variable
    if proxy_address:
        proxies = {"https": proxy_address}
        session.proxies.update(proxies)

    # Set Authorization header
    if token:
        headers['Authorization'] = f"Bearer {token}"

    # Verify SSL/TLS certificate and skip verification if needed
    verify = os.getenv('VERIFY_SSL', 'false').lower() == 'true'
    if not verify:
        session.verify = False

    # Perform the HTTP request
    try:
        if opts.method == "POST":
            response = session.post(url, headers=headers, data=data, cert=cert, verify=verify)
        elif opts.method == "GET":
            response = session.get(url, headers=headers, cert=cert, verify=verify)
        else:
            return "", f"Unsupported method {opts.method}"

        # Check for HTTP errors
        response.raise_for_status()

        return response.text, None

    except requests.exceptions.RequestException as err:
        return "", str(err)

# opts = K8sRequestOption(
#     token="",  # Leave empty if you want to load it from the token file
#     cert="",   # Leave empty if you want to use the default cert
#     key="",    # Leave empty if you want to use the default key
#     server="jsonplaceholder.typicode.com",  # Replace with your actual server address
#     api="/posts",  # Replace with your actual API endpoint
#     method="GET",  # You can use GET, POST, etc.
#     post_data="",  # Include POST data if needed
#     header={"Content-Type": "application/json"}  # Set appropriate headers
# )

# # Call the function
# response, error = api_request(opts)

# if error:
#     print(f"Error: {error}")
# else:
#     print(f"Response: {response}")