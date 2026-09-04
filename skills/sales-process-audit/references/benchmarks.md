# Benchmarks behind the defect thresholds

Every threshold in SKILL.md traces to one of these. Figures marked *secondary*
were read through an aggregator rather than the publisher's own page; treat
them as directional and re-check before quoting to a client.

## Selling time and admin load

| Finding | Figure | Source |
|---------|--------|--------|
| Share of a rep's week spent selling | ~28–30% | Salesforce, *State of Sales* 6th ed. (2024); Salesforce research release 2023 — https://www.salesforce.com/news/stories/sales-research-2023/ |
| Expected time saved by sellers using AI agents | prospect research −34%, email drafting −36% | Salesforce, *State of Sales* 2026 — https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/reports/sales/salesforce-state-of-sales-report-2026.pdf |
| Reps spending >1 h/day on manual data entry | 35% (avg 5.5 h/week) | HubSpot sales research, *secondary* — https://everready.ai/13-statistics-for-crm-data-entry-automation/ |
| Leaders who believe AI reduces manual work | 81% | HubSpot, *Sales Trends Report* 2025/26 — https://offers.hubspot.com/sales-trends-report |

## Lead response

| Finding | Figure | Source |
|---------|--------|--------|
| Qualification odds, contact within 1 h vs later | ~7× | Oldroyd, "The Short Life of Online Sales Leads", HBR, 2011 — https://hbr.org/2011/03/the-short-life-of-online-sales-leads |
| Contact within 5 min vs 30 min | ~100× more likely to connect, ~21× to qualify | MIT / InsideSales Lead Response Management Study, 2007, *secondary* — https://www.teamgate.com/blog/lead-response-time-study-speed-impacts-revenue/ |
| Cross-industry average response time | ~42 h | Lead Response Management Study, *secondary* — https://www.kixie.com/sales-blog/speed-to-lead-response-time-statistics-that-drive-conversions/ |

## Data quality and forecasting

| Finding | Figure | Source |
|---------|--------|--------|
| B2B contact data decay per year | 22.5–70% by field; email ~3.6%/month | Gartner via Landbase, *secondary* — https://www.landbase.com/blog/data-decay-rate-statistics |
| CRM users who lost revenue to bad data | 37% | Validity, *State of CRM Data Management* 2025 — same aggregator |
| CRM entries less than half complete | 76% | Validity 2025, *secondary* — https://forecastio.ai/blog/sales-forecasting-accuracy-and-analysis |
| Dead or stalled deals in a typical pipeline | 20–30% | Gartner 2025, *secondary* — same |
| Typical forecast accuracy | 70–79%; only 7% reach 90%+ | Gartner, *secondary* — same |
| Forecast accuracy gain when forecasting is integrated with CRM | +32% | Salesforce research, *secondary* — same |

## Retail and inventory

| Finding | Figure | Source |
|---------|--------|--------|
| Global inventory distortion | $1.73 T/yr; out-of-stocks $1.157 T, overstocks $572 B; 6.5% of retail sales | IHL Group, September 2025 — https://www.ihlservices.com/news/analyst-corner/2025/09/retail-inventory-crisis-persists-despite-172-billion-in-improvements/ |
| ML-driven fresh replenishment | stock-outs down up to 80%, write-offs and days-on-hand down >10%, gross margin up to +9% | McKinsey, fresh-food replenishment — https://www.mckinsey.com/industries/retail/our-insights/the-secret-to-smarter-fresh-food-replenishment-machine-learning |

## Automation project failure

| Finding | Figure | Source |
|---------|--------|--------|
| CRM projects that fail to meet objectives | widely reported 30–70% depending on definition; no single verified primary | https://www.lowcode.agency/blog/crm-implementation-failure-rate ; https://johnnygrow.com/crm/the-crm-failure-rate-is-55-percent/ |
| Failure causes | poor adoption 43%, bad data 34%, insufficient training 22%; technology itself 6–10% | *secondary* — same |
| Projects meeting objectives with excellent vs poor change management | 88% vs 13% | Prosci benchmarking, *secondary* — https://www.prosci.com/blog/the-correlation-between-change-management-and-project-success |

## Cost arithmetic reminders

- Annual selling-capacity value of a recovered hour: reps × hours/week recovered × 48 × loaded hourly cost.
- Lead-response cost: monthly leads × (qualification rate at target response − current) × average deal value × 12.
- Stockout cost per line: daily unit rate × unit margin × days out; sum over lines and sites.
- Say which of the three inputs was measured and which was assumed. Label the result measured / estimated / speculative.
