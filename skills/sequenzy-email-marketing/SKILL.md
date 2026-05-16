---
name: sequenzy-email-marketing
description: When the user wants to build, launch, or analyze lifecycle email marketing in Sequenzy, including subscriber workflows, segments, templates, campaigns, onboarding sequences, winback flows, and transactional email QA.
---

# Sequenzy Email Marketing

Use this skill to turn marketing strategy into executable Sequenzy workflows.

## Process

1. Clarify the lifecycle goal: onboarding, activation, retention, winback, launch, or transactional notification.
2. Identify the audience: list, segment, subscriber attributes, or event trigger.
3. Draft the email flow with subject lines, body copy, CTA, timing, and success metric.
4. Use Sequenzy CLI/API or dashboard to create templates, campaigns, sequences, lists, or segments.
5. Send tests before live delivery.
6. Review stats after launch: sends, opens, clicks, bounces, unsubscribes, and replies where available.

## Safety

- Inspect account and target objects before mutating anything.
- Never send or enable a live campaign without explicit approval.
- Validate recipient emails, unsubscribe expectations, and sender identity.
- Keep copy honest, specific, and human.

## Useful commands

```bash
npm install -g @sequenzy/cli@latest
sequenzy whoami
sequenzy subscribers list
sequenzy lists list
sequenzy segments list
sequenzy templates list
sequenzy campaigns list
sequenzy sequences list
sequenzy stats
```

## Examples

- Build a 4-email SaaS trial onboarding sequence.
- Create a Product Hunt launch follow-up campaign.
- Draft a churn-prevention winback flow.
- Review campaign performance and suggest the next test.
