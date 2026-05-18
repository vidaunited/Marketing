# Truelist

Email verification and deliverability validation. Validates single emails or bulk lists, classifies each as Deliverable / Risky / Undeliverable / Unknown, and catches catch-all domains, role accounts, and spam traps before cold outreach.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | ✓ | REST API for single + bulk verification |
| MCP | - | Not available |
| CLI | - | None |
| SDK | - | Use API directly |

> Verify current API surface and field names at https://truelist.io before building against this guide.

## Authentication

- **Type**: API Key
- **Header**: `Authorization: Bearer {api_key}` (or similar — confirm in current docs)
- **Get key**: Truelist dashboard → Settings → API
- **Note**: Pay-per-email pricing; bulk discounts at volume tiers

## Common Agent Operations

### Verify a single email

```bash
POST https://api.truelist.io/v1/verify

{
  "email": "user@example.com"
}
```

Response includes classification (e.g., `deliverable`, `risky`, `undeliverable`, `unknown`), confidence score, and metadata about why (catch-all domain, role account, disposable, syntax error, etc.).

### Bulk verification (recommended for prospecting lists)

```bash
POST https://api.truelist.io/v1/lists

{
  "name": "Q2 prospecting list",
  "emails": [
    "alice@example.com",
    "bob@example.com",
    "..."
  ]
}
```

Returns a list ID. Bulk verification runs async — poll for status.

### Check bulk job status

```bash
GET https://api.truelist.io/v1/lists/{list_id}
```

When complete, response includes per-email results plus summary counts.

### Download results (CSV or JSON)

```bash
GET https://api.truelist.io/v1/lists/{list_id}/results
```

### CSV upload (alternative to API for one-off lists)

Truelist dashboard supports CSV upload + download for users who prefer no-code workflows. Results are appended as new columns indicating status per row.

## Classification Output

| Status | Meaning | What to do |
|--------|---------|-----------|
| **Deliverable** | Valid mailbox, accepts mail | Include in outreach |
| **Risky** | Catch-all domain, role account (info@, hello@), or unclear deliverability | Include cautiously; lower priority |
| **Undeliverable** | Bounces, syntax errors, disabled accounts | Exclude from outreach |
| **Unknown** | Validation couldn't complete (timeout, blocked server, etc.) | Skip or manually verify |

## API Pattern

REST + JSON. Bearer auth. Async bulk jobs with polling.

## Pricing

- Pay-per-email model; volume tiers reduce per-email cost
- Free trial credits typically available for new accounts
- Confirm current pricing at https://truelist.io/pricing

## When to Use

- **Before adding contacts to any outreach list** — non-negotiable safety step. Apollo/ZoomInfo/Hunter data is typically 60–80% accurate; Truelist catches the rest.
- Cleaning up legacy contact databases
- Maintaining sender reputation by keeping bounce rates under 2%
- Validating opt-in form submissions in real time
- Detecting catch-all domains (lower-confidence sends)
- Filtering disposable / temporary emails from product signups

## Why This Step is Non-Negotiable

Cold email reputation is built over months and destroyed in days. ISPs (Gmail, Outlook, etc.) track sender reputation through:

- **Bounce rate** — bounces over 2% triggers throttling
- **Spam complaints** — spam traps in unvalidated lists generate complaints
- **Engagement** — sending to dead mailboxes hurts engagement metrics

A single unvalidated send to a bought or scraped list can damage a domain's sending reputation for months. Validation is the single highest-leverage step before cold outreach.

## Workflow Integration

Typical prospecting flow:

1. Build initial prospect list (Apollo, Clay, ZoomInfo, Hunter, etc.)
2. Export emails to Truelist bulk verification
3. Wait for job completion (typically minutes to hours depending on size)
4. Download results
5. Filter list: keep Deliverable, include Risky cautiously, exclude Undeliverable, manually review Unknown
6. Hand cleaned list to outreach platform (Instantly, Lemlist, Outreach, etc.) — see [outreach.md](outreach.md), [instantly.md](instantly.md), [lemlist.md](lemlist.md)

## Relevant Skills

- prospecting (this skill — primary use case)
- cold-email (downstream — outreach against the validated list)
- emails (transactional email senders also benefit from validated subscriber lists)
