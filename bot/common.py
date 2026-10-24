"""Shared helpers: config, queue files, time, HTTP."""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "queue"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

KINDS = ("post", "reel", "story")
PLATFORMS = ("instagram", "facebook", "linkedin", "tiktok")


def load_config() -> dict:
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


CFG = load_config()
TZ = ZoneInfo(CFG.get("timezone", "America/Los_Angeles"))


def now() -> datetime:
    fake = os.environ.get("BOT_NOW")  # for testing: "2026-10-24T09:20"
    if fake:
        return datetime.fromisoformat(fake).replace(tzinfo=TZ)
    return datetime.now(TZ)


def stable_int(*parts) -> int:
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return int(h[:8], 16)


# ── Queue ────────────────────────────────────────────────────
class Item:
    """One queued piece of content (queue/YYYY-MM-DD/<id>.yaml)."""

    def __init__(self, path: Path):
        self.path = path
        self.day = date.fromisoformat(path.parent.name)
        with open(path, encoding="utf-8") as f:
            self.d = yaml.safe_load(f) or {}
        self.d.setdefault("id", path.stem)
        self.d.setdefault("status", {})
        self.d.setdefault("media", {})
        self.d.setdefault("schedule", {})

    @property
    def id(self) -> str:
        return str(self.d["id"])

    @property
    def kind(self) -> str:
        return self.d.get("kind", "post")

    @property
    def track(self) -> str:
        return self.d.get("track", "market_update")

    def platforms(self) -> list[str]:
        wanted = self.d.get("platforms") or CFG["routing"][self.kind]
        allowed = CFG["routing"][self.kind]
        return [p for p in wanted if p in allowed and CFG["platforms"].get(p, {}).get("enabled", True)]

    def needs_approval(self) -> bool:
        # Only YOUR approval (bot.approve / the Approve workflow) clears these:
        if CFG.get("require_approval_all") or self.track in CFG.get("require_approval_tracks", []):
            return not self.d.get("approved_override")
        if self.d.get("approved_override"):
            return False
        return self.d.get("approved") is False

    def media_path(self, platform: str) -> Path | None:
        rel = self.d["media"].get(platform)
        return (ROOT / rel) if rel else None

    def scheduled_at(self, platform: str) -> datetime | None:
        s = self.d["schedule"].get(platform)
        return datetime.fromisoformat(s) if s else None

    def state(self, platform: str) -> str:
        return (self.d["status"].get(platform) or {}).get("state", "pending")

    def set_status(self, platform: str, **kw):
        st = self.d["status"].setdefault(platform, {})
        st.update(kw)
        st["at"] = now().isoformat(timespec="seconds")
        self.save()

    def caption(self, platform: str) -> str:
        caps = self.d.get("captions") or {}
        text = (caps.get(platform) or caps.get("default") or "").strip()
        footer_key = "agent_compliance_footer" if self.track == "agent_attraction" else "compliance_footer"
        footer = CFG["brand"][footer_key]
        if text and "DRE" not in text:
            text = f"{text}\n\n{footer}"
        return text

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.d, f, sort_keys=False, allow_unicode=True, width=1000)


def day_dirs() -> list[Path]:
    if not QUEUE.exists():
        return []
    out = []
    for p in sorted(QUEUE.iterdir()):
        if p.is_dir():
            try:
                date.fromisoformat(p.name)
                out.append(p)
            except ValueError:
                pass
    return out


def load_items(days: list[date] | None = None) -> list[Item]:
    items = []
    for d in day_dirs():
        if days and date.fromisoformat(d.name) not in days:
            continue
        for f in sorted(d.glob("*.yaml")):
            items.append(Item(f))
    return items


def recent_days(back: int = 2, ahead: int = 2) -> list[date]:
    t = now().date()
    return [t + timedelta(days=i) for i in range(-back, ahead + 1)]


# ── HTTP ─────────────────────────────────────────────────────
class ApiError(Exception):
    pass


def http(method: str, url: str, *, retries: int = 3, ok=(200, 201, 202, 204), **kw) -> requests.Response:
    kw.setdefault("timeout", 120)
    last = None
    for attempt in range(retries):
        try:
            r = requests.request(method, url, **kw)
        except requests.RequestException as e:
            last = str(e)
            time.sleep(3 * (attempt + 1))
            continue
        if r.status_code in ok:
            return r
        last = f"{r.status_code} {r.text[:500]}"
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(5 * (attempt + 1))
            continue
        break
    raise ApiError(f"{method} {url.split('?')[0]} failed: {last}")


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


def env(name: str) -> str | None:
    v = os.environ.get(name, "").strip()
    return v or None
