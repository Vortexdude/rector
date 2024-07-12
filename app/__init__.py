# import ssl
# import socket
# from datetime import datetime as dt
#
# hosts = ['digitalrealty.com', 'developer.digitalrealty.com']
#
# ssl_context = ssl.create_default_context()
#
#
# def get_ssl_details(domain: str):
#     with ssl_context.wrap_socket(socket.socket(), server_hostname=domain) as s:
#         s.connect((domain, 443))
#         cert = s.getpeercert()
#         issuer = cert['issuer'][1][0][1]
#         date_format = "%b %d %H:%M:%S %Y %Z"
#         issuer_date = dt.strptime(cert['notBefore'], date_format)
#         expiration_date = dt.strptime(cert['notAfter'], date_format)
#         alt_name = cert['subjectAltName'][0][1]
#         if len(cert['subjectAltName']) == 2:
#             alt_name = cert['subjectAltName'][1][1]
#
#         data = {
#             'domain': domain,
#             'altname': alt_name,
#             'issuer': issuer,
#             'issue_date': issuer_date,
#             'expiration_date': expiration_date
#         }
#     return data
#
#
# for host in hosts:
#     data = get_ssl_details(host)
#     print(f"========= Started {data['domain']} =================\n")
#     print(f"SSL Cert will expire on {data['expiration_date'].strftime("%d-%m-%Y")}-----------")
#     print(f"=========== End {data['domain']} ====================")
