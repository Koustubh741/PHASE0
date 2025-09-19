-- BFSI Sample Data for GRC Platform
-- Following System Architecture Diagram

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

INSERT INTO risk_mitigation_plans (id, risk_id, plan_name, description, status, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('MIT-BFSI-001', 'RISK-BFSI-001', 'Basel III Capital Enhancement Plan', 'Increase capital buffers and improve capital planning processes', 'In Progress', 'user-001', '2024-12-31', 'org-123', NOW(), NOW()),

('MIT-BFSI-002', 'RISK-BFSI-002', 'Portfolio Diversification Strategy', 'Reduce concentration risk through sector diversification', 'In Progress', 'user-003', '2024-11-30', 'org-123', NOW(), NOW()),

('MIT-BFSI-003', 'RISK-BFSI-003', 'Enhanced AML Monitoring Program', 'Implement advanced transaction monitoring and suspicious activity detection', 'In Progress', 'user-002', '2024-10-31', 'org-123', NOW(), NOW()),

('MIT-BFSI-004', 'RISK-BFSI-004', 'Liquidity Risk Management Framework', 'Establish comprehensive liquidity risk management and stress testing', 'In Progress', 'user-004', '2024-12-31', 'org-123', NOW(), NOW()),

('MIT-BFSI-005', 'RISK-BFSI-005', 'Cybersecurity Enhancement Program', 'Strengthen cybersecurity controls and incident response capabilities', 'In Progress', 'user-006', '2024-11-15', 'org-123', NOW(), NOW());

-- =============================================
-- COMPLIANCE GAPS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO compliance_gaps (id, assessment_id, gap_description, severity, status, remediation_plan, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('GAP-BFSI-001', 'COMP-BFSI-001', 'Liquidity Coverage Ratio below regulatory minimum', 'High', 'Open', 'Increase high-quality liquid assets and improve liquidity management', 'user-001', '2024-12-31', 'org-123', NOW(), NOW()),

('GAP-BFSI-002', 'COMP-BFSI-002', 'Customer due diligence documentation incomplete', 'Medium', 'Open', 'Complete missing documentation and implement automated verification', 'user-002', '2024-10-15', 'org-123', NOW(), NOW()),

('GAP-BFSI-003', 'COMP-BFSI-003', 'Credit risk models require validation', 'Medium', 'Open', 'Validate and recalibrate credit risk models', 'user-003', '2024-11-30', 'org-123', NOW(), NOW()),

('GAP-BFSI-004', 'COMP-BFSI-005', 'FATCA reporting system needs upgrade', 'High', 'Open', 'Upgrade reporting system and implement automated data collection', 'user-005', '2024-10-31', 'org-123', NOW(), NOW()),

('GAP-BFSI-005', 'COMP-BFSI-006', 'Cybersecurity incident response plan outdated', 'Medium', 'Open', 'Update incident response plan and conduct tabletop exercises', 'user-006', '2024-11-15', 'org-123', NOW(), NOW());

-- =============================================
-- WORKFLOW TASKS SAMPLE DATA (BFSI Domain)
-- =============================================

INSERT INTO workflow_tasks (id, workflow_id, task_name, description, status, assignee_id, due_date, priority, organization_id, created_at, updated_at) VALUES
('TASK-BFSI-001', 'WF-BFSI-001', 'Capital Adequacy Calculation', 'Calculate and validate Basel III capital adequacy ratios', 'In Progress', 'user-001', '2024-09-30', 'High', 'org-123', NOW(), NOW()),

('TASK-BFSI-002', 'WF-BFSI-002', 'Enhanced Due Diligence Review', 'Complete enhanced due diligence for high-risk customer', 'Pending', 'user-002', '2024-09-20', 'High', 'org-123', NOW(), NOW()),

('TASK-BFSI-003', 'WF-BFSI-003', 'Credit Portfolio Analysis', 'Analyze credit portfolio concentration and risk metrics', 'In Progress', 'user-003', '2024-09-25', 'Medium', 'org-123', NOW(), NOW()),

('TASK-BFSI-004', 'WF-BFSI-004', 'Suspicious Activity Investigation', 'Investigate flagged suspicious transactions', 'Pending', 'user-004', '2024-09-18', 'High', 'org-123', NOW(), NOW()),

('TASK-BFSI-005', 'WF-BFSI-005', 'Regulatory Report Preparation', 'Prepare and validate quarterly regulatory reports', 'In Progress', 'user-005', '2024-09-28', 'High', 'org-123', NOW(), NOW()),

('TASK-BFSI-006', 'WF-BFSI-006', 'Operational Risk Control Testing', 'Test effectiveness of operational risk controls', 'Pending', 'user-006', '2024-10-05', 'Medium', 'org-123', NOW(), NOW()),

('TASK-BFSI-007', 'WF-BFSI-007', 'Cybersecurity Threat Assessment', 'Assess current cybersecurity threats and vulnerabilities', 'In Progress', 'user-007', '2024-09-22', 'High', 'org-123', NOW(), NOW()),

('TASK-BFSI-008', 'WF-BFSI-008', 'Business Continuity Test Execution', 'Execute quarterly business continuity test', 'Pending', 'user-008', '2024-09-15', 'Medium', 'org-123', NOW(), NOW());

-- =============================================
-- SAMPLE DATA SUMMARY
-- =============================================
-- Policies: 5 BFSI-specific policies
-- Risks: 8 BFSI domain risks
-- Compliance Assessments: 8 BFSI assessments
-- Workflows: 8 BFSI workflows
-- AI Agent Records: 5 BFSI agents
-- AI Agent Activities: 5 recent activities
-- Risk Mitigation Plans: 5 plans
-- Compliance Gaps: 5 identified gaps
-- Workflow Tasks: 8 active tasks
-- Total Records: 57 BFSI-specific records
