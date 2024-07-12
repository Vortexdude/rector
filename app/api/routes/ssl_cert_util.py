from fastapi import APIRouter
import ssl
import socket
from datetime import datetime as dt
router = APIRouter()
ssl_context = ssl.create_default_context()


@router.get("/ssl_cert")
def get_ssl_cert_details(domain: str):
    return get_ssl_details(domain)


def get_ssl_details(domain: str):
    with ssl_context.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.connect((domain, 443))
        cert = s.getpeercert()
        issuer = cert['issuer'][1][0][1]
        date_format = "%b %d %H:%M:%S %Y %Z"
        issuer_date = dt.strptime(cert['notBefore'], date_format)
        expiration_date = dt.strptime(cert['notAfter'], date_format)
        alt_name = cert['subjectAltName'][0][1]
        if len(cert['subjectAltName']) == 2:
            alt_name = cert['subjectAltName'][1][1]

    return {
            'domain': domain,
            'altname': alt_name,
            'issuer': issuer,
            'issue_date': issuer_date.strftime("%d-%m-%Y"),
            'expiration_date': expiration_date.strftime("%d-%m-%Y")
        }
