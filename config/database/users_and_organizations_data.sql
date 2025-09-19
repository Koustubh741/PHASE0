-- Users and Organizations Sample Data for GRC Platform
-- Supporting all 4 industries: BFSI, Healthcare, Manufacturing, Telecom

-- =============================================
-- ORGANIZATIONS SAMPLE DATA
-- =============================================

-- Update existing organizations and add new ones
INSERT INTO organizations (id, name, industry, size, location, created_at, updated_at) VALUES
('org-123', 'Global Bank International', 'Financial Services', 'Large', 'New York, NY', NOW(), NOW()),
('org-hc-001', 'MedTech Solutions Inc.', 'Healthcare', 'Large', 'Boston, MA', NOW(), NOW()),
('org-mfg-001', 'Advanced Manufacturing Corp', 'Manufacturing', 'Large', 'Detroit, MI', NOW(), NOW()),
('org-tel-001', 'TelecomConnect Networks', 'Telecommunications', 'Large', 'Dallas, TX', NOW(), NOW()),
('org-hc-002', 'Regional Healthcare System', 'Healthcare', 'Medium', 'Chicago, IL', NOW(), NOW()),
('org-mfg-002', 'Precision Manufacturing Ltd', 'Manufacturing', 'Medium', 'Cleveland, OH', NOW(), NOW()),
('org-tel-002', 'Metro Wireless Solutions', 'Telecommunications', 'Medium', 'Atlanta, GA', NOW(), NOW());

-- =============================================
-- USERS SAMPLE DATA (BFSI - Global Bank International)
-- =============================================

INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-001', 'john.smith', 'john.smith@globalbank.com', 'John', 'Smith', 'Chief Risk Officer', 'org-123', true, NOW(), NOW()),
('user-002', 'sarah.johnson', 'sarah.johnson@globalbank.com', 'Sarah', 'Johnson', 'Compliance Manager', 'org-123', true, NOW(), NOW()),
('user-003', 'michael.chen', 'michael.chen@globalbank.com', 'Michael', 'Chen', 'Credit Risk Manager', 'org-123', true, NOW(), NOW()),
('user-004', 'lisa.davis', 'lisa.davis@globalbank.com', 'Lisa', 'Davis', 'Operational Risk Manager', 'org-123', true, NOW(), NOW()),
('user-005', 'robert.wilson', 'robert.wilson@globalbank.com', 'Robert', 'Wilson', 'Regulatory Reporting Manager', 'org-123', true, NOW(), NOW()),
('user-006', 'jennifer.brown', 'jennifer.brown@globalbank.com', 'Jennifer', 'Brown', 'Cybersecurity Manager', 'org-123', true, NOW(), NOW()),
('user-007', 'david.miller', 'david.miller@globalbank.com', 'David', 'Miller', 'Market Risk Manager', 'org-123', true, NOW(), NOW()),
('user-008', 'amanda.taylor', 'amanda.taylor@globalbank.com', 'Amanda', 'Taylor', 'Risk Analyst', 'org-123', true, NOW(), NOW()),
('user-009', 'kevin.anderson', 'kevin.anderson@globalbank.com', 'Kevin', 'Anderson', 'Compliance Analyst', 'org-123', true, NOW(), NOW()),
('user-010', 'rachel.thomas', 'rachel.thomas@globalbank.com', 'Rachel', 'Thomas', 'GRC Administrator', 'org-123', true, NOW(), NOW());

-- =============================================
-- USERS SAMPLE DATA (Healthcare - MedTech Solutions Inc.)
-- =============================================

INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-hc-001', 'dr.maria.rodriguez', 'maria.rodriguez@medtech.com', 'Maria', 'Rodriguez', 'Chief Medical Officer', 'org-hc-001', true, NOW(), NOW()),
('user-hc-002', 'dr.james.patel', 'james.patel@medtech.com', 'James', 'Patel', 'Patient Safety Director', 'org-hc-001', true, NOW(), NOW()),
('user-hc-003', 'dr.emily.wang', 'emily.wang@medtech.com', 'Emily', 'Wang', 'Clinical Research Director', 'org-hc-001', true, NOW(), NOW()),
('user-hc-004', 'alex.kim', 'alex.kim@medtech.com', 'Alex', 'Kim', 'IT Security Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-005', 'dr.sophia.garcia', 'sophia.garcia@medtech.com', 'Sophia', 'Garcia', 'Quality Assurance Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-006', 'marcus.johnson', 'marcus.johnson@medtech.com', 'Marcus', 'Johnson', 'Data Analytics Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-007', 'dr.olivia.martinez', 'olivia.martinez@medtech.com', 'Olivia', 'Martinez', 'Regulatory Affairs Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-008', 'tyler.white', 'tyler.white@medtech.com', 'Tyler', 'White', 'Emergency Preparedness Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-009', 'dr.nathan.lee', 'nathan.lee@medtech.com', 'Nathan', 'Lee', 'Clinical Quality Manager', 'org-hc-001', true, NOW(), NOW()),
('user-hc-010', 'isabella.clark', 'isabella.clark@medtech.com', 'Isabella', 'Clark', 'Healthcare Compliance Analyst', 'org-hc-001', true, NOW(), NOW());

-- =============================================
-- USERS SAMPLE DATA (Manufacturing - Advanced Manufacturing Corp)
-- =============================================

INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-mfg-001', 'william.thompson', 'william.thompson@advmfg.com', 'William', 'Thompson', 'Quality Director', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-002', 'jessica.moore', 'jessica.moore@advmfg.com', 'Jessica', 'Moore', 'Environmental Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-003', 'christopher.hall', 'christopher.hall@advmfg.com', 'Christopher', 'Hall', 'Safety Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-004', 'ashley.allen', 'ashley.allen@advmfg.com', 'Ashley', 'Allen', 'Supply Chain Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-005', 'matthew.young', 'matthew.young@advmfg.com', 'Matthew', 'Young', 'Product Safety Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-006', 'samantha.king', 'samantha.king@advmfg.com', 'Samantha', 'King', 'IT Security Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-007', 'daniel.wright', 'daniel.wright@advmfg.com', 'Daniel', 'Wright', 'Regulatory Compliance Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-008', 'megan.lopez', 'megan.lopez@advmfg.com', 'Megan', 'Lopez', 'Equipment Maintenance Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-009', 'ryan.hill', 'ryan.hill@advmfg.com', 'Ryan', 'Hill', 'Production Manager', 'org-mfg-001', true, NOW(), NOW()),
('user-mfg-010', 'lauren.scott', 'lauren.scott@advmfg.com', 'Lauren', 'Scott', 'Manufacturing Compliance Analyst', 'org-mfg-001', true, NOW(), NOW());

-- =============================================
-- USERS SAMPLE DATA (Telecom - TelecomConnect Networks)
-- =============================================

INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-tel-001', 'mark.adams', 'mark.adams@telecomconnect.com', 'Mark', 'Adams', 'Regulatory Affairs Director', 'org-tel-001', true, NOW(), NOW()),
('user-tel-002', 'nicole.carter', 'nicole.carter@telecomconnect.com', 'Nicole', 'Carter', 'Network Security Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-003', 'brandon.mitchell', 'brandon.mitchell@telecomconnect.com', 'Brandon', 'Mitchell', 'Privacy Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-004', 'stephanie.perez', 'stephanie.perez@telecomconnect.com', 'Stephanie', 'Perez', 'Service Quality Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-005', 'justin.roberts', 'justin.roberts@telecomconnect.com', 'Justin', 'Roberts', 'Network Infrastructure Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-006', 'danielle.turner', 'danielle.turner@telecomconnect.com', 'Danielle', 'Turner', 'Fraud Prevention Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-007', 'aaron.phillips', 'aaron.phillips@telecomconnect.com', 'Aaron', 'Phillips', 'Emergency Services Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-008', 'crystal.campbell', 'crystal.campbell@telecomconnect.com', 'Crystal', 'Campbell', 'Infrastructure Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-009', 'jeremy.parker', 'jeremy.parker@telecomconnect.com', 'Jeremy', 'Parker', 'Spectrum Manager', 'org-tel-001', true, NOW(), NOW()),
('user-tel-010', 'vanessa.evans', 'vanessa.evans@telecomconnect.com', 'Vanessa', 'Evans', 'Telecom Compliance Analyst', 'org-tel-001', true, NOW(), NOW());

-- =============================================
-- USERS SAMPLE DATA (Additional Organizations)
-- =============================================

