-- Comprehensive Sample Data Population Script for GRC Platform
-- This script populates the database with realistic data across all industries
-- Run this script to populate the database with sample data for dashboard display

-- =============================================
-- STEP 1: Run Schema and Basic Data
-- =============================================
-- First run: database/schema.sql (creates tables and basic data)
-- This includes organizations, compliance frameworks, risk categories, policy categories

-- =============================================
-- STEP 2: Populate Users and Organizations
-- =============================================
-- Run: database/users_and_organizations_data.sql
-- This creates 7 organizations and 43 users across all industries

-- =============================================
-- STEP 3: Populate Industry-Specific Data
-- =============================================
-- Run each industry data file:

-- BFSI Industry Data
\i database/bfsi_sample_data.sql

-- Healthcare Industry Data  
\i database/healthcare_sample_data.sql

-- Manufacturing Industry Data
\i database/manufacturing_sample_data.sql

-- Telecom Industry Data
\i database/telecom_sample_data.sql

-- =============================================
-- VERIFICATION QUERIES
-- =============================================

-- Verify data population
SELECT 'Organizations' as table_name, COUNT(*) as record_count FROM organizations
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Policies', COUNT(*) FROM policies
UNION ALL
SELECT 'Risks', COUNT(*) FROM risks
UNION ALL
SELECT 'Compliance Assessments', COUNT(*) FROM compliance_assessments
UNION ALL
SELECT 'Workflows', COUNT(*) FROM workflows
UNION ALL
SELECT 'AI Agent Records', COUNT(*) FROM ai_agent_records
UNION ALL
SELECT 'AI Agent Activities', COUNT(*) FROM ai_agent_activities
UNION ALL
SELECT 'Risk Mitigation Plans', COUNT(*) FROM risk_mitigation_plans
UNION ALL
SELECT 'Compliance Gaps', COUNT(*) FROM compliance_gaps
UNION ALL
SELECT 'Workflow Tasks', COUNT(*) FROM workflow_tasks
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_logs;

-- =============================================
-- DASHBOARD DATA SUMMARY
-- =============================================

-- Expected Dashboard Metrics After Population:
-- Total Policies: 25 (BFSI: 5, Healthcare: 6, Manufacturing: 7, Telecom: 7)
-- Total Risks: 35 (BFSI: 8, Healthcare: 8, Manufacturing: 9, Telecom: 9)
-- Total Compliance Assessments: 32 (BFSI: 8, Healthcare: 8, Manufacturing: 8, Telecom: 8)
-- Total Workflows: 32 (BFSI: 8, Healthcare: 8, Manufacturing: 8, Telecom: 8)
-- Total AI Agents: 20 (BFSI: 5, Healthcare: 5, Manufacturing: 5, Telecom: 5)
-- Total Organizations: 7
-- Total Users: 43

-- =============================================
-- INDUSTRY BREAKDOWN
-- =============================================

-- BFSI (Banking, Financial Services, Insurance)
-- - Global Bank International (org-123)
-- - 10 users with banking/finance roles
-- - 5 policies (Basel III, KYC, Credit Risk, Operational Risk, Regulatory Reporting)
-- - 8 risks (Capital adequacy, credit concentration, AML, liquidity, cybersecurity)
-- - 8 compliance assessments (Basel III, KYC/AML, FATCA/CRS, NIST CSF)
-- - 8 workflows (Capital planning, customer onboarding, risk reviews)
-- - 5 AI agents (Compliance, Risk, Fraud Detection, AML, Reporting)

-- Healthcare
-- - MedTech Solutions Inc. (org-hc-001)
-- - Regional Healthcare System (org-hc-002)
-- - 13 users with healthcare roles
-- - 6 policies (HIPAA, Patient Safety, Clinical Trials, Device Security, Adverse Events, Data Governance)
-- - 8 risks (Patient data breach, device security, clinical trial compliance, patient safety)
-- - 8 compliance assessments (HIPAA, FDA 21 CFR, Joint Commission, NIST CSF, AHRQ, GDPR/CCPA, ISO 13485, CMS)
-- - 8 workflows (HIPAA monitoring, patient safety, clinical trials, device security)
-- - 5 AI agents (HIPAA Compliance, Patient Safety, Clinical Risk, Device Security, Quality Assurance)

-- Manufacturing
-- - Advanced Manufacturing Corp (org-mfg-001)
-- - Precision Manufacturing Ltd (org-mfg-002)
-- - 13 users with manufacturing roles
-- - 7 policies (ISO 9001, Environmental, Safety, Supply Chain, Product Safety, Cybersecurity, Regulatory)
-- - 9 risks (Supply chain disruption, quality failure, safety incidents, environmental compliance)
-- - 8 compliance assessments (ISO 9001, ISO 14001, OSHA, FDA 21 CFR, EPA, ISO 28000, NIST CSF, CPSC)
-- - 8 workflows (Quality audits, environmental impact, safety inspections, supplier reviews)
-- - 5 AI agents (Quality Control, Supply Chain, Safety, Environmental, Compliance)

-- Telecom
-- - TelecomConnect Networks (org-tel-001)
-- - Metro Wireless Solutions (org-tel-002)
-- - 13 users with telecom roles
-- - 7 policies (FCC Compliance, Network Security, Data Privacy, Service Quality, Infrastructure, Fraud Prevention, Emergency Services)
-- - 9 risks (Network outages, cybersecurity, FCC violations, data breaches, service quality)
-- - 8 compliance assessments (FCC, NIST CSF, GDPR/CCPA, ITIL, FCC 911, Fraud Prevention, ISO 27001, FCC Spectrum)
-- - 8 workflows (FCC monitoring, network security, privacy reviews, service quality)
-- - 5 AI agents (Network Monitoring, Fraud Detection, Compliance, Customer Experience, Security)

-- =============================================
-- NOTES
-- =============================================
-- 1. All data uses realistic industry-specific terminology and scenarios
-- 2. Risk levels, compliance scores, and performance metrics are realistic
-- 3. User roles match industry requirements and GRC responsibilities
-- 4. AI agent activities include realistic input/output data and performance scores
-- 5. Audit logs provide sample audit trail entries
-- 6. All foreign key relationships are properly maintained
-- 7. Timestamps are recent and realistic for dashboard display

-- =============================================
-- POST-POPULATION STEPS
-- =============================================
-- 1. Start all backend services
-- 2. Start frontend application
-- 3. Access dashboard at http://localhost:3000
-- 4. Dashboard should now display realistic data across all metrics
-- 5. All charts and visualizations should show meaningful data
-- 6. AI agent status should show active agents with performance metrics
