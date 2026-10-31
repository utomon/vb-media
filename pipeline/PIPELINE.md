# Virtual Binder daily post, runbook

Scheduling runs on **Posterly** (poster.ly MCP, connector "Poster_ly"). Metricool is deprecated since Oct 31 2026: do not use it. Posts are created with a scheduled time and publish BY THEMSELVES. David reviews slides and caption in chat before any post is created; never publish without his go.

- **Phase 1 (scheduled, unattended, ~07:52 Jakarta):** research today's story, write a brief into the repo, push, and finish with a short message that works as the push notification. Do NOT build slides or touch Posterly.
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

## Game rotation (default; if no verified story for that game, take the next game with one)
Mon Pokémon, Tue One Piece, Wed Magic: The Gathering, Thu Yu-Gi-Oh!, Fri Pokémon, Sat Lorcana / Digimon / Riftbound / Union Arena / Gundam (best story), Sun app-feature post (no news, no image needed).
Check the repo `briefs/` folder for the last 14 days first (every posted story has a brief). Never repeat a story already posted or briefed.

## Phase 1: brief (scheduled run)
1. Attach the repo with add_repo (owner utomon, repo vb-media, access push) and clone it to /home/claude/vb-media if missing (one clone, generous timeout). No push access: stop and report that clearly.
2. Research. Search for TCG news for today's game from the last ~7 days (releases, product reveals, banlists, results, notable verified sales). Verify the key facts against at least two independent sources, preferring official ones. Facts only from what you verified in this run; paraphrase, never copy text.
3. Pick ONE story. If nothing verifiable and useful, make it a Sunday-style app-feature brief instead.
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
  {"type":"cta"}
 ]}
```
Limits: photocover `lines` max 2 but use 1 when `accent` is long (2 lines + accent overlaps the swipe text; always open the rendered slide), `accent` about 14 characters max, hook `lines` max 2, `chips` 2 to 3; photo `lines` max 2, `body` 2 short lines; detail `title` max 2 lines, `rows` max 5.
