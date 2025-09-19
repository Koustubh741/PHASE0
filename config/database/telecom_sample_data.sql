-- Telecom Sample Data for GRC Platform
-- Following System Architecture Diagram

-- =============================================
-- POLICIES SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO policies (id, title, description, category, status, version, effective_date, review_date, owner_id, organization_id, created_at, updated_at) VALUES
('POL-TEL-001', 'FCC Regulatory Compliance Policy', 'Comprehensive policy for FCC regulations, spectrum management, and telecommunications compliance', 'Regulatory Compliance', 'Active', '2.4', '2024-01-01', '2024-12-31', 'user-tel-001', 'org-tel-001', NOW(), NOW()),

('POL-TEL-002', 'Network Security and Cybersecurity Policy', 'Framework for network security, cybersecurity controls, and incident response', 'Information Security', 'Active', '3.1', '2024-01-15', '2024-12-31', 'user-tel-002', 'org-tel-001', NOW(), NOW()),

('POL-TEL-003', 'Customer Data Privacy Policy', 'Customer data protection and privacy policy aligned with GDPR, CCPA, and telecom regulations', 'Data Privacy', 'Active', '2.2', '2024-02-01', '2024-12-31', 'user-tel-003', 'org-tel-001', NOW(), NOW()),

('POL-TEL-004', 'Service Quality and SLA Management Policy', 'Service quality standards, SLA management, and customer experience policies', 'Service Quality', 'Active', '1.9', '2024-01-20', '2024-12-31', 'user-tel-004', 'org-tel-001', NOW(), NOW()),

('POL-TEL-005', 'Infrastructure and Network Management Policy', 'Network infrastructure management, maintenance, and disaster recovery procedures', 'Infrastructure', 'Active', '2.0', '2024-01-10', '2024-12-31', 'user-tel-005', 'org-tel-001', NOW(), NOW()),

('POL-TEL-006', 'Fraud Detection and Prevention Policy', 'Telecom fraud detection, prevention, and investigation procedures', 'Fraud Prevention', 'Active', '1.8', '2024-02-15', '2024-12-31', 'user-tel-006', 'org-tel-001', NOW(), NOW()),

('POL-TEL-007', 'Emergency Services and 911 Policy', 'Emergency services support, 911 compliance, and public safety procedures', 'Public Safety', 'Active', '1.7', '2024-01-25', '2024-12-31', 'user-tel-007', 'org-tel-001', NOW(), NOW());

