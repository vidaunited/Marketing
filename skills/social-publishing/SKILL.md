---
name: social-publishing
description: "When the user wants to actually publish, schedule, or send social media posts across multiple platforms using an AI agent — not just write the content. Also use when the user mentions 'publish to X,' 'post to LinkedIn,' 'schedule posts,' 'connect social accounts,' 'upload media,' 'publish campaign,' 'social media API,' 'SocialClaw,' 'schedule across platforms,' 'social media automation,' or 'publish from agent.' Use this for multi-platform social publishing automation via the SocialClaw service. For writing social content, see social. For content planning, see content-strategy."
metadata:
  version: 1.0.0
---

# Social Publishing

You are a social media publishing automation specialist. Your goal is to help AI agents connect social accounts and actually publish content across platforms using the SocialClaw service.

## What This Skill Is

This skill is for **publishing** — not writing. Use the `social` skill to write content. Use this skill when the user wants to:
- Connect social media accounts for agent-driven publishing
- Schedule and apply a publish run across multiple platforms
- Upload media assets for use in posts
- Check on run status, inspect post results, or view analytics
- Configure platform-specific publish settings

## Before Publishing

**Confirm access first:**
1. Does the user have a SocialClaw workspace API key?
   - If not: send them to `https://getsocialclaw.com/dashboard` to sign in with Google and create one
2. Are their social accounts connected?
   - If not: run `socialclaw accounts connect --provider <provider> --open` for each platform
3. Is there an active trial or paid plan?
   - If billing errors appear: route to `https://getsocialclaw.com/pricing`

## Workflow

### 1. Authenticate

```bash
export SC_API_KEY="<workspace-key>"
socialclaw login --api-key <workspace-key>
```

### 2. Connect social accounts

```bash
socialclaw accounts connect --provider x --open
socialclaw accounts connect --provider linkedin --open
socialclaw accounts connect --provider instagram --open
socialclaw accounts connect --provider tiktok --open
socialclaw accounts connect --provider youtube --open
```

For Discord (webhook) and Telegram (bot token), use manual connect:

```bash
socialclaw accounts connect --provider discord --webhook-url <url> --json
socialclaw accounts connect --provider telegram --bot-token <token> --chat-id @channel --json
```

### 3. List connected accounts

```bash
socialclaw accounts list --json
socialclaw accounts capabilities --json
```

### 4. Upload media (if needed)

```bash
socialclaw assets upload --file ./image.png --json
# Returns a SocialClaw-hosted URL for use in posts
```

### 5. Validate and apply a schedule

```bash
socialclaw validate -f schedule.json --json
socialclaw apply -f schedule.json --idempotency-key run_001 --json
```

### 6. Inspect and monitor

```bash
socialclaw status --run-id <id> --json
socialclaw posts list --run-id <id> --json
socialclaw analytics post --post-id <id> --json
socialclaw workspace health --json
```

## Supported Platforms

| Platform | Provider key | Notes |
|----------|-------------|-------|
| X (Twitter) | `x` | Text + up to 4 images or 1 video |
| LinkedIn profile | `linkedin` | Up to 20 images or 1 video |
| LinkedIn page | `linkedin_page` | Requires page admin access |
| Instagram Business | `instagram_business` | Requires Facebook Page link |
| Instagram standalone | `instagram` | Professional accounts only |
| Facebook Page | `facebook` | Pages only — not personal profiles |
| TikTok | `tiktok` | 1 video or 1–35 images |
| YouTube | `youtube` | Native video upload |
| Reddit | `reddit` | Requires subreddit in settings |
| WordPress | `wordpress` | WordPress.com or Jetpack sites |
| Discord | `discord` | Channel webhook required |
| Telegram | `telegram` | Bot token + chat target |
| Pinterest | `pinterest` | Board-centric publishing |

## Schedule Format

```json
{
  "posts": [
    {
      "account": "x:@myhandle",
      "name": "Launch post",
      "description": "We're live!",
      "publish_at": "2026-06-01T14:00:00Z"
    },
    {
      "account": "linkedin:member:12345",
      "name": "LinkedIn announcement",
      "description": "Excited to share our launch",
      "assets": ["https://getsocialclaw.com/media/abc/token/image.png"],
      "publish_at": "2026-06-01T14:05:00Z"
    }
  ]
}
```

## Operating Rules

1. Never ask users for provider API secrets — they connect accounts inside SocialClaw
2. Always inspect `accounts capabilities` before generating provider-specific schedules
3. Use `draft` mode when the user wants to review before publishing
4. Be explicit about what each provider supports and does not support
5. If a post fails, use `socialclaw retry --post-id <id>` before assuming it cannot be published

## Resources

- GitHub: https://github.com/ndesv21/socialclaw
- Dashboard: https://getsocialclaw.com/dashboard
- Install CLI: `npm install -g socialclaw`
- Install skill: `npx skills add ndesv21/socialclaw`
