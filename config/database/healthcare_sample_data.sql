-- Healthcare Sample Data for GRC Platform
-- Following System Architecture Diagram

-- =============================================
-- POLICIES SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO policies (id, title, description, category, status, version, effective_date, review_date, owner_id, organization_id, created_at, updated_at) VALUES
('POL-HC-001', 'HIPAA Privacy and Security Policy', 'Comprehensive policy for protecting patient health information and ensuring HIPAA compliance', 'Information Security', 'Active', '3.2', '2024-01-01', '2024-12-31', 'user-hc-001', 'org-hc-001', NOW(), NOW()),

('POL-HC-002', 'Patient Safety and Quality Policy', 'Framework for patient safety protocols, incident reporting, and quality improvement', 'Patient Safety', 'Active', '2.1', '2024-01-15', '2024-12-31', 'user-hc-002', 'org-hc-001', NOW(), NOW()),

('POL-HC-003', 'Clinical Trial Management Policy', 'Guidelines for conducting clinical trials in compliance with FDA regulations', 'Clinical Research', 'Active', '1.8', '2024-02-01', '2024-12-31', 'user-hc-003', 'org-hc-001', NOW(), NOW()),

('POL-HC-004', 'Medical Device Security Policy', 'Security protocols for connected medical devices and IoT healthcare systems', 'Technology Risk', 'Active', '2.0', '2024-01-20', '2024-12-31', 'user-hc-004', 'org-hc-001', NOW(), NOW()),

('POL-HC-005', 'Adverse Event Reporting Policy', 'Procedures for reporting and managing adverse events and medical errors', 'Risk Management', 'Active', '1.9', '2024-01-10', '2024-12-31', 'user-hc-005', 'org-hc-001', NOW(), NOW()),

('POL-HC-006', 'Data Governance and Analytics Policy', 'Framework for healthcare data governance, analytics, and research compliance', 'Data Management', 'Active', '1.7', '2024-02-15', '2024-12-31', 'user-hc-006', 'org-hc-001', NOW(), NOW());

-- =============================================
-- RISKS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO risks (id, title, description, category, risk_level, probability, impact, status, owner_id, organization_id, created_at, updated_at) VALUES
('RISK-HC-001', 'Patient Data Breach Risk', 'Risk of unauthorized access to patient health information leading to HIPAA violations', 'Compliance Risk', 'High', 0.4, 0.9, 'Active', 'user-hc-001', 'org-hc-001', NOW(), NOW()),

('RISK-HC-002', 'Medical Device Cybersecurity Risk', 'Risk of cyber attacks on connected medical devices compromising patient safety', 'Technology Risk', 'High', 0.6, 0.8, 'Active', 'user-hc-004', 'org-hc-001', NOW(), NOW()),

('RISK-HC-003', 'Clinical Trial Non-Compliance Risk', 'Risk of failing to meet FDA clinical trial regulations and Good Clinical Practice', 'Compliance Risk', 'Medium', 0.3, 0.7, 'Active', 'user-hc-003', 'org-hc-001', NOW(), NOW()),

('RISK-HC-004', 'Patient Safety Incident Risk', 'Risk of medical errors and adverse events affecting patient outcomes', 'Operational Risk', 'Medium', 0.5, 0.8, 'Active', 'user-hc-002', 'org-hc-001', NOW(), NOW()),

('RISK-HC-005', 'Regulatory Change Risk', 'Risk of new healthcare regulations requiring system and process changes', 'Compliance Risk', 'Medium', 0.7, 0.6, 'Active', 'user-hc-007', 'org-hc-001', NOW(), NOW()),

('RISK-HC-006', 'Supply Chain Disruption Risk', 'Risk of medical supply shortages affecting patient care delivery', 'Operational Risk', 'Medium', 0.4, 0.7, 'Active', 'user-hc-008', 'org-hc-001', NOW(), NOW()),

('RISK-HC-007', 'Quality Assurance Failure Risk', 'Risk of quality control failures in clinical processes and outcomes', 'Operational Risk', 'Medium', 0.3, 0.6, 'Active', 'user-hc-009', 'org-hc-001', NOW(), NOW()),

