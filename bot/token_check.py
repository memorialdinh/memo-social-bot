"""Weekly check that every access key still works and isn't about to expire.
Writes data/token_status.json; the workflow opens a GitHub issue if action is needed."""
from __future__ import annotations

from datetime import datetime, timezone

from .common import CFG, DATA, env, http, write_json

WARN_DAYS = 10


def days_left(ts):
    if not ts:
        return None
    return (datetime.fromtimestamp(int(ts), timezone.utc) - datetime.now(timezone.utc)).days


def main():
    out, problems = {}, []

    tok = env("META_PAGE_TOKEN")
    if tok and env("META_APP_ID") and env("META_APP_SECRET"):
        try:
            j = http("GET", f"https://graph.facebook.com/{CFG['api']['graph_version']}/debug_token",
                     params={"input_token": tok, "access_token": f"{env('META_APP_ID')}|{env('META_APP_SECRET')}"}).json()["data"]
            left = days_left(j.get("expires_at")) if j.get("expires_at") else None
            out["meta"] = {"valid": j.get("is_valid"), "days_left": left if left is not None else "never expires"}
            if not j.get("is_valid"):
                problems.append("Meta (Facebook/Instagram) key is no longer valid. Re-run tools/setup_meta.py.")
            elif left is not None and left < WARN_DAYS:
                problems.append(f"Meta key expires in {left} days. Re-run tools/setup_meta.py.")
        except Exception as e:
            problems.append(f"Meta key check failed: {e}")
    elif tok:
        out["meta"] = {"note": "add META_APP_ID + META_APP_SECRET secrets to enable expiry checks"}

    lt = env("LINKEDIN_TOKEN")
    if lt and env("LINKEDIN_CLIENT_ID") and env("LINKEDIN_CLIENT_SECRET"):
        try:
            j = http("POST", "https://www.linkedin.com/oauth/v2/introspectToken", data={
                "client_id": env("LINKEDIN_CLIENT_ID"), "client_secret": env("LINKEDIN_CLIENT_SECRET"), "token": lt}).json()
            left = days_left(j.get("expires_at"))
            out["linkedin"] = {"active": j.get("active"), "days_left": left}
            if not j.get("active"):
                problems.append("LinkedIn key expired. Re-run tools/setup_linkedin.py (takes 2 minutes).")
            elif left is not None and left < WARN_DAYS:
                problems.append(f"LinkedIn key expires in {left} days. Re-run tools/setup_linkedin.py.")
        except Exception as e:
            problems.append(f"LinkedIn key check failed: {e}")

    if env("TIKTOK_REFRESH_TOKEN"):
        from .platforms.tiktok import TikTok
        try:
            TikTok().auth()
            out["tiktok"] = {"ok": True}
        except Exception as e:
            problems.append(f"TikTok key failed: {e}. Re-run tools/setup_tiktok.py.")

    out["problems"] = problems
    out["checked"] = datetime.now(timezone.utc).isoformat(timespec="minutes")
    write_json(DATA / "token_status.json", out)
    (DATA / "token_problems.md").write_text("\n".join(f"- {p}" for p in problems) if problems else "", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
