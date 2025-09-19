-- =============================================
-- BFSI SAMPLE DATA - CORE GRC AGENTS ONLY
-- =============================================
-- This file contains sample data for BFSI domain focusing on core GRC:
-- - Compliance Agent (Basel III, KYC, Regulatory Reporting)
-- - Risk Assessment Agent (Credit, Market, Operational, Liquidity Risk)
-- - Regulatory Reporting Agent (Basel III, SOX, GDPR reporting)

-- =============================================
-- POLICIES SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO policies (id, title, description, category, status, version, effective_date, review_date, owner_id, organization_id, created_at, updated_at) VALUES
('POL-BFSI-001', 'Basel III Capital Requirements Policy', 'Comprehensive policy for Basel III capital adequacy, leverage ratio, and liquidity requirements for BFSI operations', 'Capital Management', 'Active', '2.1', '2024-01-01', '2024-12-31', 'user-001', 'org-123', NOW(), NOW()),

('POL-BFSI-002', 'KYC Customer Due Diligence Policy', 'Know Your Customer procedures for customer onboarding and ongoing monitoring', 'Compliance', 'Active', '3.0', '2024-01-15', '2024-12-31', 'user-002', 'org-123', NOW(), NOW()),

('POL-BFSI-003', 'Credit Risk Management Policy', 'Framework for credit risk assessment, monitoring, and mitigation in BFSI lending operations', 'Risk Management', 'Active', '1.8', '2024-02-01', '2024-12-31', 'user-003', 'org-123', NOW(), NOW()),

('POL-BFSI-004', 'Operational Risk Management Policy', 'Guidelines for identifying, assessing, and managing operational risks in banking operations', 'Risk Management', 'Active', '2.2', '2024-01-20', '2024-12-31', 'user-004', 'org-123', NOW(), NOW()),

('POL-BFSI-005', 'Regulatory Reporting Policy', 'Procedures for regulatory reporting and compliance documentation', 'Compliance', 'Active', '1.5', '2024-01-10', '2024-12-31', 'user-005', 'org-123', NOW(), NOW());

-- =============================================
-- RISKS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO risks (id, title, description, category, risk_level, probability, impact, status, owner_id, organization_id, created_at, updated_at) VALUES
('RISK-BFSI-001', 'Basel III Non-Compliance Risk', 'Risk of failing to meet Basel III capital adequacy requirements leading to regulatory penalties', 'Compliance Risk', 'High', 0.3, 0.9, 'Active', 'user-001', 'org-123', NOW(), NOW()),

('RISK-BFSI-002', 'Credit Portfolio Concentration Risk', 'High concentration of credit exposure in technology sector increasing portfolio vulnerability', 'Credit Risk', 'Medium', 0.6, 0.7, 'Active', 'user-003', 'org-123', NOW(), NOW()),

('RISK-BFSI-003', 'KYC Compliance Risk', 'Risk of failing to meet Know Your Customer requirements leading to regulatory sanctions', 'Compliance Risk', 'Medium', 0.4, 0.6, 'Active', 'user-002', 'org-123', NOW(), NOW()),

('RISK-BFSI-004', 'Liquidity Shortfall Risk', 'Insufficient liquid assets to meet short-term obligations during stress scenarios', 'Liquidity Risk', 'Medium', 0.5, 0.6, 'Active', 'user-004', 'org-123', NOW(), NOW()),

('RISK-BFSI-005', 'Cybersecurity Breach Risk', 'Risk of cyber attacks compromising customer data and banking systems', 'Operational Risk', 'High', 0.7, 0.8, 'Active', 'user-006', 'org-123', NOW(), NOW()),

('RISK-BFSI-006', 'Interest Rate Risk', 'Exposure to adverse movements in interest rates affecting net interest margin', 'Market Risk', 'Medium', 0.8, 0.5, 'Active', 'user-007', 'org-123', NOW(), NOW()),

('RISK-BFSI-007', 'Operational Risk', 'Risk of operational failures leading to financial losses and reputational damage', 'Operational Risk', 'Medium', 0.6, 0.7, 'Active', 'user-008', 'org-123', NOW(), NOW()),

('RISK-BFSI-008', 'Regulatory Change Risk', 'Risk of new regulations requiring significant system and process changes', 'Compliance Risk', 'Medium', 0.7, 0.6, 'Active', 'user-009', 'org-123', NOW(), NOW());

