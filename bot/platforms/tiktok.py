"""TikTok via the free Content Posting API — 'inbox' (draft) mode.

Videos land in your TikTok inbox/drafts; you open TikTok, paste the caption
from the dashboard and tap Post. (Direct public posting needs a TikTok app
audit that personal tools don't qualify for.)

Secrets used: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN
"""
from __future__ import annotations

from pathlib import Path

from ..common import ApiError, DATA, env, http

API = "https://open.tiktokapis.com/v2"
MB = 1024 * 1024


class TikTok:
    def __init__(self):
        self.key = env("TIKTOK_CLIENT_KEY")
        self.secret = env("TIKTOK_CLIENT_SECRET")
        self.refresh = env("TIKTOK_REFRESH_TOKEN")
        self.token = None

    def ready(self) -> bool:
        return bool(self.key and self.secret and self.refresh)

    def auth(self):
        """Access tokens last 24h, so refresh on every run."""
        if self.token:
            return
        r = http("POST", f"{API}/oauth/token/", data={
            "client_key": self.key, "client_secret": self.secret,
            "grant_type": "refresh_token", "refresh_token": self.refresh},
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        j = r.json()
        if "access_token" not in j:
            raise ApiError(f"TikTok token refresh failed: {j}")
        self.token = j["access_token"]
        new_rt = j.get("refresh_token")
        if new_rt and new_rt != self.refresh:
            # the workflow saves this back into GitHub Secrets (needs GH_PAT)
            (DATA / ".tiktok_refresh_token").write_text(new_rt)
            self.refresh = new_rt

    def _h(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json; charset=UTF-8"}

    def upload_draft(self, video: Path) -> str:
        self.auth()
        size = video.stat().st_size
        if size <= 64 * MB:
            chunk, count = size, 1
        else:
            chunk = 10 * MB
            count = size // chunk
        r = http("POST", f"{API}/post/publish/inbox/video/init/", headers=self._h(), json={
            "source_info": {"source": "FILE_UPLOAD", "video_size": size,
                            "chunk_size": chunk, "total_chunk_count": count}})
        j = r.json()
        if (j.get("error") or {}).get("code") not in (None, "ok"):
            raise ApiError(f"TikTok init failed: {j['error']}")
        url = j["data"]["upload_url"]
        pid = j["data"]["publish_id"]
        with open(video, "rb") as f:
            for i in range(count):
                start = i * chunk
                end = size - 1 if i == count - 1 else start + chunk - 1
                f.seek(start)
                part = f.read(end - start + 1)
                http("PUT", url, data=part, headers={
                    "Content-Type": "video/mp4", "Content-Length": str(len(part)),
                    "Content-Range": f"bytes {start}-{end}/{size}"})
        return pid

    def videos(self, max_count: int = 20) -> list[dict]:
        """Public stats for analytics (needs video.list scope)."""
        self.auth()
        fields = "id,create_time,title,share_url,view_count,like_count,comment_count,share_count"
        r = http("POST", f"{API}/video/list/?fields={fields}", headers=self._h(), json={"max_count": max_count})
        return (r.json().get("data") or {}).get("videos", [])
