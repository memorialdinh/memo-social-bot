# Setup Guide — Memo's Free Social Bot

About 60–90 minutes, one time. After that it runs itself.
Cost: **$0** (GitHub, Meta, LinkedIn and TikTok APIs are all free for this).

---

## What you're building

```
Claude (every evening)          GitHub (free, runs 24/7)                 Your accounts
─────────────────────           ───────────────────────────              ─────────────
researches the market   ──►     renders branded graphics + reels  ──►    Instagram
writes tomorrow's 10 posts      checks compliance                         Facebook
learns from your stats   ◄──    posts on schedule (every 15 min)          LinkedIn
                                pulls stats, learns best times            TikTok (drafts)
                                updates your dashboard
```

---

## Step 1 — GitHub (10 min)

1. Create a free account at **github.com** (skip if you have one).
2. Click **+ → New repository**. Name it `memo-social-bot`. Choose **Public**. Click **Create**.
   - Why public: it keeps GitHub's automation 100% free and lets Instagram fetch your images.
     Your passwords/keys are stored in encrypted **Secrets** — never visible to anyone.
     (What *is* visible: your upcoming posts and the dashboard. Nothing private goes in either.)
3. Tell Claude the repo name (e.g. `yourusername/memo-social-bot`). Claude will push all the files for you.
   *Or do it yourself:* install **GitHub Desktop**, clone the repo, copy this folder's contents in
   (make sure the hidden `.github` folder comes along — on Mac press ⌘⇧. in Finder to show it), and push.
4. In the repo: **Settings → Actions → General → Workflow permissions → Read and write → Save.**
5. **Settings → Pages → Source: Deploy from a branch → Branch: `main` / folder `/docs` → Save.**
   Your dashboard will live at `https://YOURUSERNAME.github.io/memo-social-bot/`
   and the setup callback page at `https://YOURUSERNAME.github.io/memo-social-bot/oauth-callback.html`.

## Step 2 — Your photos and logo (5 min)

- Upload 4–8 headshots to `assets/headshots/` (JPG or PNG, face centered, at least 800×800).
  Each platform gets a different one each day, automatically.
- Upload your Epique logo to `assets/logos/` named **`logo-white.png`** (white/gold version, transparent background).
  It's only resized, never reshaped.

In GitHub: open the folder → **Add file → Upload files**.

## Step 3 — Facebook + Instagram (20 min)

**Before you start:** Instagram must be a **Professional (Business or Creator)** account and linked to your
Facebook **Page** (Instagram app → Settings → Account type and tools / Accounts Center).

1. Go to **developers.facebook.com** → log in → **My Apps → Create App**.
   Choose the use case for managing a Page/Instagram content (Business type). Name it "Memo Publisher".
2. In the app: add the **Instagram** (Instagram API with Facebook Login) and **Facebook Login for Business** products if asked.
3. **App settings → Basic**: set Privacy Policy URL to
   `https://YOURUSERNAME.github.io/memo-social-bot/privacy.html`. Copy the **App ID** and **App Secret**.
4. Open **Graph API Explorer** (Tools menu). Pick your app. Click **Generate Access Token** and grant:
   `pages_show_list, pages_read_engagement, pages_manage_posts, pages_read_user_content, read_insights,
   instagram_basic, instagram_content_publish, instagram_manage_insights, business_management`
   plus, for the engagement brain (comments + DMs): `instagram_manage_comments, instagram_manage_messages,
   pages_manage_engagement, pages_messaging`. One token covers both repos.
   Also turn on **Allow access to messages** in the Instagram app → Settings → Messages and story replies → Connected tools.
   Select your Page and Instagram account when it asks. Copy the token.
5. On your computer, in Terminal, in this folder: `python3 tools/setup_meta.py`
   Paste App ID, App Secret, and the token. It prints your values.
6. Switch the app from **Development** to **Live** (top of the app dashboard) so posts are public.

## Step 4 — LinkedIn (15 min, repeat the last step every ~60 days)

1. Go to **linkedin.com/developers → Create app**. LinkedIn requires a Company Page to attach it to —
   use your Prestige Luxury Group page (or create one; it takes a minute).
2. **Products** tab: add **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn**.
3. **Auth** tab: add redirect URL `https://YOURUSERNAME.github.io/memo-social-bot/oauth-callback.html`.
   Copy **Client ID** and **Client Secret**.