-- =============================================
-- COMPLIANCE ASSESSMENTS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO compliance_assessments (id, title, description, framework, status, score, target_score, assessor_id, organization_id, created_at, updated_at) VALUES
('COMP-BFSI-001', 'Basel III Capital Adequacy Assessment', 'Comprehensive assessment of capital adequacy ratios and Basel III compliance', 'Basel III', 'In Progress', 7.2, 9.0, 'user-001', 'org-123', NOW(), NOW()),

('COMP-BFSI-002', 'KYC Program Assessment', 'Evaluation of Know Your Customer program effectiveness', 'KYC', 'Completed', 8.5, 9.0, 'user-002', 'org-123', NOW(), NOW()),

('COMP-BFSI-003', 'Credit Risk Management Assessment', 'Assessment of credit risk management framework and processes', 'Basel III', 'In Progress', 6.8, 8.5, 'user-003', 'org-123', NOW(), NOW()),

('COMP-BFSI-004', 'Operational Risk Assessment', 'Evaluation of operational risk management and control environment', 'Basel III', 'Completed', 7.9, 8.0, 'user-004', 'org-123', NOW(), NOW()),

('COMP-BFSI-005', 'Regulatory Reporting Assessment', 'Assessment of regulatory reporting compliance and accuracy', 'Basel III', 'In Progress', 6.5, 8.0, 'user-005', 'org-123', NOW(), NOW()),

('COMP-BFSI-006', 'Cybersecurity Compliance Assessment', 'Evaluation of cybersecurity controls and incident response capabilities', 'NIST CSF', 'In Progress', 7.1, 8.5, 'user-006', 'org-123', NOW(), NOW()),

('COMP-BFSI-007', 'Data Privacy Compliance Assessment', 'Assessment of data protection and privacy compliance', 'GDPR/CCPA', 'Completed', 8.2, 8.5, 'user-007', 'org-123', NOW(), NOW()),

('COMP-BFSI-008', 'Business Continuity Assessment', 'Evaluation of business continuity and disaster recovery capabilities', 'ISO 22301', 'In Progress', 6.9, 8.0, 'user-008', 'org-123', NOW(), NOW());

-- =============================================
-- WORKFLOWS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO workflows (id, name, description, status, priority, assignee_id, due_date, organization_id, created_at, updated_at) VALUES
('WF-BFSI-001', 'Basel III Capital Planning Workflow', 'Annual capital planning and stress testing workflow for Basel III compliance', 'Active', 'High', 'user-001', '2024-12-31', 'org-123', NOW(), NOW()),

('WF-BFSI-002', 'Customer Onboarding KYC Workflow', 'Customer due diligence workflow for customer onboarding', 'Active', 'High', 'user-002', '2024-10-15', 'org-123', NOW(), NOW()),

('WF-BFSI-003', 'Credit Risk Review Workflow', 'Quarterly credit portfolio review and risk assessment workflow', 'Active', 'Medium', 'user-003', '2024-09-30', 'org-123', NOW(), NOW()),

('WF-BFSI-004', 'Regulatory Reporting Workflow', 'Monthly and quarterly regulatory reporting preparation and submission', 'Active', 'High', 'user-004', '2024-12-31', 'org-123', NOW(), NOW()),

('WF-BFSI-005', 'Compliance Monitoring Workflow', 'Ongoing compliance monitoring and assessment workflow', 'Active', 'High', 'user-005', '2024-10-31', 'org-123', NOW(), NOW()),

('WF-BFSI-006', 'Operational Risk Assessment Workflow', 'Annual operational risk assessment and control testing workflow', 'Active', 'Medium', 'user-006', '2024-11-30', 'org-123', NOW(), NOW()),

('WF-BFSI-007', 'Cybersecurity Incident Response Workflow', 'Incident response and recovery workflow for cybersecurity events', 'Active', 'High', 'user-007', '2024-12-31', 'org-123', NOW(), NOW()),

('WF-BFSI-008', 'Business Continuity Testing Workflow', 'Quarterly business continuity and disaster recovery testing', 'Active', 'Medium', 'user-008', '2024-09-15', 'org-123', NOW(), NOW());

-- =============================================
-- AI AGENT RECORDS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO ai_agent_records (id, agent_name, agent_type, industry, status, last_activity, performance_score, organization_id, created_at, updated_at) VALUES
('AGENT-BFSI-001', 'BFSI Compliance Agent', 'Compliance', 'BFSI', 'Active', NOW(), 0.94, 'org-123', NOW(), NOW()),

