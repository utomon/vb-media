# Virtual Binder daily post, runbook

Scheduling runs on **Posterly** (poster.ly MCP, connector "Poster_ly"). Metricool is deprecated since Oct 31 2026: do not use it. Posts are created with a scheduled time and publish BY THEMSELVES. David reviews slides and caption in chat before any post is created; never publish without his go.

- **Phase 1 (scheduled, unattended, ~07:52 Jakarta):** pick today's format and game from the rotation, research it, write a brief into the repo, push, and finish with a short message that works as the push notification. Do NOT build slides or touch Posterly.
- **Phase 2 (interactive, when David writes "run today's post" and attaches an image, or says "no image"):** read the brief, build the slides, show slides + caption + accounts + time, wait for "go", then create the posts.

## Accounts and constants (Posterly)
Workspace f67d2c70-f375-4b22-877a-59087740bd02, timezone Asia/Jakarta. One post per account (account_id, not a list):
- Facebook page "Virtual Binder": 2266
- Instagram @virtualbinder.app: 2267
- TikTok "Virtual Binder on App Store": 2268
- X @virtual_binder: 2269
- Pinterest "Virtual Binder": 2270 (default board "TCG News & Release Dates", board_id 1148699517398033264, public)
- Post time: 10:00 Asia/Jakarta. If the 10:00 slot is missed (already past 09:45 when creating the post), do NOT move it to the next day: schedule it for 19:00 Asia/Jakarta the SAME DAY and say the new time. Only if it is already past 18:30 ask David.
- App Store: https://apps.apple.com/app/id6798784324 (bios carry the link; captions say "link in bio").
- Slides 1080x1350 (4:5), JPEG output. Builder: `pipeline/vbslides.py`, see spec format at the bottom. Instagram rejects anything taller than 9:16.

## Card data API (Virtual Binder content API)
Evergreen formats (evolution lines, binder pages, rankings, Debut vs Now) take card names, images and prices from the Virtual Binder content API. Use it from the cloud environment "virtual binder content api prod" (daily task) or "Virtual Binder content (UAT)" (testing only), where CONTENT_API_TOKEN is set as a secret. Never print or commit the token. Read-only, 30 requests a minute (pace about 2.5 s apart, retry once on 429 or a connection reset).
- Base URL (default, prod): https://api.virtualbinder.app/internal/content. UAT (testing only): https://uat.virtualbinder.app/internal/content. Header: `Authorization: Bearer $CONTENT_API_TOKEN`.
- Endpoints (GET): `/cards?game=&q=&set=&number=&rarity=&illustrator=&language=&limit=&offset=`, `/cards/{id}`, `/top-by-price?game=&q=&language=&variant=&limit=`, `/sets?game=&language=`. Games: pokemon, mtg, yugioh, onepiece, digimon, lorcana, gundam, riftbound, unionarena. Languages: en, ja.
- Each card: id, game, language, name, english_name, set, collector_number, printed_total, rarity, variant, finishes, illustrator, image_url, prices.
- **Prices (these get published):** quote ONLY the `prices` entry with `is_default: true`. Say the source and `updated_at` date in the slide `note` and the caption. Never quote `price_type: "unknown"` (Yu-Gi-Oh! set prices, some are placeholders like $999.99). `condition` is always null. A default price may also appear a second time as a finish: do not count it twice.
  - USD market price: TCGplayer via TCGCSV (Pokémon, Yu-Gi-Oh!, English One Piece and Digimon, Lorcana, Gundam, Riftbound, Union Arena); Magic from Scryfall's TCGplayer feed.
  - Japanese One Piece and Digimon: Yuyu-tei shop ASKING price in JPY (`retail`, not a sold price). Quote yen, or say "shop price, about $X". `usd_amount` is our conversion when `usd_converted_from` is "JPY". Never mix shop prices and market prices in one ranking.
  - A ranking needs prices updated within 7 days. Anything older: leave it out or label the date on the slide.
  - Prod prices are fine to publish (Top 5 rankings included) under the rules above. UAT prices come from a test copy of the database: never publish them.