4. Run `python3 tools/setup_linkedin.py`, approve in the browser, copy the code shown, paste it back.

LinkedIn keys last ~60 days. The bot opens a GitHub issue (you get an email) 10 days before it expires —
just re-run step 4.

## Step 5 — TikTok (15 min)

1. **developers.tiktok.com** → Manage apps → **Connect an app**. Add products **Login Kit** and
   **Content Posting API**. Scopes: `user.info.basic`, `video.upload`, `video.list`.
2. Redirect URI: `https://YOURUSERNAME.github.io/memo-social-bot/oauth-callback.html`.
   Use the app's **Sandbox** and add your own TikTok account as a test user if TikTok asks.
3. Run `python3 tools/setup_tiktok.py`, approve, paste the code back.

TikTok videos arrive in your **TikTok inbox as drafts**. Open TikTok, tap the draft, paste the caption
(copy button on your dashboard), Post. ~30 seconds a day.

## Step 6 — Save your keys in GitHub (5 min)

Repo → **Settings → Secrets and variables → Actions → New repository secret**. Add each:

| Secret | From |
|---|---|
| `META_PAGE_TOKEN`, `META_PAGE_ID`, `META_IG_ID` | setup_meta.py |
| `META_APP_ID`, `META_APP_SECRET` | Meta app → Basic settings |
| `LINKEDIN_TOKEN` | LinkedIn Developers → your app → Auth → OAuth 2.0 tools. The author URN is looked up automatically. |
| `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET` | LinkedIn app → Auth |
| `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` | setup_tiktok.py |
| `GH_PAT` *(optional, recommended)* | GitHub → Settings → Developer settings → Fine-grained token → this repo only → permission **Secrets: Read and write**. Lets the bot keep the TikTok key fresh by itself. |

You can skip any platform — the bot simply waits on that one until its keys exist.

## Step 7 — Test it (5 min)

1. **Actions → Prepare content → Run workflow.** Check `queue/` for rendered images/videos.
2. **Actions → Publish → Run workflow → tick "Dry run".** The log shows what *would* post.
3. **Actions → Analytics → Run workflow.** Open your dashboard link.
4. When you're happy, let it run. Keep Metricool for 2–3 weeks side by side, then cancel.

## Step 8 — Engagement brain (comments, DMs, Birthday Club)

Set up the second, **private** repo `memo-social-brain` — see its own SETUP.md. Same Meta secrets.

## Step 9 — Turn on the daily writer

Tell Claude: *"Connect the content writer to `yourusername/memo-social-bot`."*
Claude sets up a scheduled task that runs every evening: researches the market, writes tomorrow's
10 pieces following `CONTENT_BRIEF.md`, and pushes them. GitHub does the rest.

---

## Your daily routine (2–5 minutes)

- **Dashboard** (bookmark it): anything waiting for approval, failures, TikTok drafts.
- **Approve law posts**: GitHub app → Actions → **Approve posts** → Run workflow → enter the date.
- **TikTok**: post the drafts with the copied captions.

## Changing things

Everything lives in `config.yaml` (edit on GitHub with the pencil icon):
- turn a platform off, change daily volume, default times, approval rules, topic weights
- `require_approval_all: true` if you want to approve every post by hand

To pull a post: delete its file in `queue/DATE/` before its time. To fix one: edit its YAML; the bot re-renders.

## Troubleshooting

| Problem | Fix |
|---|---|
| Nothing posts | Actions tab → check Publish runs are green. Settings → Actions must be enabled with Read/write. |
| "keys not set" in logs | That platform's secrets are missing or misspelled. |
| Instagram error about the image URL | Repo must be **Public**; wait 5 minutes after Prepare runs. |
| LinkedIn 401 | Key expired → re-run `tools/setup_linkedin.py`. |
| LinkedIn "version" error | Bump `linkedin_version` in config.yaml to a recent month, e.g. `202610`. |
| Facebook/IG posts only visible to you | Switch the Meta app to **Live**. |
| TikTok "unaudited" error | Make sure your account is added as a Sandbox test user. Drafts-to-inbox should still work. |
| Scheduled runs stopped | GitHub pauses schedules after 60 days with no commits. The bot commits daily, so this only happens if it's been off. Re-enable in Actions. |

Posting times run a few minutes late sometimes — GitHub schedules aren't to-the-second. That's normal.
