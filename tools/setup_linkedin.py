"""One-time LinkedIn setup (repeat every ~60 days — the bot reminds you).
Run on your computer:  python3 tools/setup_linkedin.py
"""
import getpass
import json
import secrets
import urllib.parse
import urllib.request
import webbrowser

client_id = input("LinkedIn Client ID: ").strip()
client_secret = getpass.getpass("LinkedIn Client Secret (hidden): ").strip()
redirect = input("Redirect URL (your GitHub Pages callback, e.g. https://USERNAME.github.io/memo-social-bot/oauth-callback.html): ").strip()
state = secrets.token_urlsafe(12)
url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
    "response_type": "code", "client_id": client_id, "redirect_uri": redirect,
    "state": state, "scope": "openid profile w_member_social"})
print("\nOpening LinkedIn… approve access, then copy the code shown on the page.")
webbrowser.open(url)
print(url)
code = input("\nPaste the code: ").strip()

data = urllib.parse.urlencode({"grant_type": "authorization_code", "code": code, "redirect_uri": redirect,
                               "client_id": client_id, "client_secret": client_secret}).encode()
tok = json.load(urllib.request.urlopen(urllib.request.Request("https://www.linkedin.com/oauth/v2/accessToken", data=data)))
access = tok["access_token"]
me = json.load(urllib.request.urlopen(urllib.request.Request("https://api.linkedin.com/v2/userinfo",
                                                             headers={"Authorization": f"Bearer {access}"})))
print("\n✅ Add/update these GitHub Secrets:\n")
print(f"LINKEDIN_TOKEN         = {access}")
print(f"LINKEDIN_AUTHOR_URN    = urn:li:person:{me['sub']}")
print(f"LINKEDIN_CLIENT_ID     = {client_id}")
print("LINKEDIN_CLIENT_SECRET = (the secret you pasted)")
print(f"\nThis key lasts about {tok.get('expires_in', 0) // 86400} days.")
