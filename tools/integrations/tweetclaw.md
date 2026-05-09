# TweetClaw

OpenClaw plugin and MCP-accessible X/Twitter automation layer for tweet search, reply search, posting, follower export, monitors, webhooks, and giveaway draws.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | ✓ | Structured Xquik REST endpoints |
| MCP | ✓ | StreamableHTTP MCP server plus packaged OpenClaw plugin runtime |
| CLI | - | No standalone CLI in this repo |
| SDK | - | Use the packaged plugin path for agents |

## Authentication

- **Type**: API key for account-backed workflows, or MPP signing key for read-only pay-per-use mode
- **Install**: `openclaw plugins install @xquik/tweetclaw`
- **API key**: `openclaw config set plugins.entries.tweetclaw.config.apiKey "$XQUIK_API_KEY"`
- **MPP mode**: `openclaw config set plugins.entries.tweetclaw.config.tempoSigningKey "$MPP_SIGNING_KEY"`
- **Tool access**: `openclaw config set tools.alsoAllow '["explore", "tweetclaw"]'` when your OpenClaw profile hides external tools

TweetClaw can be installed before credentials are configured. In that state, the free `explore` tool remains available for endpoint discovery and the live tool returns setup guidance instead of failing installation.

## Common Agent Operations

### Search tweets about a topic

```text
Search tweets about AI agents from the last 7 days.
```

### Search tweet replies for objections or feedback

```text
Find replies to this product-launch tweet and summarize the top objections.
```

### Post a tweet or reply

```text
Post this launch tweet from my connected account after you show me the final text.
```

### Export followers from a target account

```text
Export followers of @openclawapp and group them by role keywords in bio.
```

### Monitor an account and route events to a webhook

```text
Create a monitor for @openclawapp and send new tweet events to this webhook.
```

### Run a giveaway draw from tweet replies

```text
Run a giveaway draw from replies to this tweet and return the winners list.
```

## When to Use

- X/Twitter research that needs live tweet search, reply analysis, or user lookup
- Approval-gated posting, replies, likes, follows, DMs, or profile actions
- Follower export, tweet extraction, and giveaway workflows
- Monitor and webhook setups for launch, support, or brand tracking

## Limitations

- MPP mode is read-only and covers 31 X/Twitter endpoints
- Posting, replies, monitors, webhooks, uploads, and other state-changing actions need an API key
- Media downloads are not MPP-eligible
- OpenClaw should show the exact payload before any visible or recurring action is approved

## Relevant Skills

- social-content
- launch-strategy
- customer-research
- directory-submissions
