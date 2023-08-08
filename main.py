
# This doesnt print CSRF Token, only cookie cuz most of people dont know what to do and they keep only Cookie so thats it lol its almost the same lol. 
import httpx,re
from datetime import datetime

ROBLOX_HOME_URL = "https://www.roblox.com/home"
AUTH_API_URL = "https://auth.roblox.com/v1/authentication-ticket"
REDEEM_API_URL = "https://auth.roblox.com/v1/authentication-ticket/redeem"

def get_csrf_token(auth_cookie):
    response = httpx.get(ROBLOX_HOME_URL, cookies={".ROBLOSECURITY": auth_cookie})
    csrf_token = re.search(r'<meta name="csrf-token" data-token="(.*?)"', response.text).group(1)
    return csrf_token

def generate_request_headers(csrf_token, auth_cookie):
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Roblox/WinInet",
        "origin": "https://www.roblox.com",
        "referer": "https://www.roblox.com/my/account",
        "x-csrf-token": csrf_token,
        "RBXAuthenticationNegotiation": "1"
    }
    cookies = {".ROBLOSECURITY": auth_cookie}
    return headers, cookies

def refresh_auth_cookie(auth_cookie):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {auth_cookie}\n")

        csrf_token = get_csrf_token(auth_cookie)
        log_file.write(f"{datetime.now()} - CSRF Token: {csrf_token}\n")

        headers, cookies = generate_request_headers(csrf_token, auth_cookie)

        response = httpx.post(AUTH_API_URL, headers=headers, cookies=cookies, json={})
        auth_ticket = response.headers.get("rbx-authentication-ticket", "Failed to get authentication ticket")
        log_file.write(f"{datetime.now()} - Authentication Ticket: {auth_ticket}\n")

        headers["RBXAuthenticationNegotiation"] = "1"
        redeem_data = {"authenticationTicket": auth_ticket}
        
        response = httpx.post(REDEEM_API_URL, headers=headers, json=redeem_data)
        new_auth_cookie = re.search(r".ROBLOSECURITY=(.*?);", response.headers["set-cookie"]).group(1)
        log_file.write(f"{datetime.now()} - New Auth Cookie: {new_auth_cookie}\n\n\n")
        
        return new_auth_cookie

def main():
    auth_cookie = input("Auth Cookie: ")
    new_auth_cookie = refresh_auth_cookie(auth_cookie)
    print(f"\nNew Auth Cookie: {new_auth_cookie}")

if __name__ == "__main__":
    main()