-- Regional Healthcare System Users
INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-hc-011', 'dr.richard.baker', 'richard.baker@regionalhealth.com', 'Richard', 'Baker', 'Chief Compliance Officer', 'org-hc-002', true, NOW(), NOW()),
('user-hc-012', 'lisa.gonzalez', 'lisa.gonzalez@regionalhealth.com', 'Lisa', 'Gonzalez', 'HIPAA Compliance Manager', 'org-hc-002', true, NOW(), NOW()),
('user-hc-013', 'dr.thomas.nelson', 'thomas.nelson@regionalhealth.com', 'Thomas', 'Nelson', 'Clinical Director', 'org-hc-002', true, NOW(), NOW());

-- Precision Manufacturing Ltd Users
INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-mfg-011', 'jennifer.adams', 'jennifer.adams@precisionmfg.com', 'Jennifer', 'Adams', 'Quality Manager', 'org-mfg-002', true, NOW(), NOW()),
('user-mfg-012', 'robert.cook', 'robert.cook@precisionmfg.com', 'Robert', 'Cook', 'Safety Coordinator', 'org-mfg-002', true, NOW(), NOW()),
('user-mfg-013', 'michelle.bailey', 'michelle.bailey@precisionmfg.com', 'Michelle', 'Bailey', 'Environmental Coordinator', 'org-mfg-002', true, NOW(), NOW());

-- Metro Wireless Solutions Users
INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES
('user-tel-011', 'kenneth.rivera', 'kenneth.rivera@metrowireless.com', 'Kenneth', 'Rivera', 'Network Operations Manager', 'org-tel-002', true, NOW(), NOW()),
('user-tel-012', 'angela.cooper', 'angela.cooper@metrowireless.com', 'Angela', 'Cooper', 'Customer Experience Manager', 'org-tel-002', true, NOW(), NOW()),
('user-tel-013', 'gregory.richardson', 'gregory.richardson@metrowireless.com', 'Gregory', 'Richardson', 'Regulatory Specialist', 'org-tel-002', true, NOW(), NOW());

-- =============================================
-- AUDIT LOGS SAMPLE DATA
-- =============================================

INSERT INTO audit_logs (id, user_id, action, resource_type, resource_id, details, ip_address, user_agent, organization_id, created_at) VALUES
('audit-001', 'user-001', 'CREATE', 'POLICY', 'POL-BFSI-001', 'Created Basel III Capital Requirements Policy', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'org-123', NOW() - INTERVAL '1 day'),
('audit-002', 'user-hc-001', 'CREATE', 'POLICY', 'POL-HC-001', 'Created HIPAA Privacy and Security Policy', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'org-hc-001', NOW() - INTERVAL '2 days'),
('audit-003', 'user-mfg-001', 'CREATE', 'POLICY', 'POL-MFG-001', 'Created ISO 9001 Quality Management Policy', '192.168.1.102', 'Mozilla/5.0 (X11; Linux x86_64)', 'org-mfg-001', NOW() - INTERVAL '3 days'),
('audit-004', 'user-tel-001', 'CREATE', 'POLICY', 'POL-TEL-001', 'Created FCC Regulatory Compliance Policy', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'org-tel-001', NOW() - INTERVAL '4 days'),
('audit-005', 'user-002', 'UPDATE', 'RISK', 'RISK-BFSI-001', 'Updated Basel III Non-Compliance Risk assessment', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'org-123', NOW() - INTERVAL '5 days'),
('audit-006', 'user-hc-002', 'UPDATE', 'RISK', 'RISK-HC-001', 'Updated Patient Data Breach Risk mitigation plan', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'org-hc-001', NOW() - INTERVAL '6 days'),
('audit-007', 'user-mfg-002', 'UPDATE', 'RISK', 'RISK-MFG-001', 'Updated Supply Chain Disruption Risk assessment', '192.168.1.102', 'Mozilla/5.0 (X11; Linux x86_64)', 'org-mfg-001', NOW() - INTERVAL '7 days'),
('audit-008', 'user-tel-002', 'UPDATE', 'RISK', 'RISK-TEL-001', 'Updated Network Outage Risk mitigation strategy', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'org-tel-001', NOW() - INTERVAL '8 days');

-- =============================================
-- SAMPLE DATA SUMMARY
-- =============================================
-- Organizations: 7 organizations across 4 industries
-- Users: 43 users across all organizations
-- Audit Logs: 8 sample audit log entries
-- Total Records: 58 user and organization records