- **Images:** `image_url` is the stored original card-database image (hosts: cards.scryfall.io, assets.tcgdex.net, www.pokemon-card.com, images.ygoprodeck.com, tcgplayer-cdn.tcgplayer.com, product-images.tcgplayer.com, digimoncard.com, images.digimoncard.io, optcgapi.com, www.onepiece-cardgame.com, cards.lorcast.io). TCGdex URLs ending `low.png` are low resolution: use `high.png`. Lorcana images are AVIF (Pillow reads them). Download each image, open it, and check it is the right card and sharp enough at the slide size before building. Credit the source on the slide.
- **Known data problems (verify, do not trust blindly):** skip any card with no default price when the format needs one; only 9 placeholder cards (Yu-Gi-Oh!) are named "???" with no set and no price: skip any card with no set code or a "???" name, but Yu-Gi-Oh! itself is fine to use (an unfiltered search sorts by name, so "???" comes first: always filter with q, set or limit and check results). One Piece set codes are correct: a card's `id` keeps the code PRINTED on the card, while `set` is the product it was released in, so reprints and SP parallels sit in a later set (e.g. ST31-004 Luffy is an SP card in OP-17, and PRB-01/PRB-02 hold OP01 to OP09 reprints). In a post, quote the printed code (from the id) and name the set it came out in. One Piece names mix full-width and half-width characters (e.g. the D in Monkey D. Luffy): normalise when comparing. Magic prices on prod are about 1 day old (a week-old price was UAT's test copy), but keep the 7-day rule.

## Daily rotation (default): format + game
Not every day is news. Each day has a FORMAT and a game. If the format cannot be done well (no verifiable facts, no image David can supply), fall back to a news story for that game, then to the app-feature post. Never repeat a format+topic pair from the last 14 days of `briefs/`.

