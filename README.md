# Memo Social Bot

Free, self-running social media system for **Memo Dinh | Prestige Luxury Group | Epique Realty**.

- **Writes** 10 pieces a day (3 posts, 2 reels, 5 stories) from fresh market research — via a Claude scheduled task
- **Designs** branded graphics and animated reels with your headshot (black/gold, Space Grotesk)
- **Checks** compliance: DRE footer, Fair Housing wording, no guarantees, law posts held for approval
- **Posts** to Instagram, Facebook and LinkedIn on schedule; TikTok as ready-to-post drafts
- **Learns** your best posting times and best-performing topics, and reschedules around them
- **Dashboard** with followers, engagement, best-time heatmap, queue and TikTok captions

Start with **[SETUP.md](SETUP.md)**. Writer rules: **[CONTENT_BRIEF.md](CONTENT_BRIEF.md)**. Settings: **[config.yaml](config.yaml)**.

| Folder | What's in it |
|---|---|
| `queue/DATE/` | each day's content (YAML) + rendered `media/` |
| `bot/` | the code: render, plan, validate, publish, analytics, dashboard |
| `.github/workflows/` | the schedules that run it all |
| `data/` | stats history, best times, publish log |
| `docs/` | your dashboard (GitHub Pages) |
| `knowledge/` | the writer's market notes and topic log |
| `tools/` | one-time key setup scripts |
| `examples/` | sample day of content |

Run locally: `pip install -r requirements.txt`, then `python -m bot.render`, `python -m bot.plan`,
`python -m bot.publish --dry-run`, `python -m bot.analytics --offline`.
