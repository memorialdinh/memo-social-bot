# Playbook — the editorial brain

Maintained by **Mentor** (Sundays). Read by **Scribe** every night before writing. This is the
standing knowledge: what to say, how to say it, what not to say, and why. The week plan says *what*
goes out; this says *how it should land*.

---

## 1. What this content is for

Memo isn't selling posts, he's shortening the distance between a stranger and a consultation. The
path is always the same:

**someone has a question → he answers it straight → they trust the answer → they DM a keyword → a
call → a client.**

Every piece should move someone one step along that path. If a post doesn't educate, make someone
feel capable, or make them laugh enough to remember his face, it's filler.

**The keyword CTAs are the conversion point**, and they're what the engagement bot answers
automatically: `RATES`, `BUYER`, `SELLER`, `VALUE`, `PROP 19`, `AGREEMENT`, `MATH`, `INVEST`,
`BDAY`, `PLAN`. One per piece. Never two.

## 2. Voice — the four registers

Memo is direct, warm, a little punchy, and never performs expertise. Mix the registers; a feed that
is all one note stops working.

**Educational** (the floor, ~half the output). Plain answers to real questions, with the number.
The test: could a reader act on this today? "Here's what a lender actually verifies" beats
"understanding the mortgage process."

**Funny** (~1 a day). The joke is about the *process*, never about people — see the meme rules in
CONTENT_BRIEF. Memo is usually the one being roasted. Humour buys attention that education spends.

**Motivational** (~2 a week, `quote` template). Not hustle-porn, not "manifest your dream home."
The motivating thing in real estate is **clarity**: someone who thought buying was impossible
learning what it actually takes. "You don't need to be ready, you need to know your numbers" works.
"Grind until you make it" doesn't, and it isn't him.

**Empowering** (woven through). Give people the actual arithmetic so they can decide for themselves,
including when the answer is "don't buy yet." Someone who trusts him enough to wait a year is worth
more than someone pushed into a bad purchase. Never make a reader feel behind or stupid.

**Banned words**, always: dive in, navigate, unlock, elevate, seamless, game-changer, nestled,
boasts, "dream home" as filler. No ALL-CAPS shouting. No hype.

## 3. The audiences and what each one needs

| Audience | Where they are | What earns them |
|---|---|---|
| **First-time buyers** | Scared of the money, don't know the steps | The real number. Down payment reality, closing costs, what pre-approval checks, assistance programs |
| **Move-up sellers** | Have equity, worried about timing and the next purchase | Net sheets, pricing math, sell-first vs buy-first, what prep actually returns |
| **Investors** | Running numbers already | Cap rate vs cash-on-cash, price per sq ft used correctly, ADUs, 1031 basics, Mello-Roos |
| **Inheritors / trustees** | Overwhelmed, often grieving | Gentle, procedural, "not legal advice", timelines, who to call first |
| **Agents** (recruiting) | Weighing a move, tired of being sold to | Cost per deal, cap questions, what changes after cap. Never income promises |
| **Sphere / past clients** | Already trust him | Birthdays, anniversaries, local notes, the human stuff |

## 4. Seasonality — plan around these

- **Nov 1 / Dec 10** — CA property tax 1st installment due / delinquent. **Feb 1 / Apr 10** — 2nd.
  Reliable, useful, recurring. Always cite the county tax collector.
- **Late Nov** — FHFA announces next year's conforming loan limits.
- **Dec** — "should I wait until spring?" season. Fewer buyers, more serious ones.
- **Jan** — new-year listings, resolution energy, tax documents arriving.
- **Mar–Jun** — spring market, highest inventory and competition.
- **Sep–Oct** — back-to-school slowdown, then the pre-holiday push.
- **Weekly** — Freddie Mac PMMS releases Thursday mornings. **Monthly** — C.A.R. sales and price
  report, roughly the third week, covering the prior month.

## 5. Compliance — the spine, not a disclaimer

These are not optional and they are not footnotes. A post that breaks one doesn't go out.

