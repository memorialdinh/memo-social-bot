"""LinkedIn personal-profile posting via the free Posts API (w_member_social).

Secrets used: LINKEDIN_TOKEN. LINKEDIN_AUTHOR_URN is optional — when it isn't
set, the author URN is looked up once from the token and cached in data/.
"""
from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import quote

from ..common import CFG, DATA, ApiError, env, http

API = "https://api.linkedin.com/rest"
_RESERVED = r"\|{}@[]()<>#*_~"


def little_text(s: str) -> str:
    """LinkedIn 'little text' format: escape reserved chars, keep #hashtags clickable."""
    out = []
    for part in re.split(r"(#\w+)", s):
        if re.fullmatch(r"#\w+", part):
            out.append("{hashtag|\\#|" + part[1:] + "}")
        else:
            out.append("".join("\\" + ch if ch in _RESERVED else ch for ch in part))
    return "".join(out)


class LinkedIn:
    def __init__(self):
        self.token = env("LINKEDIN_TOKEN")
        self._author = env("LINKEDIN_AUTHOR_URN")

    @property
    def author(self) -> str:
        """Who the post is published as. Looked up from the token if not set."""
        if not self._author and self.token:
            self._author = self._whoami()
        return self._author

    def _whoami(self) -> str:
        """urn:li:person:<id> from /v2/userinfo. Cached so it's fetched once."""
        cache = DATA / "linkedin_author.txt"
        if cache.exists():
            cached = cache.read_text().strip()
            if cached:
                return cached
        try:
            r = http("GET", "https://api.linkedin.com/v2/userinfo",
                     headers={"Authorization": f"Bearer {self.token}"})
            sub = (r.json() or {}).get("sub", "")
        except Exception:
            return ""
        if not sub:
            return ""
        urn = f"urn:li:person:{sub}"
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(urn)
        return urn

    def ready(self) -> bool:
        return bool(self.token and self.author)

    def _h(self, json_body=True):
        h = {"Authorization": f"Bearer {self.token}",
             "LinkedIn-Version": str(CFG["api"]["linkedin_version"]),
             "X-Restli-Protocol-Version": "2.0.0"}
        if json_body:
            h["Content-Type"] = "application/json"
        return h

    def _upload_image(self, img: Path) -> str:
        r = http("POST", f"{API}/images?action=initializeUpload", headers=self._h(),
                 json={"initializeUploadRequest": {"owner": self.author}})
        v = r.json()["value"]
        http("PUT", v["uploadUrl"], data=img.read_bytes(),
             headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/octet-stream"})
        return v["image"]

    def _upload_video(self, video: Path) -> str:
        data = video.read_bytes()
        r = http("POST", f"{API}/videos?action=initializeUpload", headers=self._h(), json={
            "initializeUploadRequest": {"owner": self.author, "fileSizeBytes": len(data),
                                        "uploadCaptions": False, "uploadThumbnail": False}})
        v = r.json()["value"]
        etags = []
        for ins in v["uploadInstructions"]:
            chunk = data[ins["firstByte"]: ins["lastByte"] + 1]
            up = http("PUT", ins["uploadUrl"], data=chunk, headers={"Content-Type": "application/octet-stream"})
            etags.append(up.headers.get("etag") or up.headers.get("ETag"))
        http("POST", f"{API}/videos?action=finalizeUpload", headers=self._h(), json={
            "finalizeUploadRequest": {"video": v["video"], "uploadToken": v.get("uploadToken", ""),
                                      "uploadedPartIds": etags}})
        # wait until LinkedIn finishes processing
        urn = v["video"]
        for _ in range(60):
            st = http("GET", f"{API}/videos/{quote(urn, safe='')}", headers=self._h()).json()
            if st.get("status") == "AVAILABLE":
                break
            if st.get("status") == "PROCESSING_FAILED":
                raise ApiError("LinkedIn video processing failed")
            time.sleep(5)
        return urn

    def post(self, media: Path, text: str, title: str = "") -> str:
        urn = self._upload_video(media) if media.suffix == ".mp4" else self._upload_image(media)
        body = {
            "author": self.author,
            "commentary": little_text(text),
            "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "content": {"media": {"id": urn, "title": title[:200] or "Memo Dinh"}},
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        r = http("POST", f"{API}/posts", headers=self._h(), json=body)
        return r.headers.get("x-restli-id") or r.headers.get("x-linkedin-id") or "posted"
