import httpagentparser
from fastapi import Request


def extract_user_info(request: Request) -> tuple[str, str, str]:
    user_agent = request.headers.get('user-agent')
    _user_agent = httpagentparser.detect(user_agent)
    os = _user_agent['os']['name']
    device = _user_agent['platform']['name']
    browser = _user_agent['browser']['name']
    return os, device, browser
