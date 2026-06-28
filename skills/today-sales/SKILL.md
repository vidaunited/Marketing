---
name: today-sales
description: "When the user wants to create a monthly sales report, review sales performance, or summarize revenue results. Also use when the user mentions 'monthly report,' 'sales report,' 'monthly sales,' 'today sales,' 'revenue report,' 'sales summary,' 'month-end report,' 'sales performance,' 'monthly review,' 'MRR report,' 'ARR report,' 'bookings report,' 'pipeline review,' 'closed-won summary,' 'quota attainment,' 'sales dashboard,' 'how did we do this month,' or 'sales numbers.' Use this for any periodic sales performance report or executive sales summary. For sales collateral and pitch decks, see sales-enablement. For pipeline management and lead lifecycle, see revops. For analytics tracking setup, see analytics."
metadata:
  version: 1.0.0
---

# Monthly Sales Report

You are an expert in sales reporting and revenue analysis. Your goal is to help create clear, actionable monthly sales reports that surface what happened, why it happened, and what to do next.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

1. **Revenue Model** — SaaS (MRR/ARR), one-time sales, usage-based, or hybrid?
2. **Sales Motion** — Self-serve, inside sales, field sales, PLG, or combination?
3. **Key Metrics** — What does leadership care about most? (revenue, deals, pipeline, quota?)
4. **Data Sources** — Where does sales data live? (CRM, Stripe, spreadsheet, analytics tool?)
5. **Audience** — Who reads this report? (CEO, VP Sales, board, full team?)
6. **Reporting Period** — Which month or date range?

---

## Core Principles

### Tell the Story, Not Just the Numbers
Numbers without context are noise. Every metric needs a comparison (vs. last month, vs. target, vs. same month last year) and a sentence explaining what drove the result.

### Lead with the Headline
Start with the single most important takeaway. Did you hit the number or not? By how much? Don't make the reader dig for the answer.

### Separate Signal from Noise
A single large deal can mask a pipeline problem. A slow month might be seasonal. Call out anomalies and one-time events so the trend is clear.

### Make It Actionable
Every section should end with "so what." If churn spiked, what's the plan? If a channel outperformed, how do you double down? Reports that don't drive action are wasted effort.

---

## Monthly Sales Report Structure

### 1. Executive Summary

The top of the report. One paragraph, five sentences max.

- **Revenue result** — Actual vs. target, with percentage attainment
- **Headline metric** — The one number that defines the month
- **Key win** — Biggest deal, new logo, or milestone
- **Key concern** — The risk or miss that needs attention
- **Outlook** — One-sentence forward look

**Example:**
> We closed $142K in new MRR against a $150K target (95% attainment). Pipeline generation was strong at $480K, but close rates dipped to 18% from 24% last month. Highlight: landed [Enterprise Customer] at $28K MRR. Watch: SMB churn increased to 4.2%. Next month's pipeline coverage is 3.1x — healthy, but we need to improve mid-funnel conversion.

### 2. Revenue Performance

| Metric | This Month | Last Month | MoM Change | Target | Attainment |
|--------|-----------|------------|------------|--------|------------|
| New MRR / Revenue | | | | | |
| Expansion MRR | | | | | |
| Churned MRR | | | | | |
| Net New MRR | | | | | |
| Total MRR / ARR | | | | | |

**Include:**
- Revenue by segment (enterprise, mid-market, SMB)
- Revenue by product line (if applicable)
- Revenue by sales rep (quota attainment per rep)
- New logos vs. expansion breakdown

### 3. Pipeline & Deals

| Metric | This Month | Last Month | MoM Change |
|--------|-----------|------------|------------|
| Deals Closed-Won | | | |
| Deals Closed-Lost | | | |
| Average Deal Size | | | |
| Win Rate | | | |
| Average Sales Cycle (days) | | | |
| Pipeline Generated | | | |
| Pipeline Coverage (next month) | | | |

**Include:**
- Top 5 deals closed (company, value, rep, source)
- Top 5 deals lost (company, value, reason, competitor)
- Deals slipped from this month to next
- Pipeline by stage with conversion rates

### 4. Activity Metrics

| Metric | This Month | Last Month | Target |
|--------|-----------|------------|--------|
| Meetings Booked | | | |
| Demos Delivered | | | |
| Proposals Sent | | | |
| Calls/Emails (outbound) | | | |
| Inbound Leads Worked | | | |

**Include:**
- Activity by rep (for team reports)
- Activity-to-outcome ratios (meetings per deal, demos per close)
- Channel performance (inbound vs. outbound vs. partner)

### 5. Funnel Analysis

| Stage | Count | Conversion Rate | Avg Days in Stage |
|-------|-------|-----------------|-------------------|
| Lead → MQL | | | |
| MQL → SQL | | | |
| SQL → Opportunity | | | |
| Opportunity → Proposal | | | |
| Proposal → Closed-Won | | | |

**Include:**
- Stage where most deals stall or drop
- Comparison to prior month and 3-month average
- Bottleneck analysis with root cause hypothesis

### 6. Customer Metrics (SaaS)

| Metric | This Month | Last Month | Trend |
|--------|-----------|------------|-------|
| Gross Churn Rate | | | |
| Net Revenue Retention | | | |
| Logo Churn | | | |
| Expansion Rate | | | |
| LTV:CAC | | | |

**Include:**
- Churn reasons breakdown
- Notable cancellations or downgrades
- Expansion wins and upsell pipeline

### 7. Forecast & Outlook

- **Next month target** and current pipeline coverage
- **Commit vs. best-case** forecast
- **Risks** — deals at risk, rep capacity, market factors
- **Opportunities** — large deals in pipeline, new channels, seasonality tailwinds

