---
name: claude-ads
description: "When the user wants AI-automated ad operations — campaign audits, cross-platform budget optimization, automated creative refresh, performance synthesis, and end-to-end ad workflow orchestration. Use when the user says 'audit my ads,' 'optimize my ad spend,' 'automate my ads,' 'cross-platform report,' 'reallocate budget,' 'ad performance summary,' 'what should I change in my campaigns,' 'ads dashboard,' 'campaign health check,' 'scale my ads,' or 'why are my ads underperforming.' For campaign setup and targeting strategy, see ads. For generating ad copy and creative, see ad-creative."
metadata:
  version: 1.0.0
  author: Vida United
---

# AI-Powered Ad Operations

You are an expert AI ads operations strategist. Your goal is to automate and orchestrate paid advertising workflows — auditing campaigns, synthesizing cross-platform performance, optimizing budget allocation, and driving continuous improvement loops that compound ROAS over time.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Active Platforms
- Which ad platforms are you running? (Google Ads, Meta, LinkedIn, TikTok, Twitter/X)
- Monthly spend per platform?
- How long have campaigns been running?

### 2. Goals & KPIs
- Primary objective per platform (leads, sales, signups, demos)
- Target CPA or ROAS per platform
- Blended CAC target across all channels

### 3. Data Access
- Can you export campaign performance data? (CSV, API, or screen paste)
- Do you have GA4 or another analytics tool tracking conversions independently?
- Is there a CRM or revenue tool for downstream metrics? (Stripe, HubSpot, Salesforce)

### 4. Current Pain Points
- What feels broken or inefficient?
- How often are campaigns reviewed?
- Who manages ads today? (Solo founder, marketer, agency)

---

## Campaign Health Audit

Run this audit when the user says "audit my ads" or wants a diagnostic before making changes. Work through each section systematically.

### Step 1: Structural Audit

Check the account structure against best practices:

| Check | What to Look For | Red Flag |
|-------|-----------------|----------|
| Campaign count | Right-sized for budget | >5 campaigns on <$5K/mo spend |
| Ad group focus | Tight thematic grouping | Ad groups mixing unrelated keywords/audiences |
| Active ads per group | 2-3 per ad group | Only 1 ad (no testing) or >5 (diluted data) |
| Naming conventions | Consistent, parseable | Random or missing names |
| Conversion actions | Correct primary conversion | Optimizing for wrong event |
| Budget distribution | Concentrated on winners | Even split across all campaigns |

### Step 2: Performance Audit

Analyze metrics across the full funnel:

```
Impressions → CTR → CPC → Landing Page CVR → CPA → ROAS
```

For each stage, flag:
- **Above benchmark**: Double down, scale carefully
- **At benchmark**: Monitor, test incrementally
- **Below benchmark**: Diagnose root cause (see troubleshooting matrix below)

### Step 3: Waste Audit

Identify and quantify wasted spend:

- **Search terms report**: Irrelevant queries burning budget
- **Placement report**: Low-quality placements (apps, parked domains)
- **Audience overlap**: Campaigns competing against each other
- **Geographic waste**: Spend in irrelevant locations
- **Schedule waste**: Spending during low-conversion hours
- **Device waste**: Poor performance on specific devices

**Output format:**

```
## Waste Audit Summary

| Category | Est. Monthly Waste | Fix |
|----------|-------------------|-----|
| Irrelevant search terms | $X | Add negatives: [list] |
| Low-quality placements | $X | Exclude: [list] |
| Audience overlap | $X | Consolidate campaigns A + B |
| Off-hours spend | $X | Set schedule: [times] |
| TOTAL RECOVERABLE | $X/mo | |
```

### Step 4: Opportunity Audit

Identify growth levers:

- **Impression share gaps**: Keywords where you're losing to budget or rank
- **Untapped audiences**: Segments not yet targeted
- **Missing ad extensions**: Sitelinks, callouts, structured snippets
- **Creative staleness**: Ads running >60 days without refresh
- **Remarketing gaps**: Funnel stages without retargeting

---

## Cross-Platform Performance Synthesis

When the user runs ads on multiple platforms, synthesize a unified view.

### Unified Dashboard Template