('AGENT-BFSI-002', 'BFSI Risk Assessment Agent', 'Risk', 'BFSI', 'Active', NOW(), 0.91, 'org-123', NOW(), NOW()),

('AGENT-BFSI-003', 'BFSI Regulatory Reporting Agent', 'Reporting', 'BFSI', 'Active', NOW(), 0.87, 'org-123', NOW(), NOW());

-- =============================================
-- AI AGENT ACTIVITIES SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO ai_agent_activities (id, agent_id, activity_type, description, input_data, output_data, confidence_score, execution_time_ms, organization_id, created_at) VALUES
('ACT-BFSI-001', 'AGENT-BFSI-001', 'Compliance Analysis', 'Basel III capital adequacy assessment for Q3 2024', '{"capital_ratio": 12.5, "leverage_ratio": 4.2, "lcr": 125}', '{"compliance_status": "Compliant", "risk_level": "Low", "recommendations": ["Maintain current capital levels"]}', 0.94, 1250, 'org-123', NOW()),

('ACT-BFSI-002', 'AGENT-BFSI-002', 'Risk Assessment', 'Credit risk evaluation for corporate loan portfolio', '{"portfolio_size": 500000000, "default_rate": 2.1, "concentration": 0.15}', '{"risk_score": 6.8, "risk_rating": "Medium", "recommendations": ["Diversify portfolio", "Increase monitoring"]}', 0.91, 2100, 'org-123', NOW()),

('ACT-BFSI-003', 'AGENT-BFSI-003', 'Regulatory Reporting', 'Basel III regulatory reporting preparation and validation', '{"reporting_period": "Q3-2024", "capital_ratios": 3, "risk_metrics": 15}', '{"reports_generated": 2, "validation_status": "Passed", "recommendations": ["Submit reports by deadline"]}', 0.87, 4500, 'org-123', NOW());

-- =============================================
-- RISK MITIGATION PLANS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO risk_mitigation_plans (id, risk_id, plan_name, description, status, owner_id, target_date, organization_id, created_at, updated_at) VALUES
('RMP-BFSI-001', 'RISK-BFSI-001', 'Basel III Capital Enhancement Plan', 'Strategic plan to strengthen capital position and ensure Basel III compliance', 'In Progress', 'user-001', '2024-12-31', 'org-123', NOW(), NOW()),

('RMP-BFSI-002', 'RISK-BFSI-002', 'Credit Portfolio Diversification Plan', 'Plan to reduce concentration risk through portfolio diversification', 'In Progress', 'user-003', '2024-11-30', 'org-123', NOW(), NOW()),

('RMP-BFSI-003', 'RISK-BFSI-003', 'Enhanced KYC Compliance Plan', 'Comprehensive plan to strengthen KYC compliance and monitoring capabilities', 'In Progress', 'user-002', '2024-10-31', 'org-123', NOW(), NOW()),

('RMP-BFSI-004', 'RISK-BFSI-004', 'Liquidity Risk Management Plan', 'Plan to enhance liquidity risk management and stress testing', 'In Progress', 'user-004', '2024-12-31', 'org-123', NOW(), NOW()),

('RMP-BFSI-005', 'RISK-BFSI-005', 'Cybersecurity Enhancement Plan', 'Comprehensive cybersecurity improvement and incident response plan', 'In Progress', 'user-006', '2024-12-31', 'org-123', NOW(), NOW()),

('RMP-BFSI-006', 'RISK-BFSI-006', 'Interest Rate Risk Hedging Plan', 'Plan to implement interest rate hedging strategies', 'In Progress', 'user-007', '2024-11-15', 'org-123', NOW(), NOW()),

('RMP-BFSI-007', 'RISK-BFSI-007', 'Operational Risk Control Plan', 'Comprehensive operational risk control and monitoring system upgrade', 'In Progress', 'user-008', '2024-10-31', 'org-123', NOW(), NOW()),

('RMP-BFSI-008', 'RISK-BFSI-008', 'Regulatory Change Management Plan', 'Plan to establish robust regulatory change management process', 'In Progress', 'user-009', '2024-12-31', 'org-123', NOW(), NOW());

-- =============================================
-- COMPLIANCE VIOLATIONS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO compliance_violations (id, policy_id, violation_type, description, severity, status, detected_date, resolved_date, organization_id, created_at, updated_at) VALUES
('CV-BFSI-001', 'POL-BFSI-001', 'Capital Ratio Breach', 'Tier 1 capital ratio fell below regulatory minimum during stress test', 'High', 'Resolved', '2024-08-15', '2024-09-01', 'org-123', NOW(), NOW()),