-- =============================================
-- RISKS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO risks (id, title, description, category, risk_level, probability, impact, status, owner_id, organization_id, created_at, updated_at) VALUES
('RISK-TEL-001', 'Network Outage and Service Disruption Risk', 'Risk of network outages affecting customer services and emergency communications', 'Operational Risk', 'High', 0.4, 0.9, 'Active', 'user-tel-005', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-002', 'Cybersecurity Breach Risk', 'Risk of cyber attacks on telecom networks and customer data systems', 'Technology Risk', 'High', 0.6, 0.8, 'Active', 'user-tel-002', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-003', 'FCC Regulatory Violation Risk', 'Risk of FCC regulatory violations and spectrum interference issues', 'Compliance Risk', 'Medium', 0.3, 0.7, 'Active', 'user-tel-001', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-004', 'Customer Data Breach Risk', 'Risk of unauthorized access to customer data and privacy violations', 'Compliance Risk', 'High', 0.5, 0.8, 'Active', 'user-tel-003', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-005', 'Service Quality Degradation Risk', 'Risk of service quality issues affecting customer satisfaction and SLAs', 'Operational Risk', 'Medium', 0.5, 0.6, 'Active', 'user-tel-004', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-006', 'Telecom Fraud Risk', 'Risk of telecom fraud, SIM swapping, and unauthorized service usage', 'Fraud Risk', 'Medium', 0.4, 0.5, 'Active', 'user-tel-006', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-007', 'Emergency Services Failure Risk', 'Risk of 911 and emergency services failures affecting public safety', 'Public Safety Risk', 'High', 0.2, 0.9, 'Active', 'user-tel-007', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-008', 'Infrastructure Aging Risk', 'Risk of aging network infrastructure affecting service reliability', 'Infrastructure Risk', 'Medium', 0.6, 0.6, 'Active', 'user-tel-008', 'org-tel-001', NOW(), NOW()),

('RISK-TEL-009', 'Spectrum Interference Risk', 'Risk of spectrum interference and regulatory compliance issues', 'Regulatory Risk', 'Medium', 0.3, 0.5, 'Active', 'user-tel-009', 'org-tel-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE ASSESSMENTS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO compliance_assessments (id, title, description, framework, status, score, target_score, assessor_id, organization_id, created_at, updated_at) VALUES
('COMP-TEL-001', 'FCC Regulatory Compliance Assessment', 'Comprehensive assessment of FCC regulations and spectrum management compliance', 'FCC', 'Completed', 8.6, 9.0, 'user-tel-001', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-002', 'Network Security Framework Assessment', 'Evaluation of network security controls and cybersecurity framework', 'NIST CSF', 'In Progress', 7.9, 8.5, 'user-tel-002', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-003', 'Customer Data Privacy Compliance Assessment', 'Assessment of customer data privacy and GDPR/CCPA compliance', 'GDPR/CCPA', 'Completed', 8.3, 8.5, 'user-tel-003', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-004', 'Service Quality and SLA Assessment', 'Evaluation of service quality metrics and SLA compliance', 'ITIL', 'In Progress', 8.1, 8.5, 'user-tel-004', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-005', 'Emergency Services Compliance Assessment', 'Assessment of 911 and emergency services compliance', 'FCC 911', 'Completed', 8.8, 9.0, 'user-tel-007', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-006', 'Telecom Fraud Prevention Assessment', 'Evaluation of fraud detection and prevention systems', 'Fraud Prevention', 'In Progress', 7.7, 8.0, 'user-tel-006', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-007', 'Infrastructure Security Assessment', 'Assessment of network infrastructure security and resilience', 'ISO 27001', 'In Progress', 8.0, 8.5, 'user-tel-005', 'org-tel-001', NOW(), NOW()),

('COMP-TEL-008', 'Spectrum Management Compliance Assessment', 'Assessment of spectrum management and interference prevention', 'FCC Spectrum', 'Completed', 8.4, 8.5, 'user-tel-009', 'org-tel-001', NOW(), NOW());

-- =============================================
-- WORKFLOWS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO workflows (id, name, description, status, priority, assignee_id, due_date, organization_id, created_at, updated_at) VALUES
('WF-TEL-001', 'FCC Regulatory Compliance Monitoring', 'Ongoing monitoring of FCC regulatory compliance and spectrum management', 'Active', 'High', 'user-tel-001', '2024-12-31', 'org-tel-001', NOW(), NOW()),

('WF-TEL-002', 'Network Security Monitoring', 'Continuous monitoring of network security and cybersecurity threats', 'Active', 'High', 'user-tel-002', '2024-10-15', 'org-tel-001', NOW(), NOW()),

('WF-TEL-003', 'Customer Data Privacy Review', 'Regular review of customer data privacy and consent management', 'Active', 'High', 'user-tel-003', '2024-09-30', 'org-tel-001', NOW(), NOW()),

('WF-TEL-004', 'Service Quality Monitoring', 'Continuous monitoring of service quality and SLA compliance', 'Active', 'Medium', 'user-tel-004', '2024-11-30', 'org-tel-001', NOW(), NOW()),

('WF-TEL-005', 'Network Infrastructure Maintenance', 'Regular maintenance and upgrade of network infrastructure', 'Active', 'High', 'user-tel-005', '2024-12-31', 'org-tel-001', NOW(), NOW()),

('WF-TEL-006', 'Fraud Detection and Investigation', 'Continuous fraud detection and investigation of suspicious activities', 'Active', 'High', 'user-tel-006', '2024-10-31', 'org-tel-001', NOW(), NOW()),

('WF-TEL-007', 'Emergency Services Testing', 'Regular testing of 911 and emergency services functionality', 'Active', 'High', 'user-tel-007', '2024-11-15', 'org-tel-001', NOW(), NOW()),

('WF-TEL-008', 'Spectrum Interference Monitoring', 'Continuous monitoring of spectrum usage and interference prevention', 'Active', 'Medium', 'user-tel-009', '2024-09-15', 'org-tel-001', NOW(), NOW());

-- =============================================
-- AI AGENT RECORDS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO ai_agent_records (id, agent_name, agent_type, industry, status, last_activity, performance_score, organization_id, created_at, updated_at) VALUES
('AGENT-TEL-001', 'Telecom Network Monitoring Agent', 'Network Monitoring', 'Telecom', 'Active', NOW(), 0.94, 'org-tel-001', NOW(), NOW()),

('AGENT-TEL-002', 'Telecom Fraud Detection Agent', 'Fraud Detection', 'Telecom', 'Active', NOW(), 0.91, 'org-tel-001', NOW(), NOW()),

('AGENT-TEL-003', 'Telecom Compliance Agent', 'Compliance', 'Telecom', 'Active', NOW(), 0.89, 'org-tel-001', NOW(), NOW()),

('AGENT-TEL-004', 'Telecom Customer Experience Agent', 'Customer Experience', 'Telecom', 'Active', NOW(), 0.87, 'org-tel-001', NOW(), NOW()),

('AGENT-TEL-005', 'Telecom Security Agent', 'Security', 'Telecom', 'Active', NOW(), 0.92, 'org-tel-001', NOW(), NOW());

-- =============================================
-- AI AGENT ACTIVITIES SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO ai_agent_activities (id, agent_id, activity_type, description, input_data, output_data, confidence_score, execution_time_ms, organization_id, created_at) VALUES
('ACT-TEL-001', 'AGENT-TEL-001', 'Network Performance Analysis', 'Analysis of network performance metrics and service quality', '{"network_nodes": 150, "traffic_volume": 5000000, "time_period": "24h"}', '{"performance_score": 8.6, "bottlenecks": 2, "recommendations": ["Capacity upgrade", "Traffic optimization"]}', 0.94, 1800, 'org-tel-001', NOW()),

('ACT-TEL-002', 'AGENT-TEL-002', 'Fraud Pattern Detection', 'Detection of fraudulent usage patterns and suspicious activities', '{"transactions_analyzed": 100000, "fraud_indicators": 15, "time_period": "daily"}', '{"fraud_score": 2.1, "suspicious_accounts": 8, "recommendations": ["Account monitoring", "Enhanced verification"]}', 0.91, 2200, 'org-tel-001', NOW()),

('ACT-TEL-003', 'AGENT-TEL-003', 'Regulatory Compliance Check', 'Automated compliance check against FCC and telecom regulations', '{"regulations_checked": 20, "processes_reviewed": 25, "time_period": "weekly"}', '{"compliance_score": 8.6, "violations": 1, "recommendations": ["Process update", "Documentation review"]}', 0.89, 2000, 'org-tel-001', NOW()),

('ACT-TEL-004', 'AGENT-TEL-004', 'Customer Experience Analysis', 'Analysis of customer experience metrics and satisfaction scores', '{"customers_analyzed": 50000, "interactions": 100000, "time_period": "monthly"}', '{"satisfaction_score": 8.1, "issue_areas": 3, "recommendations": ["Service improvement", "Process optimization"]}', 0.87, 1600, 'org-tel-001', NOW()),

('ACT-TEL-005', 'AGENT-TEL-005', 'Security Threat Assessment', 'Assessment of cybersecurity threats and network vulnerabilities', '{"threats_analyzed": 50, "vulnerabilities": 12, "time_period": "daily"}', '{"security_score": 8.0, "critical_threats": 2, "recommendations": ["Patch management", "Enhanced monitoring"]}', 0.92, 2400, 'org-tel-001', NOW());

-- =============================================
-- RISK MITIGATION PLANS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO risk_mitigation_plans (id, risk_id, plan_name, description, status, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('MIT-TEL-001', 'RISK-TEL-001', 'Network Redundancy and Resilience Program', 'Implement network redundancy and disaster recovery capabilities', 'In Progress', 'user-tel-005', '2024-12-31', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-002', 'RISK-TEL-002', 'Advanced Cybersecurity Framework', 'Implement advanced cybersecurity controls and threat detection', 'In Progress', 'user-tel-002', '2024-11-30', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-003', 'RISK-TEL-003', 'FCC Compliance Management System', 'Establish proactive FCC compliance monitoring and management', 'In Progress', 'user-tel-001', '2024-10-31', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-004', 'RISK-TEL-004', 'Customer Data Protection Enhancement', 'Enhance customer data protection and privacy controls', 'In Progress', 'user-tel-003', '2024-12-31', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-005', 'RISK-TEL-005', 'Service Quality Improvement Initiative', 'Implement advanced service quality monitoring and improvement', 'In Progress', 'user-tel-004', '2024-11-15', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-006', 'RISK-TEL-006', 'Advanced Fraud Prevention System', 'Implement advanced fraud detection and prevention systems', 'In Progress', 'user-tel-006', '2024-10-20', 'org-tel-001', NOW(), NOW()),

('MIT-TEL-007', 'RISK-TEL-007', 'Emergency Services Redundancy Program', 'Establish redundant emergency services and 911 capabilities', 'In Progress', 'user-tel-007', '2024-11-30', 'org-tel-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE GAPS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO compliance_gaps (id, assessment_id, gap_description, severity, status, remediation_plan, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('GAP-TEL-001', 'COMP-TEL-001', 'FCC spectrum reporting system needs automation', 'Medium', 'Open', 'Implement automated FCC spectrum reporting system', 'user-tel-001', '2024-10-15', 'org-tel-001', NOW(), NOW()),

('GAP-TEL-002', 'COMP-TEL-002', 'Network security monitoring needs enhancement', 'High', 'Open', 'Implement advanced network security monitoring and threat detection', 'user-tel-002', '2024-11-30', 'org-tel-001', NOW(), NOW()),

('GAP-TEL-003', 'COMP-TEL-003', 'Customer consent management system outdated', 'Medium', 'Open', 'Update customer consent management and privacy controls', 'user-tel-003', '2024-10-31', 'org-tel-001', NOW(), NOW()),

('GAP-TEL-004', 'COMP-TEL-004', 'SLA monitoring and reporting needs automation', 'Medium', 'Open', 'Implement automated SLA monitoring and reporting system', 'user-tel-004', '2024-11-15', 'org-tel-001', NOW(), NOW()),

('GAP-TEL-005', 'COMP-TEL-006', 'Fraud detection algorithms need updating', 'High', 'Open', 'Update fraud detection algorithms and machine learning models', 'user-tel-006', '2024-10-20', 'org-tel-001', NOW(), NOW()),

('GAP-TEL-006', 'COMP-TEL-007', 'Network infrastructure documentation incomplete', 'Medium', 'Open', 'Complete network infrastructure documentation and asset management', 'user-tel-005', '2024-11-10', 'org-tel-001', NOW(), NOW());

-- =============================================
-- WORKFLOW TASKS SAMPLE DATA (Telecom Domain)
-- =============================================

INSERT INTO workflow_tasks (id, workflow_id, task_name, description, status, assignee_id, due_date, priority, organization_id, created_at, updated_at) VALUES
('TASK-TEL-001', 'WF-TEL-001', 'FCC Regulatory Report Preparation', 'Prepare and submit quarterly FCC regulatory reports', 'In Progress', 'user-tel-001', '2024-09-30', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-002', 'WF-TEL-002', 'Network Security Threat Assessment', 'Complete network security threat assessment and vulnerability scan', 'Pending', 'user-tel-002', '2024-09-20', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-003', 'WF-TEL-003', 'Customer Privacy Impact Assessment', 'Complete privacy impact assessment for new services', 'In Progress', 'user-tel-003', '2024-09-25', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-004', 'WF-TEL-004', 'Service Quality Metrics Review', 'Review service quality metrics and SLA performance', 'Pending', 'user-tel-004', '2024-09-18', 'Medium', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-005', 'WF-TEL-005', 'Network Infrastructure Upgrade', 'Complete network infrastructure upgrade and capacity expansion', 'In Progress', 'user-tel-005', '2024-09-28', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-006', 'WF-TEL-006', 'Fraud Investigation Report', 'Complete investigation of suspected fraud cases', 'Pending', 'user-tel-006', '2024-10-05', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-007', 'WF-TEL-007', 'Emergency Services Test Execution', 'Execute emergency services functionality test', 'In Progress', 'user-tel-007', '2024-09-22', 'High', 'org-tel-001', NOW(), NOW()),

('TASK-TEL-008', 'WF-TEL-008', 'Spectrum Interference Analysis', 'Complete spectrum interference analysis and mitigation', 'Pending', 'user-tel-009', '2024-09-15', 'Medium', 'org-tel-001', NOW(), NOW());

-- =============================================
-- SAMPLE DATA SUMMARY (Telecom Domain)
-- =============================================
-- Policies: 7 Telecom-specific policies
-- Risks: 9 Telecom domain risks
-- Compliance Assessments: 8 Telecom assessments
-- Workflows: 8 Telecom workflows
-- AI Agent Records: 5 Telecom agents
-- AI Agent Activities: 5 recent activities
-- Risk Mitigation Plans: 7 plans
-- Compliance Gaps: 6 identified gaps
-- Workflow Tasks: 8 active tasks
-- Total Records: 67 Telecom-specific records