('RISK-HC-008', 'Research Data Integrity Risk', 'Risk of data integrity issues in clinical research and analytics', 'Technology Risk', 'Medium', 0.4, 0.5, 'Active', 'user-hc-006', 'org-hc-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE ASSESSMENTS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO compliance_assessments (id, title, description, framework, status, score, target_score, assessor_id, organization_id, created_at, updated_at) VALUES
('COMP-HC-001', 'HIPAA Privacy Rule Assessment', 'Comprehensive assessment of HIPAA Privacy Rule compliance and patient data protection', 'HIPAA', 'Completed', 8.7, 9.0, 'user-hc-001', 'org-hc-001', NOW(), NOW()),

('COMP-HC-002', 'FDA Clinical Trial Compliance Assessment', 'Evaluation of clinical trial processes and FDA 21 CFR Part 11 compliance', 'FDA 21 CFR', 'In Progress', 7.8, 9.0, 'user-hc-003', 'org-hc-001', NOW(), NOW()),

('COMP-HC-003', 'Joint Commission Standards Assessment', 'Assessment of Joint Commission accreditation standards and quality measures', 'Joint Commission', 'Completed', 8.2, 8.5, 'user-hc-002', 'org-hc-001', NOW(), NOW()),

('COMP-HC-004', 'Medical Device Security Assessment', 'Evaluation of connected medical device security and cybersecurity controls', 'NIST CSF', 'In Progress', 7.5, 8.5, 'user-hc-004', 'org-hc-001', NOW(), NOW()),

('COMP-HC-005', 'Patient Safety Culture Assessment', 'Assessment of patient safety culture and incident reporting processes', 'AHRQ', 'Completed', 8.0, 8.0, 'user-hc-005', 'org-hc-001', NOW(), NOW()),

('COMP-HC-006', 'Healthcare Data Analytics Compliance', 'Evaluation of healthcare data analytics and research compliance', 'GDPR/CCPA', 'In Progress', 7.2, 8.0, 'user-hc-006', 'org-hc-001', NOW(), NOW()),

('COMP-HC-007', 'Quality Management System Assessment', 'Assessment of ISO 13485 quality management system for medical devices', 'ISO 13485', 'In Progress', 7.9, 8.5, 'user-hc-007', 'org-hc-001', NOW(), NOW()),

('COMP-HC-008', 'Emergency Preparedness Assessment', 'Evaluation of emergency preparedness and disaster recovery capabilities', 'CMS', 'Completed', 8.4, 8.5, 'user-hc-008', 'org-hc-001', NOW(), NOW());

-- =============================================
-- WORKFLOWS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO workflows (id, name, description, status, priority, assignee_id, due_date, organization_id, created_at, updated_at) VALUES
('WF-HC-001', 'HIPAA Compliance Monitoring Workflow', 'Ongoing monitoring and assessment of HIPAA compliance across all systems', 'Active', 'High', 'user-hc-001', '2024-12-31', 'org-hc-001', NOW(), NOW()),

('WF-HC-002', 'Patient Safety Incident Investigation', 'Investigation and root cause analysis of patient safety incidents', 'Active', 'High', 'user-hc-002', '2024-10-15', 'org-hc-001', NOW(), NOW()),

('WF-HC-003', 'Clinical Trial Protocol Review', 'Review and approval of clinical trial protocols and informed consent', 'Active', 'High', 'user-hc-003', '2024-09-30', 'org-hc-001', NOW(), NOW()),

('WF-HC-004', 'Medical Device Security Assessment', 'Regular security assessment of connected medical devices', 'Active', 'High', 'user-hc-004', '2024-11-30', 'org-hc-001', NOW(), NOW()),

('WF-HC-005', 'Adverse Event Reporting Workflow', 'Standardized adverse event reporting and regulatory notification', 'Active', 'High', 'user-hc-005', '2024-12-31', 'org-hc-001', NOW(), NOW()),

('WF-HC-006', 'Healthcare Data Analytics Review', 'Review of healthcare data analytics for research and quality improvement', 'Active', 'Medium', 'user-hc-006', '2024-10-31', 'org-hc-001', NOW(), NOW()),

('WF-HC-007', 'Quality Assurance Audit Workflow', 'Regular quality assurance audits and process improvement', 'Active', 'Medium', 'user-hc-007', '2024-11-15', 'org-hc-001', NOW(), NOW()),

('WF-HC-008', 'Emergency Preparedness Testing', 'Regular testing of emergency preparedness and disaster recovery plans', 'Active', 'Medium', 'user-hc-008', '2024-09-15', 'org-hc-001', NOW(), NOW());

-- =============================================
-- AI AGENT RECORDS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO ai_agent_records (id, agent_name, agent_type, industry, status, last_activity, performance_score, organization_id, created_at, updated_at) VALUES
('AGENT-HC-001', 'Healthcare HIPAA Compliance Agent', 'Compliance', 'Healthcare', 'Active', NOW(), 0.93, 'org-hc-001', NOW(), NOW()),

('AGENT-HC-002', 'Healthcare Patient Safety Agent', 'Patient Safety', 'Healthcare', 'Active', NOW(), 0.91, 'org-hc-001', NOW(), NOW()),

('AGENT-HC-003', 'Healthcare Clinical Risk Agent', 'Clinical Risk', 'Healthcare', 'Active', NOW(), 0.89, 'org-hc-001', NOW(), NOW()),

('AGENT-HC-004', 'Healthcare Device Security Agent', 'Device Security', 'Healthcare', 'Active', NOW(), 0.87, 'org-hc-001', NOW(), NOW()),

('AGENT-HC-005', 'Healthcare Quality Assurance Agent', 'Quality Assurance', 'Healthcare', 'Active', NOW(), 0.92, 'org-hc-001', NOW(), NOW());

-- =============================================
-- AI AGENT ACTIVITIES SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO ai_agent_activities (id, agent_id, activity_type, description, input_data, output_data, confidence_score, execution_time_ms, organization_id, created_at) VALUES
('ACT-HC-001', 'AGENT-HC-001', 'HIPAA Compliance Check', 'Automated HIPAA compliance assessment for patient data systems', '{"systems_checked": 15, "patient_records": 50000, "access_logs": 1000}', '{"compliance_score": 8.7, "violations_found": 2, "recommendations": ["Update access controls", "Enhance audit logging"]}', 0.93, 2100, 'org-hc-001', NOW()),

('ACT-HC-002', 'AGENT-HC-002', 'Patient Safety Analysis', 'Analysis of patient safety incidents and risk patterns', '{"incidents_analyzed": 25, "time_period": "30_days", "departments": 8}', '{"risk_score": 6.2, "trending_issues": 3, "recommendations": ["Enhanced training", "Process improvements"]}', 0.91, 1800, 'org-hc-001', NOW()),

('ACT-HC-003', 'AGENT-HC-003', 'Clinical Risk Assessment', 'Assessment of clinical trial risks and protocol compliance', '{"trials_active": 12, "protocols_reviewed": 5, "participants": 1500}', '{"risk_level": "Medium", "compliance_gaps": 2, "recommendations": ["Protocol updates", "Additional monitoring"]}', 0.89, 2500, 'org-hc-001', NOW()),

('ACT-HC-004', 'AGENT-HC-004', 'Device Security Scan', 'Security assessment of connected medical devices', '{"devices_scanned": 45, "vulnerabilities_found": 8, "critical_issues": 2}', '{"security_score": 7.5, "patches_needed": 5, "recommendations": ["Immediate patching", "Network segmentation"]}', 0.87, 3200, 'org-hc-001', NOW()),

('ACT-HC-005', 'AGENT-HC-005', 'Quality Metrics Analysis', 'Analysis of healthcare quality metrics and outcomes', '{"metrics_analyzed": 20, "time_period": "quarterly", "departments": 10}', '{"quality_score": 8.0, "improvement_areas": 4, "recommendations": ["Process optimization", "Staff training"]}', 0.92, 1900, 'org-hc-001', NOW());

-- =============================================
-- RISK MITIGATION PLANS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO risk_mitigation_plans (id, risk_id, plan_name, description, status, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('MIT-HC-001', 'RISK-HC-001', 'Enhanced Data Protection Program', 'Implement advanced encryption and access controls for patient data', 'In Progress', 'user-hc-001', '2024-12-31', 'org-hc-001', NOW(), NOW()),

('MIT-HC-002', 'RISK-HC-002', 'Medical Device Security Framework', 'Establish comprehensive security framework for connected medical devices', 'In Progress', 'user-hc-004', '2024-11-30', 'org-hc-001', NOW(), NOW()),

('MIT-HC-003', 'RISK-HC-003', 'Clinical Trial Compliance Program', 'Enhance clinical trial monitoring and compliance processes', 'In Progress', 'user-hc-003', '2024-10-31', 'org-hc-001', NOW(), NOW()),

('MIT-HC-004', 'RISK-HC-004', 'Patient Safety Improvement Initiative', 'Implement advanced patient safety protocols and training programs', 'In Progress', 'user-hc-002', '2024-12-31', 'org-hc-001', NOW(), NOW()),

('MIT-HC-005', 'RISK-HC-005', 'Regulatory Change Management System', 'Establish proactive regulatory change monitoring and response system', 'In Progress', 'user-hc-007', '2024-11-15', 'org-hc-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE GAPS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO compliance_gaps (id, assessment_id, gap_description, severity, status, remediation_plan, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('GAP-HC-001', 'COMP-HC-001', 'Incomplete patient consent documentation for data sharing', 'Medium', 'Open', 'Implement automated consent management system', 'user-hc-001', '2024-10-15', 'org-hc-001', NOW(), NOW()),

('GAP-HC-002', 'COMP-HC-002', 'Clinical trial data integrity controls need enhancement', 'High', 'Open', 'Implement advanced data validation and audit trails', 'user-hc-003', '2024-11-30', 'org-hc-001', NOW(), NOW()),

('GAP-HC-003', 'COMP-HC-004', 'Medical device firmware update process not automated', 'Medium', 'Open', 'Implement automated device management and patching', 'user-hc-004', '2024-10-31', 'org-hc-001', NOW(), NOW()),

('GAP-HC-004', 'COMP-HC-006', 'Healthcare analytics data anonymization needs improvement', 'High', 'Open', 'Enhance data anonymization and de-identification processes', 'user-hc-006', '2024-11-15', 'org-hc-001', NOW(), NOW()),

('GAP-HC-005', 'COMP-HC-007', 'Quality management system documentation outdated', 'Medium', 'Open', 'Update quality management system documentation and procedures', 'user-hc-007', '2024-10-20', 'org-hc-001', NOW(), NOW());

-- =============================================
-- WORKFLOW TASKS SAMPLE DATA (Healthcare Domain)
-- =============================================

INSERT INTO workflow_tasks (id, workflow_id, task_name, description, status, assignee_id, due_date, priority, organization_id, created_at, updated_at) VALUES
('TASK-HC-001', 'WF-HC-001', 'HIPAA Risk Assessment Update', 'Update HIPAA risk assessment for new patient data systems', 'In Progress', 'user-hc-001', '2024-09-30', 'High', 'org-hc-001', NOW(), NOW()),

('TASK-HC-002', 'WF-HC-002', 'Patient Safety Root Cause Analysis', 'Complete root cause analysis for recent patient safety incident', 'Pending', 'user-hc-002', '2024-09-20', 'High', 'org-hc-001', NOW(), NOW()),

('TASK-HC-003', 'WF-HC-003', 'Clinical Trial Protocol Approval', 'Review and approve new clinical trial protocol', 'In Progress', 'user-hc-003', '2024-09-25', 'High', 'org-hc-001', NOW(), NOW()),

('TASK-HC-004', 'WF-HC-004', 'Medical Device Vulnerability Assessment', 'Assess vulnerabilities in connected medical devices', 'Pending', 'user-hc-004', '2024-09-18', 'High', 'org-hc-001', NOW(), NOW()),

('TASK-HC-005', 'WF-HC-005', 'Adverse Event Report Submission', 'Submit adverse event report to regulatory authorities', 'In Progress', 'user-hc-005', '2024-09-28', 'High', 'org-hc-001', NOW(), NOW()),

('TASK-HC-006', 'WF-HC-006', 'Healthcare Analytics Compliance Review', 'Review healthcare analytics for research compliance', 'Pending', 'user-hc-006', '2024-10-05', 'Medium', 'org-hc-001', NOW(), NOW()),

('TASK-HC-007', 'WF-HC-007', 'Quality Assurance Process Audit', 'Conduct quality assurance audit of clinical processes', 'In Progress', 'user-hc-007', '2024-09-22', 'Medium', 'org-hc-001', NOW(), NOW()),

('TASK-HC-008', 'WF-HC-008', 'Emergency Preparedness Drill', 'Execute emergency preparedness drill and document results', 'Pending', 'user-hc-008', '2024-09-15', 'Medium', 'org-hc-001', NOW(), NOW());

-- =============================================
-- SAMPLE DATA SUMMARY (Healthcare Domain)
-- =============================================
-- Policies: 6 Healthcare-specific policies
-- Risks: 8 Healthcare domain risks
-- Compliance Assessments: 8 Healthcare assessments
-- Workflows: 8 Healthcare workflows
-- AI Agent Records: 5 Healthcare agents
-- AI Agent Activities: 5 recent activities
-- Risk Mitigation Plans: 5 plans
-- Compliance Gaps: 5 identified gaps
-- Workflow Tasks: 8 active tasks
-- Total Records: 61 Healthcare-specific records
