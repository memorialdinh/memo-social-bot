"""One-time Meta setup. Run on your computer:  python3 tools/setup_meta.py

You'll paste: your Meta App ID, App Secret, and a short-lived token from
Graph API Explorer. It prints the 3 values to save as GitHub Secrets.
Nothing is saved or sent anywhere except Meta.
"""
import getpass
import json
import urllib.parse
import urllib.request

VER = "v25.0"


def get(url, **params):
    with urllib.request.urlopen(f"{url}?{urllib.parse.urlencode(params)}") as r:
        return json.load(r)


app_id = input("Meta App ID: ").strip()
secret = getpass.getpass("Meta App Secret (hidden): ").strip()
short = getpass.getpass("Short-lived User Token from Graph API Explorer (hidden): ").strip()

long_user = get(f"https://graph.facebook.com/{VER}/oauth/access_token", grant_type="fb_exchange_token",
                client_id=app_id, client_secret=secret, fb_exchange_token=short)["access_token"]
pages = get(f"https://graph.facebook.com/{VER}/me/accounts", access_token=long_user,
            fields="id,name,access_token,instagram_business_account{id,username}")["data"]
if not pages:
    raise SystemExit("No Facebook Pages found. Make sure you picked your Page when granting access.")
for i, p in enumerate(pages):
    ig = (p.get("instagram_business_account") or {}).get("username", "no Instagram linked")
    print(f"  [{i}] {p['name']}  (Instagram: {ig})")
pick = pages[int(input("Which Page? number: ") or 0)] if len(pages) > 1 else pages[0]
ig = pick.get("instagram_business_account") or {}

print("\n✅ Add these in GitHub → Settings → Secrets and variables → Actions → New repository secret:\n")
print(f"META_PAGE_ID     = {pick['id']}")
print(f"META_IG_ID       = {ig.get('id', '(link Instagram to this Page first)')}")
print(f"META_PAGE_TOKEN  = {pick['access_token']}")
print(f"META_APP_ID      = {app_id}")
print("META_APP_SECRET  = (the App Secret you just pasted)")
print("\nThis Page token doesn't expire unless you change your Facebook password or remove the app.")
