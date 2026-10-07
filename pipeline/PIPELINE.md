# Virtual Binder daily post, runbook

Two phases. Never publish anything: Metricool `autoPublish` stays false, so David gets a phone notification at post time and taps to publish.

- **Phase 1 (scheduled, unattended, ~07:52 Jakarta):** research today's story, write a brief into the repo, push, and finish with a short message that works as the push notification. Do NOT build slides or touch Metricool.
- **Phase 2 (interactive, when David writes "run today's post" and attaches an image, or says "no image"):** read the brief, build the slides, upload, create the Metricool draft.

## Accounts and constants
- Metricool brand ID: 7192540, timezone Asia/Jakarta. Networks: instagram (type POST) + tiktok. X and Facebook are not connected.
- Post time: 10:00 Asia/Jakarta (if already past 09:45 when creating the draft, use tomorrow 10:00 and say so).
- App Store: https://apps.apple.com/app/id6798784324 (bios carry the link; captions say "link in bio").
- Slides 1080x1350, JPEG output. Builder: `pipeline/vbslides.py`, see spec format at the bottom.

## Game rotation (default; if no verified story for that game, take the next game with one)
Mon Pokémon, Tue One Piece, Wed Magic: The Gathering, Thu Yu-Gi-Oh!, Fri Pokémon, Sat Lorcana / Digimon / Riftbound / Union Arena / Gundam (best story), Sun app-feature post (no news, no image needed).
Check Metricool `getScheduledPosts` for the last 7 days and the repo `briefs/` folder first. Never repeat a story already posted, drafted or briefed.

## Phase 1: brief (scheduled run)
1. Attach the repo with add_repo (owner utomon, repo vb-media, access push) and clone it to /home/claude/vb-media if missing (one clone, generous timeout). No push access: stop and report that clearly.
2. Research. Search for TCG news for today's game from the last ~7 days (releases, product reveals, banlists, results, notable verified sales). Verify the key facts against at least two independent sources, preferring official ones. Facts only from what you verified in this run; paraphrase, never copy text.
3. Pick ONE story. If nothing verifiable and useful, make it a Sunday-style app-feature brief instead.
4. Write `briefs/YYYY-MM-DD.md` (Jakarta date) containing:
   - game, one-line story, the verified facts, and every source with URL;
   - what is uncertain or labeled "reported";
   - the proposed `spec.json` (slide text, 4 to 6 slides, with a `photo` slide where an image would help, image path left as `IMAGE`) in a json code block;
   - the proposed Metricool caption and TikTok title;
   - **Image to download:** the direct URL of the official page/press image that fits (publisher domain only), which slide it goes on, and the credit line.
5. Delete files in `briefs/` older than 14 days (`git rm`). Commit and push. Never put credentials in files or messages.
6. Final message (it becomes the phone notification): game, the story in one line, and "Reply with the image from <URL> and say 'run today's post'." No long text.

## Phase 2: build and draft (interactive)
1. Make sure the repo is attached (add_repo, push) and pulled; read today's `briefs/YYYY-MM-DD.md` (or the latest). Re-verify any fact that looks time-sensitive.
2. Put David's attached image in `photo` slide(s) (`image` path, `credit` = publisher). If David says "no image", build text-led slides instead.
3. Build: `python3 -I pipeline/vbslides.py spec.json out/`. Open EVERY slide image and check text fit, overlaps, cropping and numbers against the brief. Fix and rebuild until clean.
4. Upload the JPEGs to `p/<random16hex>/slide_N.jpg` in the repo, commit, push. Confirm each raw.githubusercontent.com URL returns 200 image/jpeg.
5. `createScheduledPost` for brand 7192540: `autoPublish: false`, `draft: true`, instagram + tiktok, `instagramData.type = POST`, `tiktokData.title` (under 90 chars), 10:00 Jakarta, media = raw URLs in order. Confirm with `getScheduledPosts` that the post exists and its media URLs are Metricool-hosted (static.metricool.com). Then `git rm` the `p/<id>/` folder, commit, push.
6. Report: slides preview, caption, planner link, anything to double check.

## Housekeeping
- Uploaded slide folders are deleted right after Metricool copies them. Briefs older than 14 days are deleted. David's own images are never committed.
- Git history keeps old files (about 1 MB per post as JPEG). If the repo ever nears a few hundred MB, squash history.

## Caption format
Line 1: hook with emoji (e.g. "Magic: The Gathering | Star Trek release dates 🖖"). 2 to 4 short factual lines. "Availability may vary by region." plus source credit. Soft app line: "Keep every pull organized and track what it's worth. Download Virtual Binder on the App Store (link in bio) and follow @virtualbinder.app". 4 to 6 hashtags. Under 1000 characters.

## Rules
- Facts only from sources verified in this run. Say "reported" for unconfirmed items. No prices, dates or card details from memory.
- Images: only ones David supplies or official publisher images he downloads; credit the publisher on the slide. Do not use individual card art from third-party sites.
- No lyrics, long quotes or article text. Paraphrase.
- Never publish, never enable autoPublish, never post to X or Facebook.
- Never put credentials in files or messages. Repo access comes from add_repo.

## Fallback post (no verified news, or Sunday)
App-feature post: slide 1 hook on one feature (page scan, depth-effect cards, stickers and covers, price tracking, describe-a-card search, every game on one shelf), 1 to 3 `point` slides, last slide `cta`. Features must be real, confirmed on https://apps.apple.com/us/app/virtual-binder/id6798784324.

## spec.json format
```
{"footer": "Source line shown at the bottom of each slide",
 "slides": [
  {"type":"hook","kicker":"One Piece · Release","lines":["Line one","Line two"],"big":"Big word","chips":[["Date","Label"],["Date","Label"]],"swipe":"Swipe for details"},
  {"type":"photo","kicker":"Magic · Reveal","lines":["Two","lines"],"image":"/path/to/davids_image.png","credit":"Wizards of the Coast","body":"One or two short lines"},
  {"type":"detail","kicker":"Coming Oct 23","big":"Oct 23","title":"Product name","rows":[["Label","Value"], ...up to 5]},
  {"type":"point","kicker":"Market","lines":["Two","lines"],"stat":["label","$value","up|down|flat"],"body":["short paragraph"]},
  {"type":"cta"}
 ]}
```
Limits: hook `lines` max 2, `chips` 2 to 3; photo `lines` max 2, `body` 2 short lines; detail `title` max 2 lines, `rows` max 5.