- **Fair Housing.** Describe homes and places, never who should live in them. No "perfect for
  families", "safe neighborhood", "exclusive community", nothing touching race, religion, national
  origin, sex, disability or familial status. This applies to jokes exactly as it applies to
  listings.
- **No guarantees, no predictions as fact.** Not "prices will", not "rates will", not "you'll make".
- **No superiority claims.** No "best agent", "#1", "top producer".
- **Every number needs a dated source** in `sources:`. If it can't be verified, it doesn't appear.
  **The as-of date belongs on the graphic too, not only in the caption.** Stories carry no caption at
  all, so a bare figure on a story has no date anywhere. Checked Oct 25, 2026 and found two: the p2
  graphic ("active listings rose just 0.5% in a year... Supply is 3.7 months") and the s4 story
  ("CA homes closed at 98.8% of list price") both ran dateless. Write the period into the
  `stat_label`, the `fact:` line or the story `headline` — "Sept 2026", "as of Oct 22" — every time.
- **Identification** on every graphic and caption: Memo Dinh, DRE #02066757, Epique Realty, Equal
  Housing Opportunity. The renderer does this; never remove it.
- **Agent recruiting**: no income, earnings or revenue-share promises. Revenue share and equity are
  "subject to plan terms". Never disparage another brokerage.
- **Legal / tax / lending**: general information only, then "Not legal, tax or lending advice" and
  an invitation to talk. Never advise on a specific person's situation in a post.
  **That disclaimer lives in the caption footer, and stories have no caption** — and `fine_print`
  renders on `spotlight` only. So on any legal, tax or lending **story**, write the disclaimer into
  the `explain` line. Found Nov 9, 2026: the Nov 6 `s1` Prop 19 quiz answered a property-tax
  question with a BOE cite and no disclaimer anywhere.
- **Never claim**: deal counts, "100+", sales volume, that Memo speaks Vietnamese, or his schools
  and degree.
- Values are "estimates, not an appraisal". Payment examples state their assumptions and are "not a
  loan offer".

## 6. What actually works, from Memo's own numbers

Updated by Mentor from `data/insights.json` and `data/posts.csv` each week. **As of Nov 16, 2026.**

- **Still reach-starved, and this was the first zero-save zero-share week.** Nov 9–15: 78 rows,
  **2,288 reach, 59 engagements, 0 saves, 0 shares** across both platforms, down from 1 save the
  week before. Read almost every 0.0% in `insights.json` as a reach reading, not a content one.
- **Memo's own camera content is out-earning the bot about twenty to one.** Nov 9–15 on Instagram:
  his **10 untagged rows took 55 of the week's 59 engagements** on 945 reach (5.8%); the bot's **44
  tagged rows took 4** on 1,341 reach (0.3%). One reel he shot Nov 10 did **22 engagements on 214
  reach** — a third of the week in one piece. **Third week running.** The fitness journey, showing
  days, escrow wins, family. **The bot cannot make this — it needs his camera.** Education is the
  floor; his footage is the ceiling. Say it when a week looks flat.
- **Static posts earned nothing at all.** Nov 9–15 engagements per item: reels **2.61**, stories
  **0.48**, posts **0.00** — the bot's 11 Instagram posts took **0 engagements on 410 reach**. The
  1-post/2-reel feed is right and the cut to 3 items made it righter.
- **⚠ NEW: every static post lands 7–10pm, the hours `best_times.json` ranks worst** (all 11 at
  19:02–21:59; the IG heatmap reads 0.66–0.78 there against 1.63–1.74 at 7am). `post_hours` in
  `config.yaml` is deliberate but was set on **n=5** posts marked "thin, directional", and **n=11 at
  zero outweighs that.** With posts at 0 in *every* window the hour can't be shown to be the cause,
  so **not yet a reason to move it** — only to stop spending that slot on anything load-bearing.
- **Facebook got worse again:** **24 rows, 2 total reach, 0 engagements**, down from 36 rows/5
  reach. `best_times.json` still ranks Instagram only, and the Nov 12 one-caption change is right.
  Keep posting, never optimise, never spend a pass on it.
