# Platform comparison — list prices and facts seen in 2026

All prices are per user per month unless stated, mostly on annual billing, and
were read in July–September 2026. Only the Microsoft figures were confirmed on
the vendor's own page; the rest came through pricing trackers that cite the
vendor page (marked *secondary*). Confirm on the vendor page before quoting.

## A. CRM and sales automation

| Vendor | Entry | Upper tiers | Free tier | Integrations | Implementation | Fit | Limitation | Source |
|--------|-------|-------------|-----------|--------------|----------------|-----|------------|--------|
| HubSpot Sales Hub | Starter ~$15–20 | Professional $90; Enterprise $150 | Free core CRM | ~2,000 marketplace apps | 2–8 weeks | small–mid | cost step-up above Starter is steep | *secondary* emailvendorselection.com, docket.io |
| Salesforce Sales Cloud | Starter $25 | Enterprise $165–175; Unlimited $330–350; Agentforce 1 $550 | no | AppExchange ~5,900 apps | 6–14 weeks core; 6–12 months enterprise | mid–large | tier prices disagree across trackers; negotiated 20–40% below list | *secondary* marketbetter.ai, vendorbenchmark.com |
| Zoho CRM | Standard $14 (annual) | Ultimate $52 | up to 3 users | marketplace, count unverified | not verified | small | feature gaps at lower tiers | *secondary* zeeg.me |
| Pipedrive | Lite $14 (annual) | Ultimate $79 | 14-day trial | marketplace, count unverified | not verified | small pipeline-first teams | add-ons raise effective cost | *secondary* costbench.com |
| Dynamics 365 Sales | Professional $65 | Enterprise $105; Premium $150 | Team Member $8 | native Microsoft 365 / Power Platform | partner usually required; $25k–$500k+ | mid–large on Microsoft | Copilot for Sales is extra (~$20 add-on / $50 standalone) | **primary** microsoft.com |

## B. Connector and workflow automation

| Vendor | Entry | Upper tiers | Free tier | Integrations | Fit | Limitation | Source |
|--------|-------|-------------|-----------|--------------|-----|------------|--------|
| Zapier | Professional $19.99/mo (750 tasks) | Team $69/mo; Enterprise custom | 100 tasks/mo, 2-step | 9,000+ apps | small teams, broad coverage | per-task cost scales badly at volume | *secondary* nocode.mba, activepieces.com |
| Make | Core $9/mo (10,000 credits) | Teams $38/mo; Enterprise custom | 1,000 credits/mo | not confirmed | small–mid, visual flows | AI/code steps consume more credits | *secondary* usecarly.com |
| n8n Cloud | Starter $20/mo (2,500 executions) | Business $667/mo | community edition free (self-host ~$4–7/mo VPS) | 400+ core nodes; 1,500+ with community | technical teams | integration counts inconsistent across sources | *secondary* novelvista.com |
| n8n self-hosted | free | Business $800/mo | yes | as above | cost-sensitive technical teams | infra and engineering time not in the price | *secondary* instapods.com |
| Power Automate | Premium $15 | Process $150/bot; Hosted Process $215/bot | trial; basic flows in some M365 plans | Microsoft connector library | Microsoft 365 shops | premium connectors and AI Builder extra | **primary** microsoft.com |

## C. RPA

| Vendor | Entry | Enterprise | Free | Fit | Limitation | Source |
|--------|-------|------------|------|-----|------------|--------|
| UiPath | Automation Cloud from $25/mo | quote-based; trackers model Orchestrator $8k–20k/yr | Community Edition | large, rules-based back office | public per-seat pricing fragmented; old flat plans withdrawn | *secondary* automationatlas.io, aimultiple.com |
| Power Automate Desktop | in Premium $15 (attended) | Process $150/bot (unattended) | with some M365 plans | Microsoft shops, light RPA | same product spans connector and RPA use | **primary** microsoft.com |

## D. ERP, POS and BI

| Vendor | Entry | Upper | Free | Fit | Limitation | Source |
|--------|-------|-------|------|-----|------------|--------|
| Odoo (POS + Inventory) | ~$24.90 intro, ~$31.10 at renewal (US) | Custom ~$49 intro / ~$61 renewal | One App Free | small–mid wanting one suite | regional prices vary up to ~9×; intro rate steps up ~25% | *secondary* oec.sh, erpresearch.com |
| Power BI | Pro $14 | Premium per user $24; Fabric capacity separate | Free (no sharing) | Microsoft data stack | April 2025 price rise still in effect | **primary** microsoft.com |
| Metabase | Starter $100/mo + $6/user | Pro $575/mo + $12/user | open source self-hosted | cost-sensitive self-serve BI | base fee plus per-user, non-linear | *secondary* vendr.com |

## E. AI sales agents

| Vendor | Pricing model | Prerequisite | Limitation | Source |
|--------|---------------|--------------|------------|--------|
| Salesforce Agentforce | $2/conversation, or Flex Credits $0.10/action, or $125–150/user add-on; Agentforce 1 from $550/user | Salesforce org | model changed several times since 2024; confirm with the vendor | *secondary* magicfuse.co, getmonetizely.com |
| HubSpot Breeze | Customer Agent $0.50/resolved conversation; Prospecting Agent $1/lead; Data Agent $0.10/answer | Service Hub Pro/Enterprise seat ($90+) | headline per-outcome price excludes the mandatory seat and onboarding | *secondary* martech.org, cmswire.com |
| Microsoft Copilot for Sales | ~$20 add-on with M365 Copilot; ~$50 standalone | Dynamics 365 or M365 | moving to a credits model in 2026; verify | *secondary* velosio.com |

## Analyst views

- Gartner Magic Quadrant for Sales Force Automation Platforms, July 2025: Leaders Salesforce, Microsoft, Oracle — https://www.gartner.com/en/documents/6747034 (paywalled; read via vendor reprints).
- Forrester Wave: CRM Software, Q1 2025: Leaders Salesforce, Microsoft Dynamics 365, Pegasystems — https://www.forrester.com/blogs/a-market-on-the-cusp-of-change-decoding-the-crm-wave/ (summary).
- G2 CRM grid 2026: not resolved in this research pass; check https://www.g2.com/categories/crm directly.

## Outcome evidence to cite with the recommendation

- Microsoft 365 Copilot SMB study (Forrester TEI, Oct 2024): composite 200-employee firm, 132–353% three-year ROI, +6% revenue — https://www.microsoft.com/en-us/microsoft-365/blog/2024/10/17/microsoft-365-copilot-drove-up-to-353-roi-for-small-and-medium-businesses-new-study/ (vendor-commissioned).
- Salesforce Agentforce, Nexo: 62% case resolution, 2,600 hours saved, with real data-cleanup friction — https://www.salesforce.com/customer-stories/nexo-agentforce-implementation/ (vendor-published).
- UiPath, Bilfinger order-to-cash: 70% time saved on data input — https://www.uipath.com/resources/automation-case-studies/bilfinger-employs-software-robots (vendor-published).
- Zendesk speed-to-lead routing: response time −82%, ~55 staff-hours/week reclaimed — https://www.kixie.com/sales-blog/speed-to-lead-response-time-statistics-that-drive-conversions/ (*secondary*).
- McKinsey fresh-food replenishment ML at a 1,000+ store grocer: stock-outs down up to 80% — https://www.mckinsey.com/industries/retail/our-insights/the-secret-to-smarter-fresh-food-replenishment-machine-learning
