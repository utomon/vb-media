# Virtual Binder daily post, runbook

Goal: every morning, create ONE Instagram + TikTok carousel draft in Metricool for David to approve. Never publish anything automatically. Metricool autoPublish stays false, so David gets a phone notification at post time and taps to publish.

## Accounts and constants
- Metricool brand ID: 7192540, timezone Asia/Jakarta. Networks: instagram (type POST) and tiktok. X and Facebook are not connected.
- Post time: 10:00 Asia/Jakarta, same day the task runs.
- App Store link (goes in bios, caption says "link in bio"): https://apps.apple.com/app/id6798784324
- Slide size 1080x1350. Builder: `pipeline/vbslides.py` (see spec format below).

## Game rotation (default, skip a day's game if there is no verified story, pick the next)
Mon Pokémon, Tue One Piece, Wed Magic: The Gathering, Thu Yu-Gi-Oh!, Fri Pokémon, Sat Lorcana / Digimon / Riftbound / Union Arena / Gundam (pick whichever has the best story), Sun app-feature post (no news).
Check Metricool `getScheduledPosts` for the last 7 days first. Do not repeat a story already posted or drafted.

## Steps
1. **Research.** Search for TCG news for today's game from the last ~7 days (new set releases, product announcements, banlist updates, tournament results, notable verified sales). Verify the key facts against at least two independent sources. Prefer official sources (publisher site, official announcements). Use the publisher's own dates and wording only for facts, never copy text.
2. **Choose.** One story. If nothing verifiable and useful, make a fallback app-feature post (below). Never post rumors as fact. Label unconfirmed items "Reported" and name the source in the slide footer.
3. **Spec.** Write `spec.json` for 4 to 6 slides: slide 1 `hook`, middle slides `detail` or `point`, last slide `cta`. Keep text short. Always include the footer source line, including "US release dates" when dates are US dates.
4. **Build.** `python3 -I vbslides.py spec.json out/`. Open EVERY slide image and check: no text overflow or overlap, nothing cut off, numbers match the sources. Fix the spec and rebuild until clean.
5. **Upload.** Upload each PNG to the public repo `utomon/vb-media` under `p/<random16hex>/slide_N.png` through the GitHub contents API with the token. Confirm each raw.githubusercontent.com URL returns 200 image/png.
6. **Metricool draft.** `createScheduledPost` for brand 7192540 with `autoPublish: false`, `draft: true`, providers instagram + tiktok, `instagramData.type = POST`, `tiktokData.title` (required, under 90 chars), date = today 10:00 Asia/Jakarta, media = the raw URLs in order. Then call `getScheduledPosts` for today and confirm the post exists with 4 to 6 media URLs that start with static.metricool.com (proof Metricool copied them).
7. **Clean up.** Delete the uploaded files from the repo (contents API DELETE with each file's sha) and remove the token from disk. Only do this after step 6 shows Metricool-hosted media URLs.
8. **Report.** Final message: game, story in one line, the sources, the Metricool planner link, and anything David should double check. Send the first slide image as a preview.

## Caption format
Line 1: hook with emoji (e.g. "Pokémon TCG October release dates 🗓️ (US dates)"). Then 2 to 4 short factual lines. Then "Availability may vary by region." / source credit if relevant. Then a soft app line: "Keep every pull organized and track what it's worth. Download Virtual Binder on the App Store (link in bio) and follow @virtualbinder.app". Then 4 to 6 relevant hashtags. Under 1000 characters.

## Rules
- Facts only from sources you verified in this run. Say "reported" for unconfirmed things. Do not state prices, dates or card details from memory.
- No card art, character art or product photos are fetched. Slides are text-led with the app mockups only. If David supplies images, they come with his message, not from a scheduled run.
- Do not use song lyrics, long quotes or article text. Paraphrase.
- Do not publish, do not enable autoPublish, do not post to X or Facebook.
- Never print or log the GitHub token. Delete it from disk at the end.

## Fallback post (when there is no verified news)
Use an app-feature post: slide 1 hook about one feature (page scan, depth effect cards, stickers and covers, price tracking, describe-a-card search, every game on one shelf), slide 2 to 3 `point` slides, last slide `cta`. Features must be real, taken from the App Store listing https://apps.apple.com/us/app/virtual-binder/id6798784324 (fetch it to confirm).

## spec.json format
```
{"footer": "Source line shown at the bottom of each slide",
 "slides": [
  {"type":"hook","kicker":"One Piece · Release","lines":["Line one","Line two"],"big":"Big word","chips":[["Date","Label"],["Date","Label"]],"swipe":"Swipe for details"},
  {"type":"detail","kicker":"Coming Oct 23","big":"Oct 23","title":"Product name","rows":[["Label","Value"], ...up to 5]},
  {"type":"point","kicker":"Market","lines":["Two","lines"],"stat":["label","$value","up|down|flat"],"body":["short paragraph"]},
  {"type":"cta"}
 ]}
```
Hook `lines` max 2, `chips` 2 to 3, detail `title` max 2 lines, `rows` max 5. Text is auto-uppercased where the design calls for it.
