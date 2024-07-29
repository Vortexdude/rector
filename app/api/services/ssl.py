import socket
import ssl
import requests
from datetime import datetime as dt
from app.common.utils.validator import URLUtil
from app.core.config import logger


class SSLExtractor:

    @staticmethod
    def _get_ssl(url: str):
        ssl_context = ssl.create_default_context()
        with ssl_context.wrap_socket(socket.socket(), server_hostname=url) as s:
            s.connect((url, 443))
            cert = s.getpeercert()
            issuer = cert['issuer'][1][0][1]
            date_format = "%b %d %H:%M:%S %Y %Z"
            issuer_date = dt.strptime(cert['notBefore'], date_format)
            expiration_date = dt.strptime(cert['notAfter'], date_format)
            alt_name = cert['subjectAltName'][0][1]
            if len(cert['subjectAltName']) == 2:
                alt_name = cert['subjectAltName'][1][1]

        return {
            'domain': url,
            'altname': alt_name,
            'issuer': issuer,
            'issue_date': issuer_date.strftime("%d-%m-%Y"),
            'expiration_date': expiration_date.strftime("%d-%m-%Y")
        }

    @classmethod
    def get_detail(cls, domain: str):
        details = {}

        try:
            url = URLUtil.validate_url(domain)
            response = requests.get(URLUtil.request_formatter(domain))
            return cls._get_ssl(url)

        except requests.exceptions.Timeout:
            details = {"status": 1, "message": "Timeout issue"}

        except requests.exceptions.TooManyRedirects:
            details = {"status": 1, "message": "Too many redirection"}

        except requests.exceptions.RequestException:
            details = {"status": 1, "message": "Error in the request."}

        except ValueError:
            details = {"status": 1, "message": "Invalid URI"}

        finally:
            if 'status' in details and details['status'] == 1:
                logger.error(details['message'])
