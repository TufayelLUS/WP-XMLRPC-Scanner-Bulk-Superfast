import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from threading import RLock

threads = 100 # set thread count here
lock = RLock()

def isXMLRPCEnabled(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    parsed = urlparse(url)
    url = f"{parsed.scheme}://{parsed.netloc}"
    headers = {
        'Content-Type': 'text/xml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    }
    # make a test call to see if XMLRPC is enabled
    data = "<methodCall></methodCall>"
    try:
        r = requests.post(url + "/xmlrpc.php", data=data,
                          headers=headers, timeout=10)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def handleWithThread(domain):
    domain = domain.strip()
    if not domain:
        return
    if isXMLRPCEnabled(domain):
        print(f"XMLRPC is enabled on {domain}")
        lock.acquire()
        with open("xmlrpc_domains.txt", "a") as f:
            f.write(domain + "\n")
        lock.release()
    else:
        print(f"XMLRPC is not enabled on {domain}")
        lock.acquire()
        with open("no_xmlrpc_domains.txt", "a") as f:
            f.write(domain + "\n")
        lock.release()


if __name__ == "__main__":
    domains = open("domains.txt", mode="r",
                   encoding="utf-8").read().splitlines()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(handleWithThread, domains)