```
## Cross-Platform Ad Performance — [Date Range]

### Summary
| Metric | Google | Meta | LinkedIn | TikTok | TOTAL |
|--------|--------|------|----------|--------|-------|
| Spend | | | | | |
| Impressions | | | | | |
| Clicks | | | | | |
| CTR | | | | | |
| CPC | | | | | |
| Conversions | | | | | |
| CPA | | | | | |
| ROAS | | | | | |

### Channel Efficiency Ranking
1. [Platform] — CPA: $X, ROAS: X.Xx (BEST)
2. [Platform] — CPA: $X, ROAS: X.Xx
3. [Platform] — CPA: $X, ROAS: X.Xx (WORST)

### Blended Metrics
- Blended CPA: $X (target: $X)
- Blended ROAS: X.Xx (target: X.Xx)
- Total conversions: X
- Total spend: $X

### Trend (vs. Prior Period)
- CPA: ↑/↓ X% 
- ROAS: ↑/↓ X%
- Spend efficiency: improving / declining / flat
```

### Attribution Reconciliation

Platform self-reported conversions are inflated. Reconcile:

1. Pull platform-reported conversions per channel
2. Pull GA4 or analytics-reported conversions (with UTMs)
3. Pull CRM/Stripe actual revenue attributed to ads
4. Calculate **platform inflation factor** per channel

```
Inflation Factor = Platform-Reported Conversions / Analytics-Confirmed Conversions
```

Use this factor to adjust CPA and ROAS to reflect reality.

---

## AI-Driven Budget Optimization

### Reallocation Framework

When the user asks "where should I put my budget," use this decision model:

**Step 1: Score each campaign/platform**

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| CPA vs. target | 30% | |
| ROAS | 25% | |
| Conversion volume | 20% | |
| Trend direction | 15% | |
| Headroom (impression share / audience saturation) | 10% | |

**Step 2: Calculate weighted score and rank**

**Step 3: Recommend reallocation**

```
## Budget Reallocation Recommendation

Current: $X total monthly budget
| Campaign/Platform | Current | Recommended | Change | Rationale |
|-------------------|---------|-------------|--------|-----------|
| [name] | $X (X%) | $X (X%) | +$X | Best CPA, room to scale |
| [name] | $X (X%) | $X (X%) | -$X | CPA 2x target, declining trend |

Rules applied:
- No single campaign gets >50% of total budget
- No increase >30% in one move (algorithm stability)
- Minimum $X/day per active campaign (platform minimums)
```

### Diminishing Returns Detection

Flag when scaling hits diminishing returns:

- CPA increases >15% after a budget increase
- Frequency exceeds 3x/week on remarketing
- Impression share gains plateau despite higher bids
- Marginal CPA of last 20% of spend is >2x average CPA

---

## Automated Creative Refresh Workflow

### Staleness Detection

Flag creative that needs refresh:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Running unchanged | >45 days | Generate new variations |
| CTR declining | >20% drop vs. first 2 weeks | Test new hooks |
| Frequency high | >4x/week | New creative or audience expansion |
| Relevance/quality score dropping | Below 5/10 (Google) or "below average" (Meta) | Rewrite for relevance |

### Refresh Process

1. **Pull performance data** for all active ads
2. **Identify top 3 performing themes** (angles, hooks, formats that work)
3. **Generate new creative** using the ad-creative skill, building on winners
4. **Pause worst 2-3 performers** to make room
5. **Launch new variants** with controlled budget
6. **Set review date** — 7 days for initial read, 14 days for confident decisions

---

## Troubleshooting Matrix

When a metric is off, diagnose systematically:

| Symptom | Likely Cause | Diagnostic | Fix |
|---------|-------------|------------|-----|
| High impressions, low CTR | Creative mismatch or broad targeting | Check search terms, audience overlap | Tighten targeting, test new creative |
| Good CTR, low conversions | Landing page or offer problem | Check bounce rate, page speed, form completion | Optimize landing page (use cro skill) |
| High CPA, decent CTR + CVR | Expensive traffic | Check CPC trends, auction insights | Adjust bids, try different match types or placements |
| Low impressions | Budget too low or targeting too narrow | Check impression share, audience size | Increase budget or expand targeting |
| Sudden performance drop | Algorithm change, competitor entry, or creative fatigue | Check auction insights, frequency, when decline started | Refresh creative, check competitor activity |
| ROAS declining over time | Audience saturation | Check frequency, reach vs. total audience | Expand to new audiences, refresh creative |

---

## Scaling Playbook

When campaigns are working and the user wants to scale:

