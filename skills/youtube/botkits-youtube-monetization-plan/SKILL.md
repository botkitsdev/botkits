---
name: botkits-youtube-monetization-plan
description: >-
  Use this when a YouTube channel wants a week-by-week plan to reach the
  YouTube Partner Program thresholds. It sizes the gap from the real numbers,
  checks the pace against your weekly hours, and writes one plan file with
  weekly targets, a review rule and a policy checklist. It does not promise a
  date or an income.
license: MIT
---
# YouTube monetization plan

Turn "I want to get monetized" into a plan with a pace you can check each week. The plan starts from your real numbers, says out loud when the goal is out of reach in the time you have, and ends with a short review you repeat every week.

## 1. Read the current thresholds first

The thresholds change. Open the official page before you plan and write down the date you read it:

- YouTube Partner Program overview and eligibility: https://support.google.com/youtube/answer/72851

On 28 Nov 2026 that page lists two routes. Both also need 1,000 subscribers.

| Route | Second number | Window |
| --- | --- | --- |
| Long-form | 4,000 qualified public watch hours | last 12 months |
| Shorts | 10 million qualified Shorts views | last 90 days |

Rules on the same page: Shorts watch time in the Shorts feed does not count toward the 4,000 hours. Unlisted, private and deleted videos do not count. The page also says an update to the program starts 1 Feb 2027. If the page now shows other numbers, use those and say so in the plan.

## 2. Ask for the inputs

Ask once. Do not guess numbers the user can read in YouTube Studio.

| Input | Default | Where it comes from |
| --- | --- | --- |
| Channel niche, one line | none, ask | The user |
| Subscribers today | none, ask | Studio, Analytics |
| Qualified watch hours, last 12 months | none, ask | Studio, Analytics, Advanced mode |
| Qualified Shorts views, last 90 days | 0 | Studio, Analytics |
| Hours per week the user can spend on videos | none, ask | The user |
| Uploads so far, and how long one video takes to make | none, ask | The user |
| Route | choose in step 3 | Long-form or Shorts |

## 3. Size the gap and choose a route

1. Subscriber gap = 1,000 minus subscribers today.
2. Long-form gap = 4,000 minus watch hours today.
3. Shorts gap = 10,000,000 minus Shorts views in the last 90 days.

Pick one route. Say why in one sentence. Use these rules:

- If the channel has little video yet, pick the route that matches the format the user already enjoys making. A plan fails when the maker stops.
- The Shorts route needs a very large view count in 90 days. Show that number next to the weekly pace it implies, so the user sees it.
- Do not mix both routes in one plan. A second route can wait for the review in step 6.

## 4. Check the pace

Work out the pace the plan needs, then compare it with what the user can do.

1. Weeks available. If the user gave no date, ask how many weeks they want to give this before they review the whole idea. Default: 26.
2. Needed per week = gap divided by weeks available, for subscribers and for the second number.
3. Videos per week the user can make = weekly hours divided by hours per video.
4. Needed per video = needed per week divided by videos per week.

Then state the result in plain words, in one of three forms:

- **Reachable on paper.** The needed per-video numbers are close to what the channel already gets per video. Name the channel's own median per video from Studio if the user gives it.
- **A stretch.** The needed per-video numbers are several times the channel's median. Say how many times. Offer a longer window or fewer assumptions.
- **Not in this window.** Say so. Offer the shortest window where the pace is a stretch, not a miracle.

Never write a promise such as "you will be monetized in 90 days". Write "at this pace the numbers add up in N weeks if every video reaches X". Mark every projection as an estimate from the user's inputs.

## 5. Write the plan file

Write one Markdown file called `youtube-monetization-plan.md`. Use these sections and keep each short.

1. **Numbers today.** The inputs, the date, and the threshold page you read.
2. **Route and why.** One sentence.
3. **Pace check.** The gap, weeks available, needed per week, needed per video, and which of the three results from step 4.
4. **Weekly rhythm.** Uploads per week, and one fixed day for each task: pick the topic, make, publish, review. Keep the rhythm the user can keep when they are tired.
5. **Phases.**
   - Weeks 1 to 4: test. Publish at least 4 videos with different topics or openings. The goal is to learn which one the audience picks. No growth target.
   - Weeks 5 to 12: repeat the best format. Cut the formats that sit under the channel median.
   - Week 13 on: keep the pace, and add one change at a time.
6. **Policy checklist.** Work through the official page each month: the content is original, no active Community Guidelines strike, 2-Step Verification on, advanced features turned on, an AdSense account ready, and the channel lives in a country where the program runs. Say that meeting the numbers does not give automatic entry. A review follows. On the 28 Nov 2026 page it takes about a month.
7. **After the threshold.** Only now list other income: memberships, Supers, sponsors, affiliate links, a product. Pick one to try first and say what it needs. Do not plan these before the channel passes the threshold.

## 6. Run the weekly review

At the end of each week, ask for four numbers: new subscribers, new qualified watch hours (or Shorts views), uploads published, and the best video of the week by views.

Then write three lines:

1. Pace: ahead, on track or behind, with the gap left.
2. Keep: the one format or opening that did best.
3. Change: one thing to change next week, never more than one.

If the channel is behind for 4 weeks in a row, do not add more uploads. Return to step 4 with the new numbers and say what the honest window is now.

## Limits

- It plans. It does not upload, buy ads or promise results.
- Do not suggest buying subscribers, views or watch time, trading subscriptions, or posting content the user did not make. These break the program rules.
- Watch hours from ad campaigns do not count. Say so if the user plans to run ads for views.
- Every figure comes from the user's Studio or from the official page. If you cannot open the page, say the thresholds are unchecked.