('CV-BFSI-002', 'POL-BFSI-002', 'KYC Documentation Gap', 'Incomplete customer documentation for high-risk customer onboarding', 'Medium', 'In Progress', '2024-09-10', NULL, 'org-123', NOW(), NOW()),

('CV-BFSI-003', 'POL-BFSI-003', 'Credit Limit Exceeded', 'Credit exposure exceeded approved limits for corporate client', 'Medium', 'Resolved', '2024-08-20', '2024-08-25', 'org-123', NOW(), NOW()),

('CV-BFSI-004', 'POL-BFSI-004', 'Operational Control Failure', 'Segregation of duties violation in payment processing', 'High', 'In Progress', '2024-09-05', NULL, 'org-123', NOW(), NOW()),

('CV-BFSI-005', 'POL-BFSI-005', 'Reporting Deadline Missed', 'Quarterly regulatory report submitted 2 days late', 'Low', 'Resolved', '2024-07-31', '2024-08-02', 'org-123', NOW(), NOW());

-- =============================================
-- AUDIT TRAILS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO audit_trails (id, entity_type, entity_id, action, user_id, timestamp, details, organization_id) VALUES
('AUDIT-BFSI-001', 'Policy', 'POL-BFSI-001', 'Updated', 'user-001', NOW(), 'Updated Basel III policy version to 2.1', 'org-123'),

('AUDIT-BFSI-002', 'Risk', 'RISK-BFSI-001', 'Created', 'user-001', NOW(), 'Created new Basel III compliance risk', 'org-123'),

('AUDIT-BFSI-003', 'Compliance Assessment', 'COMP-BFSI-001', 'Started', 'user-001', NOW(), 'Initiated Basel III capital adequacy assessment', 'org-123'),

('AUDIT-BFSI-004', 'Workflow', 'WF-BFSI-001', 'Assigned', 'user-001', NOW(), 'Assigned Basel III capital planning workflow', 'org-123'),

('AUDIT-BFSI-005', 'AI Agent', 'AGENT-BFSI-001', 'Activated', 'system', NOW(), 'BFSI Compliance Agent activated and ready', 'org-123'),

('AUDIT-BFSI-006', 'Risk Mitigation Plan', 'RMP-BFSI-001', 'Created', 'user-001', NOW(), 'Created Basel III capital enhancement plan', 'org-123'),

('AUDIT-BFSI-007', 'Compliance Violation', 'CV-BFSI-001', 'Resolved', 'user-001', NOW(), 'Resolved capital ratio breach violation', 'org-123'),

('AUDIT-BFSI-008', 'AI Agent Activity', 'ACT-BFSI-001', 'Completed', 'system', NOW(), 'BFSI Compliance Agent completed capital adequacy analysis', 'org-123');

-- =============================================
-- SAMPLE DATA LOADING COMPLETE
-- =============================================
-- Total Records Loaded:
-- - 5 Policies (Basel III, KYC, Credit Risk, Operational Risk, Regulatory Reporting)
-- - 8 Risks (Compliance, Credit, KYC, Liquidity, Cybersecurity, Interest Rate, Operational, Regulatory Change)
-- - 8 Compliance Assessments (Basel III, KYC, Credit Risk, Operational Risk, Regulatory Reporting, Cybersecurity, Data Privacy, Business Continuity)
-- - 8 Workflows (Capital Planning, KYC, Credit Risk Review, Regulatory Reporting, Compliance Monitoring, Operational Risk, Cybersecurity, Business Continuity)
-- - 3 AI Agents (Compliance, Risk Assessment, Regulatory Reporting)
-- - 3 AI Agent Activities (Compliance Analysis, Risk Assessment, Regulatory Reporting)
-- - 8 Risk Mitigation Plans (Capital Enhancement, Portfolio Diversification, KYC Compliance, Liquidity Risk, Cybersecurity, Interest Rate Hedging, Operational Risk Control, Regulatory Change Management)
-- - 5 Compliance Violations (Capital Ratio Breach, KYC Documentation Gap, Credit Limit Exceeded, Operational Control Failure, Reporting Deadline Missed)
-- - 8 Audit Trails (Policy Updates, Risk Creation, Assessment Initiation, Workflow Assignment, Agent Activation, Plan Creation, Violation Resolution, Activity Completion)
