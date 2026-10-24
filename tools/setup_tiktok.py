"""One-time TikTok setup. Run on your computer:  python3 tools/setup_tiktok.py"""
import getpass
import json
import secrets
import urllib.parse
import urllib.request
import webbrowser

key = input("TikTok Client Key: ").strip()
secret = getpass.getpass("TikTok Client Secret (hidden): ").strip()
redirect = input("Redirect URL (your GitHub Pages callback, e.g. https://USERNAME.github.io/memo-social-bot/oauth-callback.html): ").strip()
url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
    "client_key": key, "response_type": "code", "redirect_uri": redirect,
    "scope": "user.info.basic,video.upload,video.list", "state": secrets.token_urlsafe(12)})
print("\nOpening TikTok… approve access, then copy the code shown on the page.")
webbrowser.open(url)
print(url)
code = urllib.parse.unquote(input("\nPaste the code: ").strip())
data = urllib.parse.urlencode({"client_key": key, "client_secret": secret, "code": code,
                               "grant_type": "authorization_code", "redirect_uri": redirect}).encode()
req = urllib.request.Request("https://open.tiktokapis.com/v2/oauth/token/", data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
tok = json.load(urllib.request.urlopen(req))
if "refresh_token" not in tok:
    raise SystemExit(f"TikTok said: {tok}")
print("\n✅ Add these GitHub Secrets:\n")
print(f"TIKTOK_CLIENT_KEY     = {key}")
print("TIKTOK_CLIENT_SECRET  = (the secret you pasted)")
print(f"TIKTOK_REFRESH_TOKEN  = {tok['refresh_token']}")
print("\nThe bot refreshes this automatically (add the optional GH_PAT secret so it can save the new one).")
