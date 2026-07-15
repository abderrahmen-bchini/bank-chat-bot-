# Wifak Bank - Incident Response Plan (IRP)

**Document Reference:** SEC-IRP-007  
**Effective Date:** May 1, 2026  
**Version:** 4.0  
**Owner:** Information Security & DevOps Teams  

---

## 1. Objectives and Scope
This plan defines the procedures, roles, and communication channels for identifying, containing, resolving, and learning from security and operational incidents at Wifak Bank. The scope covers all production infrastructure, client-facing services (Online Banking, APIs, Mobile App), and internal databases.

---

## 2. Incident Classification & Severity Levels

| Severity | Definition | Target Resolution | Escalation Path |
| :--- | :--- | :--- | :--- |
| **Severity 1 (S1) - Critical** | Core service down (e.g. mobile app offline, database corruption, active security breach). Customer transactions blocked. | **< 2 Hours** | Alert Dev Lead (15 mins), VP Engineering (30 mins), CTO/CISO (45 mins). |
| **Severity 2 (S2) - Major** | Major feature broken (e.g. wire transfers failing but balance inquiry works, API rate limits malfunctioning). Degraded service. | **< 6 Hours** | Alert On-Call Engineer (30 mins), Dev Lead (1 hour), VP Engineering (2 hours). |
| **Severity 3 (S3) - Minor** | Minor or cosmetic issue with workaround (e.g. admin panel slow load, reporting tool export layout error). No direct customer impact. | **< 48 Hours** | Add to engineering backlog for next sprint planning. |

---

## 3. Incident Lifecycle Phases

### Phase 1: Identification & Logging
* Incidents are identified through automated monitoring (Datadog, AWS CloudWatch alerts), internal employee bug submissions, or customer support escalations.
* All identified incidents must be logged in the incident tracking system (*OpsIncident*) with a timestamp, initial severity rating, and description.

### Phase 2: Containment & Triage
* **Lockdown:** If a security breach is suspected, the Incident Commander (on-call security engineer) has the authority to revoke API keys, rotate DB credentials, or temporarily suspend specific service components.
* **Triage:** The engineering team establishes a dedicated incident bridge (Teams/Slack War Room) to diagnose the root cause.

### Phase 3: Eradication and Recovery
* **Eradication:** Engineers deploy hotfixes, roll back faulty releases, or block malicious IPs.
* **Recovery:** Systems are returned to full operation. Verification checks are run to ensure transactional data integrity and database synchronization.

### Phase 4: Lessons Learned & Post-Mortem
* For all **S1** and **S2** incidents, a formal Blameless Post-Mortem document must be written within **5 business days** of resolution.
* The document must list the timeline, root cause, impact (number of users, duration), and action items to prevent recurrence.

---

## 4. On-Call Escalation Contacts
In the event of an S1/S2 incident outside standard working hours, contact the following individuals in order:
1. **Primary On-Call DevOps Engineer:** Ext. 9011 (PagerDuty)
2. **Technical Operations Lead (Dev Lead):** Ext. 9015
3. **VP of Engineering:** Ext. 8055
4. **Chief Information Security Officer (CISO):** Ext. 8002