- **Follower counts are not the signal.** Instagram 817 → 816 (815 on Nov 14); Facebook 288 → 291,
  and `insights.json` shows Facebook +74 over 60 days against **2 reach for the week**. A fact, not
  growth, and **not to be cited as growth** anywhere.
- **The writer failure mode has not recurred — two clean weeks.** Every night Nov 12–15 committed
  its `bot: queue <date>` and market note two days ahead, and the volume cut landed: 5 items a day
  from Nov 13. Keep checking every run.
- **⚠ The cut's real cost was the two rows nobody protected, exactly as rule 9 predicted.** The
  **Sun Nov 15 Spotlight was never written** (the replan the Nov 12 note asked for didn't happen;
  the series is **still stuck at #8**) and the **Sat Nov 14 meme** went the same way: both days still
  listed 5 feed rows, so Scribe took the top 3 by the brief's precedence order, where humor is 5th
  and the Spotlight 4th. *Fix, applied Nov 16:* the plan now carries **exactly 3 feed rows a day**,
  names the yielding requirement per day, and says the Wed/Sun Spotlight never yields.
- **Both §5 defects are now clean, and the fixes work.** Dateless figures: **third clean week** —
  every Nov 9–15 graphic with a market figure carried its period (the only sweep flags were court
  form numbers DE-260/DE-265 and a "REAL ESTATE 101" kicker). Story disclaimers: the Nov 13 `s1`
  probate quiz — the same shape of piece that went out bare on Nov 6 — carried "Not legal advice;
  ask your own attorney." in its `explain` line, and no legal, tax or lending story published bare.
  **Keep both sweeps every run**; they are cheap and they caught real problems twice.
- **`quote` is now a story and `cta` stayed out — but only one of those has evidence.** Nov 9–15
  reach-per-item: `process` 46.2, `compare` 40.0, `stat` 37.7, **`cta` 32.0**, `meme` 30.8, `quote`
  29.5, `spotlight` 28.0, `quiz` 27.9, `tip` 25.8, `checklist` 20.8, `explainer` 13.0 — all on 0–1
  engagements. **This week does NOT reproduce the anti-`cta` finding**: the one `cta` card sat
  mid-pack among posts (26–54 reach). That directive stands because `insights.json` carries it and
  3 feed items leave no spare slot, **not** because the data showed it again. `quote` lost its slot
  for the reason that holds: reach with zero engagements is the cheapest thing to move off the feed.
  **Never drop the weekly offer to satisfy the template directive** — Thursday's `cta_sub` meets it.
- **The fetch wall is unpredictable, and there is one real workaround.** Nov 12: all three Freddie
  Mac hosts returned `PROVENANCE_REQUIRED`. Nov 14: **`globenewswire.com` carries Freddie Mac's own
  PMMS release and loaded first try** — try it before `freddiemac.com` on every rate run. Another
  Nov 14 run got zero fetches; a third read `car.org` in full. **C.A.R. still has no October 2026
  sales report** (four runs) and **FHFA still hasn't announced the 2027 conforming limits** (five
  runs) — a lender's own limit is not the conforming limit. One ⚠ item a day, fallback named.
- **`ca_cities.json` has an ACS table nobody had used** — Census ACS 2020–2024 median year built,
  value, rent and units for all 265 cities. Weeks of `stat` rows with no fetch; first use Tue Nov 17.
  **Never build a row on the owner/renter split** — tenure edges toward who lives where, and §5 wins.
- **There is still no track, template or theme finding, and Mentor must not invent one.** 146 rows
  sit in `track:untagged`; the tagged tracks read at or near 0.0%. Until a track has 4+ posts *and*
  the account has reach worth measuring, "this track works" is not a finding — say the data is thin.
  The recurring "write an extra Untagged piece" directive is an artifact of that bucket.

## 7. Standing rules for Mentor

1. Never plan a topic without running `python -m bot.seen`. His real history is ~200 posts back to
   May 2026 in `data/posts.csv`, which predates this bot. Run `--plan` clean before pushing.
