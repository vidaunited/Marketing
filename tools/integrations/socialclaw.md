# SocialClaw

Agent-first social media publishing backend. Manages connected social accounts per workspace and exposes a single API key for agents to schedule and publish across multiple platforms.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | ✓ | REST API v1 |
| MCP | - | Not available |
| CLI | ✓ | `npx socialclaw` |
| SDK | - | No official SDK; use REST API directly |

## Authentication

- **Type**: API Key (Bearer)
- **Header**: `Authorization: Bearer {SOCIALCLAW_API_KEY}`
- **Get key**: Create a workspace at https://getsocialclaw.com/dashboard → Settings → API Keys
- **Scope**: Key is workspace-scoped; all connected accounts under the workspace are accessible

## Supported Platforms

X (Twitter), LinkedIn Profile, LinkedIn Page, Instagram Business, Instagram (standalone), Facebook Pages, TikTok, YouTube, Reddit, WordPress, Discord, Telegram, Pinterest

## Common Agent Operations

### Validate API key

```bash
POST https://api.getsocialclaw.com/v1/keys/validate

Authorization: Bearer {key}
```

### List connected accounts

```bash
GET https://api.getsocialclaw.com/v1/accounts

Authorization: Bearer {key}
```

Returns array of accounts with `id`, `provider`, `label`, and connection status.

### Get account capabilities

```bash
GET https://api.getsocialclaw.com/v1/accounts/capabilities

Authorization: Bearer {key}
```

Returns structured capability model for each connected account (supported post types, media constraints, character limits).

### Publish a post

```bash
POST https://api.getsocialclaw.com/v1/posts/apply
Content-Type: application/json

Authorization: Bearer {key}

{
  "accounts": ["account_id_1", "account_id_2"],
  "content": "Your post text here",
  "mediaUrls": ["https://example.com/image.jpg"],
  "scheduledAt": "2026-06-01T10:00:00Z"
}
```

Omit `scheduledAt` to publish immediately.

### Validate a post before publishing

```bash
POST https://api.getsocialclaw.com/v1/posts/validate
Content-Type: application/json

Authorization: Bearer {key}

{
  "accounts": ["account_id_1"],
  "content": "Your post text",
  "mediaUrls": []
}
```

Returns per-platform validation results (character limit checks, media spec compliance).

### List scheduled/published posts

```bash
GET https://api.getsocialclaw.com/v1/posts

Authorization: Bearer {key}
```

### Upload a media asset

```bash
POST https://api.getsocialclaw.com/v1/assets/upload
Content-Type: multipart/form-data

Authorization: Bearer {key}

file={binary}
```

Returns a hosted media URL reusable across platforms.

### Check workspace health

```bash
GET https://api.getsocialclaw.com/v1/workspace/health

Authorization: Bearer {key}
```

### Preview a campaign

```bash
POST https://api.getsocialclaw.com/v1/campaigns/preview
Content-Type: application/json

Authorization: Bearer {key}

{
  "accounts": ["account_id_1", "account_id_2"],
  "content": "Campaign post text",
  "scheduledAt": "2026-06-01T10:00:00Z"
}
```

### List scheduled jobs

```bash
GET https://api.getsocialclaw.com/v1/jobs

Authorization: Bearer {key}
```

## Platform-Specific Notes

- **X**: Up to 4 images or 1 video per post; 280 character limit
- **LinkedIn Profile/Page**: Up to 20 images per post; text and native image upload supported
- **Instagram Business**: Requires professional/business account linked to a Facebook Page
- **Instagram (standalone)**: Standalone professional publishing via Instagram Login
- **TikTok**: Requires 1 video URL or 1–35 image URLs for a photo post
- **YouTube**: 1 video per post; community posts/Shorts not supported
- **Reddit**: Self posts and link posts; subreddit required; native media upload not supported
- **WordPress**: WordPress.com or Jetpack-connected sites; uploads remote media before publish
- **Facebook Pages**: Page posting only; personal profiles are not supported

## When to Use

- Publishing or scheduling posts across multiple social platforms from a single agent workflow
- Managing social media campaigns with platform-specific content variants
- Uploading and reusing media assets across platforms
- Validating posts against platform constraints before publishing
- Retrieving post history and analytics for connected accounts

## Relevant Skills

- social-media-calendar
- content-repurposing
- launch-sequence
