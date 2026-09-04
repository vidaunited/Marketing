# Rollout and risks — evidence and checklist

## Why these projects fail

| Finding | Figure | Source |
|---------|--------|--------|
| CRM projects failing to meet objectives | widely reported 30–70%; no single verified primary source | https://www.lowcode.agency/blog/crm-implementation-failure-rate ; https://johnnygrow.com/crm/the-crm-failure-rate-is-55-percent/ (*secondary*) |
| Causes when broken down | poor adoption 43%, bad data 34%, insufficient training 22%; technology 6–10% | same (*secondary*) |
| Migrations with significant data problems | up to 40% | https://vantagepoint.io/blog/hs/why-70-of-crm-projects-fail-and-how-the-people-process-technology-framework-prevents-it (*secondary*) |
| Success factors present in successful implementations | executive buy-in 82%, user training 76%, clean data migration 71% | same (*secondary*) |
| Projects meeting objectives, excellent vs poor change management | 88% vs 13% | Prosci benchmarking — https://www.prosci.com/blog/the-correlation-between-change-management-and-project-success (*secondary*) |
| Leaders who fully trust AI agents with core processes | 6%; 43% limited tasks; 39% supervised only | HBR Analytic Services survey, 603 leaders, 2025 — via Fortune, Dec 2025 (*secondary*) |
| AI high performers that redesign workflows | 55% vs 20% of others | McKinsey, agentic workflows — https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/reinventing-marketing-workflows-with-agentic-ai |
| Companies with a mature agentic-AI governance model | ~1 in 5; skills gap the top barrier | Deloitte, State of AI in the Enterprise 2026 — https://www.deloitte.com/us/en/about/press-room/state-of-ai-report-2026.html |
| Companies reporting a negative consequence from ungoverned AI use | >50% | McKinsey, AI in the workplace 2025 — https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/superagency-in-the-workplace-empowering-people-to-unlock-ais-full-potential-at-work |

## Regulatory floor (Gulf example)

Saudi PDPL: in force 14 September 2023, full enforcement from 14 September 2024, supervised by SDAIA; automated decisions on personal data carry extra duties (impact assessment, DPO, notification for high-risk processing); penalties up to SAR 5 million, SAR 15 million for repeat offences — https://www.rsm.global/saudiarabia/insights/pdpl-compliance-saudi-arabia. Check the equivalent law for each country the data touches before choosing a hosting region.

## Phase checklist

**Before selection**
- [ ] Audit done; top defect and baseline recorded with dates
- [ ] System of record named; API/webhook access confirmed by a real call
- [ ] Transaction volume per month measured (decides per-task vs per-seat pricing)
- [ ] Data-residency and automated-decision rules listed

**Pilot (one team or site, one full cycle)**
- [ ] Stage exit criteria and owners written
- [ ] Data deduplicated and required fields filled before migration
- [ ] Human approval kept on discounts, orders, customer-facing sends
- [ ] Same eight metrics measured at the end of the cycle

**Expand**
- [ ] Pilot showed a measured gain on the target metric
- [ ] Every alert and automation has a named owner and a closed-loop action
- [ ] Role-specific training on live records; repeat at 30 days
- [ ] Export path verified (you can leave with your data)

**Run**
- [ ] 30 / 90 / 180-day reviews against the baseline
- [ ] Retire automations that moved no number
- [ ] Re-audit yearly