2. Balance the week across the audiences in section 3 — not five buyer posts in a row. Inheritors,
   investors and the sphere are the three that keep getting one slot; give them two or more.
3. **Ratified Nov 16, 2026 — this replaces the old "a meme most days and two `quote` pieces".**
   At 3 feed items a day: **humor gets one feed slot a week, Saturday**, plus a story when one is
   free; **`quote` is one a week and rides a story.** Both registers stay in the mix per §2 — they
   stop outbidding the educational floor. The three feed slots belong to Memo's Oct 28 ask (tips,
   education, process, questionnaire, CTA). Humor keeps a feed slot on its save rate; `quote` lost
   its because it earns reach and no engagements. Rewrite this when the data changes — it is
   editorial judgment and it is Mentor's, not Scribe's.
4. **The fresh-rate piece goes on SATURDAY.** PMMS publishes Thursdays at noon ET and Scribe writes
   **two days** ahead, so Saturday's queue is written Thursday evening, after the print. If the
   print hasn't advanced, don't rerun last week's number — the brief only permits repeating a rate
   update that "carries a new weekly number." Swap in a banked topic. **Point Scribe at
   `globenewswire.com` first** (§6), then `freddiemac.gcs-web.com`, then `www.freddiemac.com`.
5. When the data contradicts this playbook, the data wins — and update this file to say so.
6. **Memo's format ask (Oct 28, 2026): "more tips, education, process, questionnaire and CTA", in a
   more luxury design.** Every day: at least one `process`, one questionnaire (`checklist`/`quiz`),
   one education piece (`tip`/`explainer`/`compare`), a clear next step on everything, and the weekly
   15-minute-call offer on Thursday as `cta_sub` on that day's client-facing feed piece. Name the
   template in the angle column. **`process` and the education piece may ride a story** — only the
   questionnaire must be in the feed — but mark which story or it gets dropped. **When a directive
   bans a template, meet the ask another way** (`quiz` for `checklist`, `cta_sub` for `cta`); never
   drop the requirement. Judge templates on saves and DMs, not likes.
7. **Agent attraction = a Spotlight series (Memo, Oct 28, 2026),** `template: spotlight`, one
   subject per post — a perk, tool, training, support line, cost line, event, or (only with written
   OK, a photo file and a consent date) an agent. **Two a week, Wednesday and Sunday, in a reel
   slot.** Rotate CONTENT_BRIEF's list, no repeat within 30 days (`spotlight-log.csv`), every fact
   from an official Epique source read the same day.
8. **One source-dependent item a day, maximum.** Give that slot to whatever has a hard same-day rule
   (the Spotlight, or the rate piece), mark it ⚠, and **name the no-fetch fallback in the row.**
   Everything else must be writable with the wall up — `ca_cities.json` sources a `stat` with no
   fetch (Realtor.com ZIP inventory, Zillow ZHVI/ZORI, C.A.R. Sept 2026 counties, ACS 2020–2024).
9. **Name the yielding row yourself, in the day heading.** The directives force an extra `stat` row
   and the five daily requirements don't fit five pieces on a Spotlight day. If Mentor doesn't
   choose, Scribe applies the brief's precedence list, which cuts humor (5th) and the Spotlight
   (4th) — that lost the Sun Nov 15 Spotlight and the Sat Nov 14 meme. **Plan the `stat` in the
   table, say which requirement yields, and say the Wed/Sun Spotlight never does.** When a piece
   exists only because an audience needs it, say in the row that it must not be cut.
10. **Check that Scribe actually ran.** Compare the latest `bot: queue <date>` commit and the newest
   `knowledge/market-notes/` file against today's date. A missing night means a near-empty
   publishing day, and it belongs in the first line of the report.
11. **Plan Tue–Sun, not Mon–Sat.** Scribe's 7:47pm PT run writes the queue for **two days later**,
   so a Mon–Sat plan starves it two nights a week and Monday is already written by Sunday's run.
