# Wifak Bank - Internal Audit Report

**Audit Subject:** Retail Loan Processing System & Credit Decision Engine  
**Report Reference:** AUD-2026-R02  
**Date of Audit:** February 10, 2026  
**Classification:** STRICTLY CONFIDENTIAL - INTERNAL USE ONLY  
**Auditor:** Compliance & Risk Management Division  

---

## 1. Executive Summary & Scope
During Q1 2026, the Internal Audit Team conducted a comprehensive review of the Retail Loan Processing System and the automated Credit Decision Engine. The objective was to assess:
* Compliance with federal credit reporting regulations.
* Data security and integrity of credit score inputs.
* The adequacy of system access controls and audit trails.
* Document retention and approval compliance for high-value loan products (loans exceeding $250,000).

The overall risk rating for the Retail Loan Processing system has been evaluated as **Medium Risk**. While the core engine performs credit calculation accurately, several procedural and control gaps were identified.

---

## 2. Key Findings & Audit Observations

### Observation 1: Inconsistent Approval Documentation for High-Value Loans
* **Risk Rating:** **High**
* **Finding:** A sample review of 50 retail loans approved in Q4 2025 exceeding $250,000 revealed that **6 loans (12%)** lacked the mandatory secondary approval signature from the Risk Committee Lead in the system files.
* **Impact:** Regulatory non-compliance and elevated credit default risk due to bypassing established secondary oversight limits.
* **Recommendation:** Update the loan origination system to programmatically block loan disbursement unless the dual-authorization signature fields are satisfied.

### Observation 2: Delayed Revocation of System Access
* **Risk Rating:** **Medium**
* **Finding:** Access logs showed that **3 departed employees** from the Loan Operations department retained active write-access to the Credit Decision Engine for up to **14 days** post-termination.
* **Impact:** Potential unauthorized modification of credit scoring rules or loan status.
* **Recommendation:** Integrate the HR termination process directly with Active Directory to enforce automatic, immediate revocation of system access upon employee departure.

### Observation 3: Inadequate Logs for Model Parameter Updates
* **Risk Rating:** **Low**
* **Finding:** Changes to variables in the credit scoring algorithm (e.g., debt-to-income limits) are logged, but the logs do not record the business justification or reference the approval ticket number.
* **Impact:** Reduced auditability and difficulty in tracing model regression issues.
* **Recommendation:** Require developers to input an approved ticket ID (Jira Reference) in the system configuration interface before any scoring parameter updates can be committed.

---

## 3. Remediation and Action Plan

| Finding | Action Plan | Owner | Target Date |
| :--- | :--- | :--- | :--- |
| **High Value Approvals** | Implement hard programmatic blocks for dual-approvals in *LoanFlow* v4.2. | VP of Loan Technology | June 30, 2026 |
| **Access Revocation** | Set up daily HR-to-IT AD sync audits and automate offboarding scripts. | IT Infrastructure Lead | May 15, 2026 |
| **Model Logs** | Add a mandatory Jira ticket field in the Credit Engine admin console. | Lead Developer | August 31, 2026 |
