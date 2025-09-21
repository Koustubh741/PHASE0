-- GRC Platform Database Initialization Script
-- This script sets up the initial database structure and creates default admin user

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS grc_platform;

-- Use the database
\c grc_platform;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create initial admin user
INSERT INTO users (
    id,
    username,
    email,
    first_name,
    last_name,
    role,
    status,
    organization_id,
    password_hash,
    email_verified,
    created_at,
    updated_at
) VALUES (
    uuid_generate_v4(),
    'admin',
    'admin@grcplatform.com',
    'System',
    'Administrator',
    'admin',
    'active',
    'system',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8VqOq6L8W2', -- password: AdminPass123!
    true,
    NOW(),
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Create default organization
INSERT INTO organizations (
    id,
    name,
    description,
    status,
    created_at,
    updated_at
) VALUES (
    'system',
    'System Organization',
    'Default system organization',
    'active',
    NOW(),
    NOW()
) ON CONFLICT (id) DO NOTHING;

-- Create audit log for initial setup
INSERT INTO audit_logs (
    id,
    action,
    resource,
    resource_id,
    user_id,
    user_name,
    organization_id,
    timestamp,
    description,
    severity,
    success,
    metadata
) VALUES (
    uuid_generate_v4(),
    'create',
    'system',
    'initial_setup',
    (SELECT id FROM users WHERE username = 'admin'),
    'System Administrator',
    'system',
    NOW(),
    'GRC Platform database initialized',
    'medium',
    true,
    '{"setup_version": "1.0.0", "initial_setup": true}'
);

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_username_trgm ON users USING gin (username gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_trgm ON users USING gin (email gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_policies_title_trgm ON policies USING gin (title gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_risks_title_trgm ON risks USING gin (title gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_controls_title_trgm ON controls USING gin (title gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_issues_title_trgm ON issues USING gin (title gin_trgm_ops);

-- Create partial indexes for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_active ON users (id) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_policies_active ON policies (id) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_risks_open ON risks (id) WHERE status IN ('identified', 'assessed');
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_controls_effective ON controls (id) WHERE status = 'effective';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_issues_open ON issues (id) WHERE status IN ('open', 'in_progress');

-- Create composite indexes for common query patterns
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_logs_user_org_time ON audit_logs (user_id, organization_id, timestamp DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_logs_resource_time ON audit_logs (resource, resource_id, timestamp DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_org_role_status ON users (organization_id, role, status);

-- Set up row level security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE risks ENABLE ROW LEVEL SECURITY;
ALTER TABLE controls ENABLE ROW LEVEL SECURITY;
ALTER TABLE issues ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users table
CREATE POLICY users_organization_isolation ON users
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Create RLS policies for policies table
CREATE POLICY policies_organization_isolation ON policies
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Create RLS policies for risks table
CREATE POLICY risks_organization_isolation ON risks
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Create RLS policies for controls table
CREATE POLICY controls_organization_isolation ON controls
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Create RLS policies for issues table
CREATE POLICY issues_organization_isolation ON issues
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Create RLS policies for audit_logs table
CREATE POLICY audit_logs_organization_isolation ON audit_logs
    FOR ALL TO grc_user
    USING (organization_id = current_setting('app.current_organization_id'));

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO grc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO grc_user;
GRANT USAGE ON SCHEMA public TO grc_user;

-- Create function to set organization context
CREATE OR REPLACE FUNCTION set_organization_context(org_id TEXT)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_organization_id', org_id, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to get current user's organization
CREATE OR REPLACE FUNCTION get_current_user_organization()
RETURNS TEXT AS $$
DECLARE
    org_id TEXT;
BEGIN
    SELECT organization_id INTO org_id 
    FROM users 
    WHERE id = current_setting('app.current_user_id')::UUID;
    
    RETURN org_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to check user permissions
CREATE OR REPLACE FUNCTION has_permission(user_id UUID, permission_name TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    user_role TEXT;
    has_perm BOOLEAN := FALSE;
BEGIN
    SELECT role INTO user_role FROM users WHERE id = user_id;
    
    -- Define permissions based on roles
    CASE user_role
        WHEN 'admin' THEN
            has_perm := TRUE;
        WHEN 'auditor' THEN
            has_perm := permission_name IN ('can_view_audit_logs', 'can_export_data');
        WHEN 'risk_owner' THEN
            has_perm := permission_name IN ('can_create_risks', 'can_edit_risks', 'can_assign_risks');
        WHEN 'control_owner' THEN
            has_perm := permission_name IN ('can_create_controls', 'can_edit_controls');
        WHEN 'compliance_manager' THEN
            has_perm := permission_name IN ('can_create_policies', 'can_edit_policies', 'can_approve_policies');
        WHEN 'policy_owner' THEN
            has_perm := permission_name IN ('can_create_policies', 'can_edit_policies');
        ELSE
            has_perm := FALSE;
    END CASE;
    
    RETURN has_perm;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- Log the change
    INSERT INTO audit_logs (
        id,
        action,
        resource,
        resource_id,
        user_id,
        user_name,
        organization_id,
        timestamp,
        description,
        old_values,
        new_values,
        severity,
        success
    ) VALUES (
        uuid_generate_v4(),
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id::TEXT, OLD.id::TEXT),
        current_setting('app.current_user_id')::UUID,
        current_setting('app.current_user_name'),
        current_setting('app.current_organization_id'),
        NOW(),
        TG_OP || ' operation on ' || TG_TABLE_NAME,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END,
        'medium',
        TRUE
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create audit triggers for all main tables
CREATE TRIGGER audit_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_policies_trigger
    AFTER INSERT OR UPDATE OR DELETE ON policies
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_risks_trigger
    AFTER INSERT OR UPDATE OR DELETE ON risks
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_controls_trigger
    AFTER INSERT OR UPDATE OR DELETE ON controls
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_issues_trigger
    AFTER INSERT OR UPDATE OR DELETE ON issues
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Create views for common queries
CREATE VIEW active_users AS
SELECT 
    id,
    username,
    email,
    first_name,
    last_name,
    role,
    organization_id,
    department,
    job_title,
    created_at,
    last_login
FROM users 
WHERE status = 'active';

CREATE VIEW policy_summary AS
SELECT 
    p.id,
    p.title,
    p.status,
    p.policy_type,
    p.owner_id,
    u.first_name || ' ' || u.last_name as owner_name,
    p.created_at,
    p.updated_at,
    p.effective_date,
    p.expiry_date
FROM policies p
LEFT JOIN users u ON p.owner_id = u.id;

CREATE VIEW risk_summary AS
SELECT 
    r.id,
    r.title,
    r.category,
    r.status,
    r.current_risk_level,
    r.current_risk_score,
    r.owner_id,
    u.first_name || ' ' || u.last_name as owner_name,
    r.created_at,
    r.updated_at,
    r.next_review_date
FROM risks r
LEFT JOIN users u ON r.owner_id = u.id;

CREATE VIEW control_summary AS
SELECT 
    c.id,
    c.title,
    c.control_type,
    c.status,
    c.effectiveness_rating,
    c.primary_owner,
    u.first_name || ' ' || u.last_name as owner_name,
    c.created_at,
    c.updated_at,
    c.next_test_date
FROM controls c
LEFT JOIN users u ON c.primary_owner = u.id;

CREATE VIEW issue_summary AS
SELECT 
    i.id,
    i.title,
    i.issue_type,
    i.priority,
    i.status,
    i.assigned_to,
    u.first_name || ' ' || u.last_name as assigned_user_name,
    i.created_at,
    i.updated_at,
    i.due_date
FROM issues i
LEFT JOIN users u ON i.assigned_to = u.id;

-- Create materialized views for reporting
CREATE MATERIALIZED VIEW audit_summary AS
SELECT 
    DATE(timestamp) as audit_date,
    organization_id,
    action,
    resource,
    COUNT(*) as event_count,
    COUNT(*) FILTER (WHERE success = true) as success_count,
    COUNT(*) FILTER (WHERE success = false) as failure_count
FROM audit_logs
GROUP BY DATE(timestamp), organization_id, action, resource;

-- Create index on materialized view
CREATE UNIQUE INDEX idx_audit_summary_unique ON audit_summary (audit_date, organization_id, action, resource);

-- Create function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_reporting_views()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY audit_summary;
END;
$$ LANGUAGE plpgsql;

-- Set up automated refresh of materialized views (requires pg_cron extension)
-- SELECT cron.schedule('refresh-audit-summary', '0 1 * * *', 'SELECT refresh_reporting_views();');

-- Final success message
DO $$
BEGIN
    RAISE NOTICE 'GRC Platform database initialization completed successfully!';
    RAISE NOTICE 'Default admin user created: admin / AdminPass123!';
    RAISE NOTICE 'Please change the default password after first login.';
END $$;
