import httpagentparser
from fastapi import Request
import psycopg2


def extract_user_info(request: Request) -> tuple[str, str, str]:
    user_agent = request.headers.get('user-agent')
    _user_agent = httpagentparser.detect(user_agent)
    os = _user_agent['os']['name']
    device = _user_agent['platform']['name']
    browser = _user_agent['browser']['name']
    return os, device, browser


def check_db_connection(db: str, user: str, host: str, password: str) -> bool:
    try:
        conn = psycopg2.connect(f"dbname='{db}' user='{user}' host='{host}' password='{password}' connect_timeout=1 ")
        conn.close()
        return True
    except:
        return False
