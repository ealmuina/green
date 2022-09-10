import os

import ipinfo
from ipware import get_client_ip


def get_timezone(request):
    print(request.META)

    client_ip, is_routable = get_client_ip(request)
    ipinfo_token = os.environ.get('IPINFO_TOKEN')

    if all((client_ip, is_routable, ipinfo_token)):
        handler = ipinfo.getHandler(ipinfo_token)
        details = handler.getDetails(client_ip)
        return details.timezone

    return 'UTC'