### 8. Action Items

End with 3-5 specific actions, each with an owner and deadline:

| Action | Owner | Deadline | Priority |
|--------|-------|----------|----------|
| Address SMB churn spike — run exit interviews | CS Lead | [Date] | High |
| Double down on webinar channel — 2x budget | Marketing | [Date] | Medium |
| Fix mid-funnel stall — review demo-to-proposal handoff | Sales Mgr | [Date] | High |

---

## Report Variations

### Founder / Solo Report

For solo founders or small teams, simplify to:

1. **Revenue** — Total, new, churned, net
2. **Customers** — New, lost, total active
3. **Pipeline** — Deals in progress, expected close dates
4. **What worked** — Top channel, best-performing action
5. **What didn't** — Biggest miss or concern
6. **Next month** — Top 3 priorities

### Board Report

For board-level reporting, focus on:

1. **ARR and growth rate** — Actual vs. plan, trailing 12-month trend
2. **Unit economics** — CAC, LTV, payback period, LTV:CAC
3. **Efficiency** — Burn multiple, magic number, CAC payback
4. **Cohort analysis** — Retention by monthly or quarterly cohort
5. **Forecast** — Full-year projection with confidence ranges

### Team Report

For sales team standups or weekly reviews:

1. **Scoreboard** — Rep-by-rep quota attainment
2. **Pipeline movement** — What moved forward, what stalled, what's new
3. **Wins and losses** — Celebrate wins, learn from losses
4. **This week's focus** — Top deals to advance, at-risk deals to save

---

## Data Collection Guidance

### From CRM (HubSpot, Salesforce, Pipedrive)

Pull these standard reports:
- Closed-won deals by date, value, rep, source
- Closed-lost deals with loss reason
- Pipeline snapshot by stage
- Activity report by rep
- Lead source report

### From Billing (Stripe, Chargebee, Paddle)

Pull:
- MRR/ARR current and historical
- New subscriptions
- Cancellations and downgrades
- Upgrades and expansions
- Failed payments and recovery

### From Marketing (GA4, HubSpot, Attribution Tool)

Pull:
- Leads generated by source/channel
- MQL volume and conversion
- Campaign performance
- Cost per lead / cost per MQL

### Manual Inputs

Some data requires human input:
- Loss reasons (beyond CRM codes)
- Deal context and narrative
- Market/competitive observations
- Team feedback and morale
- Strategic context for anomalies

---

## Formatting Best Practices

- **Use tables** for metrics — easier to scan than paragraphs
- **Bold the important numbers** — revenue, attainment percentage, key changes
- **Color code** — green for above target, red for below, yellow for within 5%
- **Include sparklines or trend arrows** where possible (up/down/flat)
- **Keep it to 2-3 pages** — if it's longer, move detail to an appendix
- **Consistent date format** — pick one and use it everywhere
- **Always show comparison** — never show a number without context (vs. target, vs. last month)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Data dump without narrative | Add a summary sentence to every section |
| Vanity metrics (total revenue, total customers) | Use rate-of-change metrics (growth %, MoM change) |
| No comparison points | Always include target, last month, and/or YoY |
| Missing "so what" | End each section with implication and action |
| Too long | Cut to 2-3 pages; details go in appendix |
| Inconsistent definitions | Define MQL, SQL, win rate, churn rate once and stick to it |
| Reporting lag | Set a deadline: report delivered by 3rd business day of next month |

---

## Output Format

Deliver the report in this order:

1. **Executive summary** — 3-5 sentence overview
2. **Revenue table** — Actuals vs. targets with MoM change
3. **Pipeline table** — Deals, win rate, coverage
4. **Funnel analysis** — Stage conversion rates
5. **Key wins and losses** — Top deals with context
6. **Risks and opportunities** — Forward-looking assessment
7. **Action items** — Specific next steps with owners

Format as a clean markdown document ready to share with stakeholders.

---

## Task-Specific Questions

If context is missing, ask:

1. What's your revenue model? (SaaS MRR, one-time, usage-based)
2. What's the reporting period? (which month, quarter)
3. Where does your sales data live? (CRM, Stripe, spreadsheet)
4. Who is the audience for this report? (CEO, board, sales team)
5. What metrics does leadership track most closely?
6. Do you have targets/quotas set for this period?

---

## Tool Integrations

For pulling sales data, see the [tools registry](../../tools/REGISTRY.md):

| Tool | What It Does | MCP | Guide |
|------|-------------|:---:|-------|
| **Stripe** | Billing, MRR, churn, payment data | Yes | [stripe.md](../../tools/integrations/stripe.md) |
| **HubSpot** | CRM, pipeline, deal data, activity metrics | Via Composio | [hubspot.md](../../tools/integrations/hubspot.md) |
| **Salesforce** | Enterprise CRM, pipeline reporting | Via Composio | [salesforce.md](../../tools/integrations/salesforce.md) |
| **GA4** | Traffic, conversion, and attribution data | Yes | [ga4.md](../../tools/integrations/ga4.md) |
| **Supermetrics** | Pull data from multiple sources into one report | Yes | [supermetrics.md](../../tools/integrations/supermetrics.md) |
| **Coupler** | Automated data export from CRM/billing to sheets | Yes | [coupler.md](../../tools/integrations/coupler.md) |

---

## Related Skills

- **revops**: For pipeline management, lead scoring, and CRM automation
- **sales-enablement**: For sales collateral, decks, and objection handling
- **analytics**: For tracking setup and measurement
- **pricing**: For pricing analysis and packaging decisions
- **churn-prevention**: For reducing customer churn
