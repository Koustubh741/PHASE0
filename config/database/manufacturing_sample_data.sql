-- Manufacturing Sample Data for GRC Platform
-- Following System Architecture Diagram

-- =============================================
-- POLICIES SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO policies (id, title, description, category, status, version, effective_date, review_date, owner_id, organization_id, created_at, updated_at) VALUES
('POL-MFG-001', 'ISO 9001 Quality Management Policy', 'Comprehensive quality management system policy aligned with ISO 9001:2015 standards', 'Quality Management', 'Active', '2.3', '2024-01-01', '2024-12-31', 'user-mfg-001', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-002', 'Environmental Management Policy', 'Environmental protection and sustainability policy aligned with ISO 14001 standards', 'Environmental', 'Active', '1.9', '2024-01-15', '2024-12-31', 'user-mfg-002', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-003', 'Occupational Safety and Health Policy', 'Workplace safety and health protection policy aligned with OSHA requirements', 'Safety', 'Active', '2.1', '2024-02-01', '2024-12-31', 'user-mfg-003', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-004', 'Supply Chain Risk Management Policy', 'Framework for managing supply chain risks and ensuring supplier compliance', 'Supply Chain', 'Active', '1.8', '2024-01-20', '2024-12-31', 'user-mfg-004', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-005', 'Product Recall and Safety Policy', 'Procedures for product recalls, safety incidents, and regulatory notifications', 'Product Safety', 'Active', '2.0', '2024-01-10', '2024-12-31', 'user-mfg-005', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-006', 'Cybersecurity and IT Security Policy', 'IT security and cybersecurity controls for manufacturing systems and IoT devices', 'Information Security', 'Active', '1.7', '2024-02-15', '2024-12-31', 'user-mfg-006', 'org-mfg-001', NOW(), NOW()),

('POL-MFG-007', 'Regulatory Compliance Policy', 'Framework for meeting FDA, EPA, and other regulatory requirements', 'Compliance', 'Active', '1.6', '2024-01-25', '2024-12-31', 'user-mfg-007', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- RISKS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO risks (id, title, description, category, risk_level, probability, impact, status, owner_id, organization_id, created_at, updated_at) VALUES
('RISK-MFG-001', 'Supply Chain Disruption Risk', 'Risk of supply chain disruptions affecting production and delivery schedules', 'Supply Chain Risk', 'High', 0.5, 0.8, 'Active', 'user-mfg-004', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-002', 'Product Quality Failure Risk', 'Risk of product quality failures leading to recalls and customer complaints', 'Quality Risk', 'Medium', 0.4, 0.7, 'Active', 'user-mfg-001', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-003', 'Workplace Safety Incident Risk', 'Risk of workplace accidents and safety incidents affecting employees', 'Safety Risk', 'Medium', 0.3, 0.8, 'Active', 'user-mfg-003', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-004', 'Environmental Compliance Risk', 'Risk of environmental violations and regulatory penalties', 'Environmental Risk', 'Medium', 0.4, 0.6, 'Active', 'user-mfg-002', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-005', 'Cybersecurity Breach Risk', 'Risk of cyber attacks on manufacturing systems and IoT devices', 'Technology Risk', 'High', 0.6, 0.7, 'Active', 'user-mfg-006', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-006', 'Regulatory Non-Compliance Risk', 'Risk of failing to meet FDA, EPA, or other regulatory requirements', 'Compliance Risk', 'Medium', 0.3, 0.7, 'Active', 'user-mfg-007', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-007', 'Equipment Failure Risk', 'Risk of critical equipment failures affecting production capacity', 'Operational Risk', 'Medium', 0.5, 0.6, 'Active', 'user-mfg-008', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-008', 'Raw Material Shortage Risk', 'Risk of raw material shortages affecting production schedules', 'Supply Chain Risk', 'Medium', 0.4, 0.5, 'Active', 'user-mfg-009', 'org-mfg-001', NOW(), NOW()),

('RISK-MFG-009', 'Product Recall Risk', 'Risk of product recalls due to safety or quality issues', 'Product Risk', 'Medium', 0.2, 0.9, 'Active', 'user-mfg-005', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE ASSESSMENTS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO compliance_assessments (id, title, description, framework, status, score, target_score, assessor_id, organization_id, created_at, updated_at) VALUES
('COMP-MFG-001', 'ISO 9001 Quality Management Assessment', 'Comprehensive assessment of ISO 9001:2015 quality management system', 'ISO 9001', 'Completed', 8.5, 9.0, 'user-mfg-001', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-002', 'ISO 14001 Environmental Management Assessment', 'Evaluation of environmental management system and sustainability practices', 'ISO 14001', 'In Progress', 7.8, 8.5, 'user-mfg-002', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-003', 'OSHA Safety Compliance Assessment', 'Assessment of workplace safety and health compliance', 'OSHA', 'Completed', 8.2, 8.5, 'user-mfg-003', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-004', 'FDA Manufacturing Compliance Assessment', 'Evaluation of FDA manufacturing and quality system regulations', 'FDA 21 CFR', 'In Progress', 7.6, 8.5, 'user-mfg-007', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-005', 'EPA Environmental Compliance Assessment', 'Assessment of environmental protection and waste management compliance', 'EPA', 'Completed', 8.0, 8.0, 'user-mfg-002', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-006', 'Supply Chain Security Assessment', 'Evaluation of supply chain security and supplier compliance', 'ISO 28000', 'In Progress', 7.4, 8.0, 'user-mfg-004', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-007', 'Cybersecurity Framework Assessment', 'Assessment of manufacturing cybersecurity controls and IoT security', 'NIST CSF', 'In Progress', 7.9, 8.5, 'user-mfg-006', 'org-mfg-001', NOW(), NOW()),

('COMP-MFG-008', 'Product Safety and Recall Readiness Assessment', 'Evaluation of product safety processes and recall readiness', 'CPSC', 'Completed', 8.3, 8.5, 'user-mfg-005', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- WORKFLOWS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO workflows (id, name, description, status, priority, assignee_id, due_date, organization_id, created_at, updated_at) VALUES
('WF-MFG-001', 'Quality Management System Audit', 'Regular audit of ISO 9001 quality management system', 'Active', 'High', 'user-mfg-001', '2024-12-31', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-002', 'Environmental Impact Assessment', 'Assessment of environmental impact and sustainability initiatives', 'Active', 'High', 'user-mfg-002', '2024-10-15', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-003', 'Workplace Safety Inspection', 'Regular workplace safety inspections and hazard assessments', 'Active', 'High', 'user-mfg-003', '2024-09-30', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-004', 'Supplier Compliance Review', 'Review of supplier compliance and supply chain risk assessment', 'Active', 'Medium', 'user-mfg-004', '2024-11-30', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-005', 'Product Safety Monitoring', 'Continuous monitoring of product safety and quality metrics', 'Active', 'High', 'user-mfg-005', '2024-12-31', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-006', 'Cybersecurity Assessment', 'Regular cybersecurity assessment of manufacturing systems', 'Active', 'High', 'user-mfg-006', '2024-10-31', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-007', 'Regulatory Compliance Review', 'Review of regulatory compliance and documentation', 'Active', 'Medium', 'user-mfg-007', '2024-11-15', 'org-mfg-001', NOW(), NOW()),

('WF-MFG-008', 'Equipment Maintenance and Calibration', 'Regular maintenance and calibration of critical manufacturing equipment', 'Active', 'Medium', 'user-mfg-008', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- AI AGENT RECORDS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO ai_agent_records (id, agent_name, agent_type, industry, status, last_activity, performance_score, organization_id, created_at, updated_at) VALUES
('AGENT-MFG-001', 'Manufacturing Quality Control Agent', 'Quality Control', 'Manufacturing', 'Active', NOW(), 0.92, 'org-mfg-001', NOW(), NOW()),

('AGENT-MFG-002', 'Manufacturing Supply Chain Agent', 'Supply Chain', 'Manufacturing', 'Active', NOW(), 0.88, 'org-mfg-001', NOW(), NOW()),

('AGENT-MFG-003', 'Manufacturing Safety Agent', 'Safety', 'Manufacturing', 'Active', NOW(), 0.90, 'org-mfg-001', NOW(), NOW()),

('AGENT-MFG-004', 'Manufacturing Environmental Agent', 'Environmental', 'Manufacturing', 'Active', NOW(), 0.86, 'org-mfg-001', NOW(), NOW()),

('AGENT-MFG-005', 'Manufacturing Compliance Agent', 'Compliance', 'Manufacturing', 'Active', NOW(), 0.91, 'org-mfg-001', NOW(), NOW());

-- =============================================
-- AI AGENT ACTIVITIES SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO ai_agent_activities (id, agent_id, activity_type, description, input_data, output_data, confidence_score, execution_time_ms, organization_id, created_at) VALUES
('ACT-MFG-001', 'AGENT-MFG-001', 'Quality Control Analysis', 'Analysis of product quality metrics and defect patterns', '{"products_tested": 1000, "defect_rate": 0.02, "time_period": "weekly"}', '{"quality_score": 8.5, "trending_issues": 2, "recommendations": ["Process optimization", "Equipment calibration"]}', 0.92, 1800, 'org-mfg-001', NOW()),

('ACT-MFG-002', 'AGENT-MFG-002', 'Supply Chain Risk Assessment', 'Assessment of supply chain risks and supplier performance', '{"suppliers_analyzed": 25, "risk_factors": 8, "time_period": "monthly"}', '{"risk_score": 6.8, "critical_suppliers": 3, "recommendations": ["Diversify suppliers", "Increase monitoring"]}', 0.88, 2200, 'org-mfg-001', NOW()),

('ACT-MFG-003', 'AGENT-MFG-003', 'Safety Incident Analysis', 'Analysis of workplace safety incidents and near-misses', '{"incidents_analyzed": 15, "near_misses": 8, "departments": 6}', '{"safety_score": 8.2, "risk_areas": 2, "recommendations": ["Enhanced training", "Safety equipment upgrade"]}', 0.90, 1600, 'org-mfg-001', NOW()),

('ACT-MFG-004', 'AGENT-MFG-004', 'Environmental Impact Assessment', 'Assessment of environmental impact and sustainability metrics', '{"emissions_analyzed": 12, "waste_streams": 5, "energy_usage": 8}', '{"environmental_score": 7.8, "improvement_areas": 3, "recommendations": ["Energy efficiency", "Waste reduction"]}', 0.86, 2400, 'org-mfg-001', NOW()),

('ACT-MFG-005', 'AGENT-MFG-005', 'Regulatory Compliance Check', 'Automated compliance check against regulatory requirements', '{"regulations_checked": 15, "processes_reviewed": 20, "time_period": "quarterly"}', '{"compliance_score": 8.1, "gaps_identified": 2, "recommendations": ["Documentation update", "Process improvement"]}', 0.91, 2000, 'org-mfg-001', NOW());

-- =============================================
-- RISK MITIGATION PLANS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO risk_mitigation_plans (id, risk_id, plan_name, description, status, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('MIT-MFG-001', 'RISK-MFG-001', 'Supply Chain Diversification Strategy', 'Diversify supplier base and establish alternative supply sources', 'In Progress', 'user-mfg-004', '2024-12-31', 'org-mfg-001', NOW(), NOW()),

('MIT-MFG-002', 'RISK-MFG-002', 'Quality Control Enhancement Program', 'Implement advanced quality control systems and automated testing', 'In Progress', 'user-mfg-001', '2024-11-30', 'org-mfg-001', NOW(), NOW()),

('MIT-MFG-003', 'RISK-MFG-003', 'Workplace Safety Improvement Initiative', 'Enhance safety protocols and implement advanced safety monitoring', 'In Progress', 'user-mfg-003', '2024-10-31', 'org-mfg-001', NOW(), NOW()),

('MIT-MFG-004', 'RISK-MFG-004', 'Environmental Compliance Program', 'Strengthen environmental monitoring and compliance processes', 'In Progress', 'user-mfg-002', '2024-12-31', 'org-mfg-001', NOW(), NOW()),

('MIT-MFG-005', 'RISK-MFG-005', 'Manufacturing Cybersecurity Framework', 'Implement comprehensive cybersecurity controls for manufacturing systems', 'In Progress', 'user-mfg-006', '2024-11-15', 'org-mfg-001', NOW(), NOW()),

('MIT-MFG-006', 'RISK-MFG-006', 'Regulatory Compliance Management System', 'Establish proactive regulatory compliance monitoring and management', 'In Progress', 'user-mfg-007', '2024-10-20', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- COMPLIANCE GAPS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO compliance_gaps (id, assessment_id, gap_description, severity, status, remediation_plan, owner_id, due_date, organization_id, created_at, updated_at) VALUES
('GAP-MFG-001', 'COMP-MFG-001', 'Quality management system documentation needs updating', 'Medium', 'Open', 'Update quality management system documentation and procedures', 'user-mfg-001', '2024-10-15', 'org-mfg-001', NOW(), NOW()),

('GAP-MFG-002', 'COMP-MFG-002', 'Environmental monitoring systems need enhancement', 'High', 'Open', 'Implement advanced environmental monitoring and reporting systems', 'user-mfg-002', '2024-11-30', 'org-mfg-001', NOW(), NOW()),

('GAP-MFG-003', 'COMP-MFG-004', 'FDA manufacturing controls require validation', 'High', 'Open', 'Validate and enhance FDA manufacturing control systems', 'user-mfg-007', '2024-10-31', 'org-mfg-001', NOW(), NOW()),

('GAP-MFG-004', 'COMP-MFG-006', 'Supplier compliance monitoring needs automation', 'Medium', 'Open', 'Implement automated supplier compliance monitoring system', 'user-mfg-004', '2024-11-15', 'org-mfg-001', NOW(), NOW()),

('GAP-MFG-005', 'COMP-MFG-007', 'Manufacturing IoT security controls need strengthening', 'High', 'Open', 'Enhance IoT security controls and network segmentation', 'user-mfg-006', '2024-10-20', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- WORKFLOW TASKS SAMPLE DATA (Manufacturing Domain)
-- =============================================

INSERT INTO workflow_tasks (id, workflow_id, task_name, description, status, assignee_id, due_date, priority, organization_id, created_at, updated_at) VALUES
('TASK-MFG-001', 'WF-MFG-001', 'Quality System Internal Audit', 'Conduct internal audit of quality management system', 'In Progress', 'user-mfg-001', '2024-09-30', 'High', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-002', 'WF-MFG-002', 'Environmental Impact Assessment', 'Complete environmental impact assessment for new production line', 'Pending', 'user-mfg-002', '2024-09-20', 'High', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-003', 'WF-MFG-003', 'Safety Hazard Assessment', 'Complete safety hazard assessment for production floor', 'In Progress', 'user-mfg-003', '2024-09-25', 'High', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-004', 'WF-MFG-004', 'Supplier Performance Review', 'Review supplier performance and compliance metrics', 'Pending', 'user-mfg-004', '2024-09-18', 'Medium', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-005', 'WF-MFG-005', 'Product Safety Testing', 'Complete product safety testing for new product line', 'In Progress', 'user-mfg-005', '2024-09-28', 'High', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-006', 'WF-MFG-006', 'Cybersecurity Vulnerability Assessment', 'Assess cybersecurity vulnerabilities in manufacturing systems', 'Pending', 'user-mfg-006', '2024-10-05', 'High', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-007', 'WF-MFG-007', 'Regulatory Documentation Review', 'Review and update regulatory compliance documentation', 'In Progress', 'user-mfg-007', '2024-09-22', 'Medium', 'org-mfg-001', NOW(), NOW()),

('TASK-MFG-008', 'WF-MFG-008', 'Equipment Calibration Schedule', 'Complete equipment calibration and maintenance schedule', 'Pending', 'user-mfg-008', '2024-09-15', 'Medium', 'org-mfg-001', NOW(), NOW());

-- =============================================
-- SAMPLE DATA SUMMARY (Manufacturing Domain)
-- =============================================
-- Policies: 7 Manufacturing-specific policies
-- Risks: 9 Manufacturing domain risks
-- Compliance Assessments: 8 Manufacturing assessments
-- Workflows: 8 Manufacturing workflows
-- AI Agent Records: 5 Manufacturing agents
-- AI Agent Activities: 5 recent activities
-- Risk Mitigation Plans: 6 plans
-- Compliance Gaps: 5 identified gaps
-- Workflow Tasks: 8 active tasks
-- Total Records: 65 Manufacturing-specific records