| Day | Format | Game |
|---|---|---|
| Mon | News | Pokémon |
| Tue | Evolution / transformation line ("swipe to evolve") | One Piece, Digimon, Yu-Gi-Oh!, MTG (rotate) |
| Wed | News | Magic: The Gathering |
| Thu | Binder page of the week ("cards that belong together", `pair` slides) | any game, rotate weekly |
| Fri | Top 5 ranking (`ranking` slide) or Debut vs Now (`pair` slide) | any game, rotate weekly |
| Sat | Story or meme: "card I regret buying" (David's own story, ask him) or "can't unsee" card-art memes | any game |
| Sun | App-feature post (no news, no image needed) | n/a |

News days keep the old game rotation logic (Thu Yu-Gi-Oh!, Sat Lorcana/Digimon/Riftbound/Union Arena/Gundam are used when a format day has nothing usable). Posterly Starter has no post cap, so an extra post on a big news day is allowed, but ask David first.

### Format rules
- **Evolution / transformation:** one line per post (e.g. a Digimon digivolution line, a Yu-Gi-Oh! fusion chain, a character's card history). Slide 1 photocover, then one `pair` or `photo` slide per stage, last slide `cta`. Card order and names must be verified against the game's official card database.
- **Binder page of the week:** 2 to 3 `pair` slides of cards whose art connects or complements each other. This is the app's home turf: the caption should say it is a binder-page idea and point to Virtual Binder.
- **Top 5 ranking:** every price needs a source and a date. Use sold data (eBay sold or a named price guide), never asking prices, put the source and date in the slide `note` and the caption. If prices cannot be verified in this run, switch to Debut vs Now. No prices from memory.
- **Debut vs Now:** first print next to latest print (or an artist's early vs recent work). Verify both with the official database.
- **Regret / meme formats:** Phase 1 only proposes the angle and asks David for his own story or the images; nothing is invented about David's purchases.
- **Images for evergreen formats:** use the Card data API above when the environment has it (image_url is the stored official card-database image). If the API or an image host is unreachable, fall back to listing the exact card names and the official URL for each image for David to download.

## Phase 1: brief (scheduled run)
1. Attach the repo with add_repo (owner utomon, repo vb-media, access push) and clone it to /home/claude/vb-media if missing (one clone, generous timeout). No push access: stop and report that clearly.
2. Check today's row in the rotation. For a news day: search for TCG news for today's game from the last ~7 days (releases, product reveals, banlists, results, notable verified sales). Verify the key facts against at least two independent sources, preferring official ones. Facts only from what you verified in this run; paraphrase, never copy text.
3. Pick ONE story or ONE format idea. If nothing verifiable and useful, make it a Sunday-style app-feature brief instead. State the format at the top of the brief.
4. Write `briefs/YYYY-MM-DD.md` (Jakarta date) containing:
   - game, one-line story, the verified facts, and every source with URL;
   - what is uncertain or labeled "reported";
   - the proposed `spec.json` (4 to 6 slides) in a json code block. **Slide 1 is ALWAYS a clickbait `photocover`** (the official image full-bleed, image path left as `IMAGE`, big punchy headline: ONE white line + ONE gradient `accent` line, e.g. "Heroines Edition" / "Vol.2 · Oct 30"; max about 14 characters per line is safe). Do NOT open with a `hook` slide and do NOT use a separate `photo` slide for the same image. With "no image", fall back to a `hook` slide. Headlines must create curiosity or urgency (reveals live, banned, drops Oct 30) while staying factual;
   - the proposed caption (Instagram/Facebook/TikTok), a short X version, and a TikTok title;
   - **Image to download:** the direct URL of the official page/press image that fits (publisher domain only), which slide it goes on, and the credit line.
5. Delete files in `briefs/` older than 14 days (`git rm`). Commit and push. Never put credentials in files or messages.
6. Final message (it becomes the phone notification): game, the story in one line, and "Reply with the image from <URL> and say 'run today's post'." No long text.

## Phase 2: build and post (interactive)
1. Make sure the repo is attached (add_repo, push) and pulled; read today's `briefs/YYYY-MM-DD.md` (or the latest, check by date, not mtime). Re-verify any fact that looks time-sensitive.
2. David's attached image goes on slide 1 as the `photocover` (use `focus`/`vfocus`/`zoom` so faces or the product are not cropped; `zoom` 1.2 with `vfocus` 0 hides text baked into the bottom of banners). Credit the publisher in the caption ("Source and image: <publisher>"). Never use a plain `hook` opener when an image exists. With "no image", use a `hook` opener and text-led slides. Small images are fine on the cover but check they are not too soft.
3. Build: `python3 -I pipeline/vbslides.py spec.json out/` (keep spec and out/ outside the repo). Open EVERY slide image and check text fit, overlaps, cropping and numbers against the brief. Fix and rebuild until clean. Send the slides to David.
4. Show David the full caption per platform, the accounts and the time, and wait for his explicit "go".
5. Upload the JPEGs to `p/<random16hex>/slide_N.jpg` in the repo, commit, push, confirm each raw.githubusercontent.com URL returns 200 image/jpeg.
6. Posterly `upload_media` with `url` = each raw URL (one call per slide, in order). Use the returned assets.poster.ly URLs as `media_urls`. Then `git rm` the `p/<id>/` folder, commit, push.
7. `validate_post` (dry run) for every account, then `create_post` with `confirm: true` for each (see below). Then `get_post` on each id and confirm the caption is NOT empty and status is scheduled.
8. After the scheduled time, `get_post` each id: all must be published. If one failed, fix and re-post that network only.
9. Report: the published links and anything to double check.

## Posterly rules (learned the hard way)
- The caption field is **`caption`**. `create_post`/`validate_post` silently accept `content` and create the post with an EMPTY caption. Always check with `get_post` after creating.
- One post per account_id. `scheduled_at` as ISO with offset, e.g. 2026-10-31T19:00:00+07:00.
- Instagram, Facebook: carousel of all slides, same caption. Never put a URL in captions; say "link in bio".
- TikTok: photo carousel of all slides as JPEG (it rejects PNG). `platform_settings`: `{"title": "<under 90 chars>", "media_type": "PHOTO", "post_mode": "auto", "privacy_level": "PUBLIC_TO_EVERYONE"}`. Use `SELF_ONLY` only for tests.
- X: max 4 images (drop the CTA slide), short caption, NO URLs (blocked). Starter allows 10 X posts a month (multi-image post = 1); call `get_x_posting_quota` first. David wants about 2 X posts a week: pick the strongest story days and ask him which if unsure.
- Pinterest: ONE pin with slide 1 only, caption as description, `platform_settings` `{"title": "...", "board_id": "1148699517398033264"}`. If boards ever list empty, the Pinterest account needs to be reconnected in Posterly.
- Media must be copied into Posterly via `upload_media` (it stores its own copy; the repo copy is then deleted).
- Writes are rate limited (20 an hour on trial; check the plan). Batch carefully: 5 uploads + 5 validates + 5 creates is already 15.
- Trial limits: 25 posts total (each platform counts), trial ends Nov 7 2026. Paid: Starter $7 + Individual API & MCP $3 = $10 a month. David upgrades himself in Posterly billing; never try to charge or upgrade.
- Trial posts and X quota reset monthly; Pinterest and Threads are covered by the plan, Threads needs a higher tier.

## Housekeeping
- Uploaded slide folders are deleted right after Posterly copies them. Briefs older than 14 days are deleted. David's own images are never committed.
- Git history keeps old files (about 1 MB per post as JPEG). If the repo ever nears a few hundred MB, squash history.

## Caption format
Line 1: hook with emoji (e.g. "Magic: The Gathering | Star Trek release dates 🖖"). 2 to 4 short factual lines. "Availability may vary by region." plus source credit. Soft app line: "Keep every pull organized and track what it's worth. Download Virtual Binder on the App Store (link in bio) and follow @virtualbinder.app". 4 to 6 hashtags. Under 1000 characters. No em dashes.

## Rules
- Facts only from sources verified in this run. Say "reported" for unconfirmed items. No prices, dates or card details from memory.
- Images: only ones David supplies or official publisher images he downloads; credit the publisher on the slide. Do not use individual card art from third-party sites.
- No lyrics, long quotes or article text. Paraphrase.
- Phase 1 (scheduled run) never creates or publishes a post. In phase 2, create posts only after David's explicit go in chat.
- Never put credentials in files or messages. Repo access comes from add_repo.

## Fallback post (no verified news, or Sunday)
App-feature post: slide 1 hook on one feature (page scan, depth-effect cards, stickers and covers, price tracking, describe-a-card search, every game on one shelf), 1 to 3 `point` slides, last slide `cta`. Features must be real, confirmed on https://apps.apple.com/us/app/virtual-binder/id6798784324.

## spec.json format
```
{"footer": "Source line shown at the bottom of each slide",
 "slides": [
  {"type":"photocover","kicker":"Magic · Star Trek","lines":["One white line"],"accent":"Gradient line","image":"/path/to/davids_image.png","swipe":"Swipe for details","focus":0.5,"vfocus":0.3},
  {"type":"hook","kicker":"One Piece · Release","lines":["Line one","Line two"],"big":"Big word","chips":[["Date","Label"],["Date","Label"]],"swipe":"Swipe for details"},
  {"type":"photo","kicker":"Magic · Reveal","lines":["Two","lines"],"image":"/path/to/davids_image.png","credit":"Wizards of the Coast","body":"One or two short lines"},
  {"type":"detail","kicker":"Coming Oct 23","big":"Oct 23","title":"Product name","rows":[["Label","Value"], ...up to 5]},
  {"type":"point","kicker":"Market","lines":["Two","lines"],"stat":["label","$value","up|down|flat"],"body":["short paragraph"]},
  {"type":"pair","kicker":"Pokémon · Pair #1","lines":["Display them","side by side"],"images":["/path/a.png","/path/b.png"],"labels":["Left tag","Right tag"],"names":["Card A","Card B"],"body":"One or two short lines","credit":"Publisher"},
  {"type":"ranking","kicker":"Top 5","lines":["Most wanted","X cards"],"rows":[["Name","Version","$123"], ...up to 5],"note":"Source and date of the prices"},
  {"type":"cta"}
 ]}
```
Limits: photocover `lines` max 2 but use 1 when `accent` is long (2 lines + accent overlaps the swipe text; always open the rendered slide), `accent` about 14 characters max, hook `lines` max 2, `chips` 2 to 3; photo `lines` max 2, `body` 2 short lines; detail `title` max 2 lines, `rows` max 5; pair `lines` max 2, `body` 1 to 2 short lines, `labels`/`names` about 18 characters each; ranking `rows` max 5, `note` one line. Missing or "PLACEHOLDER" images draw a dry-run frame.
