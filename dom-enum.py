import requests
from urllib.parse import urlparse
import socket
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError
import dns.resolver
import sys

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/121.0.2277.128'

def get_response_code(url, timeout=5):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=timeout, allow_redirects=True, verify=True, headers=headers)
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

def get_ip_info(domain):
    try:
        ip_address = socket.gethostbyname(domain)

        # Retrieve ASN information
        ipwhois = IPWhois(ip_address)
        result = ipwhois.lookup_rdap()
        asn = 'N/A' if ip_address.startswith(('10.', '172.', '192.168')) else result.get('asn', 'N/A')
        asn_name = result.get('asn_description', 'N/A')

        # Retrieve MX records
        mx_records = []
        try:
            mx_answers = dns.resolver.resolve(domain, 'MX')
            mx_records = [str(record.exchange) for record in mx_answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.exception.DNSException):
            pass  # Handle the case where the domain has no MX records or DNS resolution fails

        return ip_address, asn, asn_name, mx_records
    except socket.error as e:
        return f"Error: {e}", 'N/A', 'N/A', []
    except IPDefinedError:
        return ip_address, 'N/A', 'N/A', []

def extract_domain_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def enumerate_domains(file_path):
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()

    for domain in domains:
        http_url = f"http://{domain}"
        https_url = f"https://{domain}"

        response_code_http = get_response_code(http_url)
        response_code_https = get_response_code(https_url)

        cleaned_domain = extract_domain_from_url(http_url)
        ip_address, asn, asn_name, mx_records = get_ip_info(cleaned_domain)

        mx_status = "YES" if mx_records else "NO"
        print(f"{cleaned_domain}|{ip_address}|{asn}|{asn_name}|{response_code_http}|{response_code_https}|{mx_status}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    enumerate_domains(file_path)