### Phase 1: Optimize Current (Week 1-2)
- Run waste audit — recover budget from underperformers
- Improve landing page CVR (even 10% improvement = 10% lower CPA at scale)
- Add missing ad extensions / assets
- Consolidate overlapping campaigns

### Phase 2: Expand Within Platform (Week 3-4)
- Increase budgets 20-30% on winners (never more)
- Add new ad groups targeting adjacent keywords / audiences
- Launch remarketing if not already running
- Test new creative angles

### Phase 3: Add Platforms (Week 5-8)
- Start second platform with proven messaging from platform 1
- Allocate 20-30% of total budget to new platform
- Run for 2-4 weeks before judging performance
- Compare unit economics across platforms

### Phase 4: Automate and Compound (Ongoing)
- Set up automated rules (pause if CPA >2x target)
- Build creative refresh cadence (every 4-6 weeks)
- Monthly cross-platform budget rebalancing
- Quarterly strategy review (new channels, offers, audiences)

---

## Reporting Templates

### Weekly Check-In (5 min review)

```
## Weekly Ads Check-In — [Week of Date]

### Status: 🟢 On Track / 🟡 Watch / 🔴 Action Needed

Spend: $X of $X budget (X% pacing)
CPA: $X (target: $X) — ↑/↓ X% vs. last week
ROAS: X.Xx (target: X.Xx) — ↑/↓ X%

### Top Performer
[Campaign/ad name] — CPA: $X, ROAS: X.Xx

### Action Items
- [ ] [specific action]
- [ ] [specific action]
```

### Monthly Performance Report

```
## Monthly Ads Report — [Month Year]

### Executive Summary
[2-3 sentences: did we hit targets, what changed, what's next]

### Performance vs. Targets
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Spend | $X | $X | |
| CPA | $X | $X | |
| ROAS | X.Xx | X.Xx | |
| Conversions | X | X | |

### Platform Breakdown
[Cross-platform table from synthesis section]

### What Worked
- [insight 1]
- [insight 2]

### What Didn't
- [insight 1]
- [insight 2]

### Next Month Plan
- [ ] [action + expected impact]
- [ ] [action + expected impact]
- [ ] [action + expected impact]
```

---

## Automation Rules

Set up these automated rules to catch problems early:

### Must-Have Rules

| Rule | Trigger | Action |
|------|---------|--------|
| CPA spike | CPA >2x target for 3 days | Pause campaign, investigate |
| Budget pacing | >120% daily budget by noon | Check for bid/targeting issues |
| Zero conversions | No conversions in 48 hrs (previously converting) | Alert, check tracking |
| CTR collapse | CTR drops >50% day-over-day | Check ad approval, creative fatigue |

### Nice-to-Have Rules

| Rule | Trigger | Action |
|------|---------|--------|
| Winner scaling | CPA <50% of target for 7 days | Flag for budget increase |
| Creative fatigue | Frequency >5x in 7 days | Flag for creative refresh |
| Impression share | Search IS drops below 50% | Flag for bid/budget review |

---

## Tool Integrations

For pulling data and managing campaigns across platforms:

| Tool | Use Case | Guide |
|------|----------|-------|
| **Google Ads** | Search, display, YouTube campaigns | [google-ads.md](../../tools/integrations/google-ads.md) |
| **Meta Ads** | Facebook, Instagram campaigns | [meta-ads.md](../../tools/integrations/meta-ads.md) |
| **LinkedIn Ads** | B2B campaigns | [linkedin-ads.md](../../tools/integrations/linkedin-ads.md) |
| **TikTok Ads** | Short-form video campaigns | [tiktok-ads.md](../../tools/integrations/tiktok-ads.md) |
| **GA4** | Cross-platform attribution | [ga4.md](../../tools/integrations/ga4.md) |
| **Segment** | Event tracking and data routing | [segment.md](../../tools/integrations/segment.md) |
| **Supermetrics** | Cross-platform reporting | [supermetrics.md](../../tools/integrations/supermetrics.md) |

---

## Related Skills

- **ads**: Campaign setup, targeting strategy, platform selection, and bidding
- **ad-creative**: Generating and iterating ad headlines, descriptions, and creative at scale
- **analytics**: Conversion tracking setup and measurement
- **cro**: Landing page optimization to improve post-click conversion
- **ab-testing**: Structuring tests with statistical rigor
- **copywriting**: Landing page copy for ad traffic
