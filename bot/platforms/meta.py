"""Facebook Page + Instagram (Business) publishing through Meta's free Graph API.

Secrets used: META_PAGE_TOKEN, META_PAGE_ID, META_IG_ID
"""
from __future__ import annotations

import time
from pathlib import Path

from ..common import CFG, ApiError, env, http

VER = CFG["api"]["graph_version"]
GRAPH = f"https://graph.facebook.com/{VER}"


class Meta:
    def __init__(self):
        self.token = env("META_PAGE_TOKEN")
        self.page_id = env("META_PAGE_ID")
        self.ig_id = env("META_IG_ID")

    def ready_fb(self) -> bool:
        return bool(self.token and self.page_id)

    def ready_ig(self) -> bool:
        return bool(self.token and self.ig_id)

    # ── low level ──
    def _call(self, method, path, **kw):
        params = kw.pop("params", {}) or {}
        params["access_token"] = self.token
        r = http(method, f"{GRAPH}/{path.lstrip('/')}", params=params, **kw)
        j = r.json() if r.content else {}
        if isinstance(j, dict) and j.get("error"):
            raise ApiError(j["error"].get("message", str(j["error"])))
        return j

    def get(self, path, **params):
        return self._call("GET", path, params=params)

    def post(self, path, data=None, files=None, **params):
        return self._call("POST", path, params=params, data=data, files=files)

    # ── Facebook Page ──
    def fb_photo(self, img: Path, caption: str) -> str:
        with open(img, "rb") as f:
            j = self.post(f"{self.page_id}/photos", data={"message": caption, "published": "true"},
                          files={"source": (img.name, f, "image/jpeg")})
        return j.get("post_id") or j["id"]

    def fb_story_photo(self, img: Path) -> str:
        with open(img, "rb") as f:
            ph = self.post(f"{self.page_id}/photos", data={"published": "false"},
                           files={"source": (img.name, f, "image/jpeg")})
        j = self.post(f"{self.page_id}/photo_stories", data={"photo_id": ph["id"]})
        return j.get("post_id") or ph["id"]

    def fb_reel(self, video: Path, caption: str) -> str:
        start = self.post(f"{self.page_id}/video_reels", data={"upload_phase": "start"})
        vid = start["video_id"]
        url = start.get("upload_url") or f"https://rupload.facebook.com/video-upload/{VER}/{vid}"
        data = video.read_bytes()
        http("POST", url, data=data, headers={
            "Authorization": f"OAuth {self.token}", "offset": "0", "file_size": str(len(data))})
        self.post(f"{self.page_id}/video_reels", data={
            "upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED", "description": caption})
        return vid

    # ── Instagram ──
    def _ig_wait(self, container: str, limit: int = 600):
        t0 = time.time()
        while time.time() - t0 < limit:
            j = self.get(container, fields="status_code,status")
            code = j.get("status_code")
            if code in ("FINISHED", "PUBLISHED"):
                return
            if code in ("ERROR", "EXPIRED"):
                raise ApiError(f"Instagram processing failed: {j.get('status')}")
            time.sleep(6)
        raise ApiError("Instagram processing timed out")

    def _ig_publish(self, container: str) -> str:
        self._ig_wait(container)
        return self.post(f"{self.ig_id}/media_publish", data={"creation_id": container})["id"]

    def ig_image(self, image_url: str, caption: str, story: bool = False) -> str:
        data = {"image_url": image_url}
        if story:
            data["media_type"] = "STORIES"
        else:
            data["caption"] = caption
        c = self.post(f"{self.ig_id}/media", data=data)["id"]
        return self._ig_publish(c)

    def ig_reel(self, video: Path, caption: str) -> str:
        j = self.post(f"{self.ig_id}/media", data={
            "media_type": "REELS", "upload_type": "resumable", "caption": caption, "share_to_feed": "true"})
        cid = j["id"]
        uri = j.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{VER}/{cid}"
        data = video.read_bytes()
        http("POST", uri, data=data, headers={
            "Authorization": f"OAuth {self.token}", "offset": "0", "file_size": str(len(data))})
        return self._ig_publish(cid)

    def ig_publishing_quota(self) -> dict:
        return self.get(f"{self.ig_id}/content_publishing_limit", fields="config,quota_usage")
