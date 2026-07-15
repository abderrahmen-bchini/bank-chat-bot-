# Wifak Bank - Infrastructure & Architecture Overview

**Document Reference:** INF-ARC-001  
**Last Updated:** June 15, 2026  
**Version:** 3.1  
**Owner:** DevOps & Cloud Engineering Team  

---

## 1. Cloud Architecture & Deployment
Wifak Bank's digital services are deployed on a multi-region, highly available infrastructure on Amazon Web Services (AWS).
* **Primary Region:** `us-east-1` (Northern Virginia) - Handles 100% of live traffic.
* **Secondary Region:** `us-west-2` (Oregon) - Serves as an active-passive Disaster Recovery (DR) site.
* **Containerization:** All core applications and microservices are containerized using Docker and managed via Amazon Elastic Kubernetes Service (EKS).

---

## 2. Database and Data Storage
* **Core Database:** Amazon Aurora PostgreSQL (Serverless v2).
  * Data is encrypted at rest using AWS KMS (Key Management Service) with customer-managed keys.
  * Reader instances are distributed across three Availability Zones (AZs) for high availability.
* **Cache Layer:** Amazon ElastiCache for Redis is utilized to store active user sessions, API rate-limiting tokens, and query cache data.
* **Object Storage:** Amazon S3 stores raw file uploads, converted PDF statements, and nightly database backups. S3 buckets are configured with Object Lock in compliance mode for WORM (Write Once, Read Many) regulatory compliance.

---

## 3. Disaster Recovery (DR) & Backup Strategy

### 3.1 Key Metrics
* **RTO (Recovery Time Objective):** **4 Hours** - The maximum acceptable time to restore operations after a major disaster.
* **RPO (Recovery Point Objective):** **1 Hour** - The maximum acceptable data loss window measured in time.

### 3.2 Backup Execution
* **Continuous Backups:** Aurora PostgreSQL database uses continuous WAL (Write-Ahead Log) archiving to S3, enabling point-in-time recovery (PITR) down to the second.
* **Nightly Backups:** Fully automated snapshots of all persistent volumes and databases are taken every night at 02:00 UTC. Snapshots are replicated to the secondary region (`us-west-2`) and retained for a rolling **30-day period**.
* **DR Drills:** The DevOps team conducts full-scale disaster recovery simulation drills twice a year to verify that failover procedures work and meet the RTO targets.

---

## 4. Security & Network Protections
* **Data in Transit:** Enforced TLS 1.3 for all client-to-server connections. Legacy TLS 1.1 and 1.0 are disabled at the Load Balancer level.
* **VPC Setup:** Databases and core processing microservices are deployed inside private subnets with no direct route to the internet. Access is restricted using Network Access Control Lists (NACLs) and Security Groups.
* **WAF and Shield:** AWS Web Application Firewall (WAF) is configured at the CloudFront distribution to inspect incoming headers and block SQL injection, cross-site scripting (XSS), and common web exploit patterns. AWS Shield Advanced is active to mitigate DDoS threats.
