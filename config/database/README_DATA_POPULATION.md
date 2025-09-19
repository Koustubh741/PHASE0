# GRC Platform Sample Data Population Guide

This guide explains how to populate the GRC Platform database with comprehensive sample data for all industries.

## Overview

The sample data includes realistic GRC data across 4 industries:
- **BFSI** (Banking, Financial Services, Insurance)
- **Healthcare** 
- **Manufacturing**
- **Telecom**

## Data Files

### 1. Core Schema and Basic Data
- `schema.sql` - Database schema and basic reference data
- `users_and_organizations_data.sql` - Organizations and user accounts

### 2. Industry-Specific Data
- `bfsi_sample_data.sql` - BFSI industry data (61 records)
- `healthcare_sample_data.sql` - Healthcare industry data (61 records)  
- `manufacturing_sample_data.sql` - Manufacturing industry data (65 records)
- `telecom_sample_data.sql` - Telecom industry data (67 records)

### 3. Population Script
- `populate_all_sample_data.sql` - Master script to run all data files

## Quick Start

### Option 1: Run Master Script
```bash
# Connect to your PostgreSQL database
psql -h localhost -U your_username -d grc_platform

# Run the master population script
\i database/populate_all_sample_data.sql
```

### Option 2: Run Individual Files
```bash
# 1. Create schema and basic data
\i database/schema.sql

# 2. Add users and organizations
\i database/users_and_organizations_data.sql

# 3. Add industry-specific data
\i database/bfsi_sample_data.sql
\i database/healthcare_sample_data.sql
\i database/manufacturing_sample_data.sql
\i database/telecom_sample_data.sql
```

## Expected Results

After running all scripts, you should have:

### Organizations (7 total)
- Global Bank International (BFSI)
- MedTech Solutions Inc. (Healthcare)
- Advanced Manufacturing Corp (Manufacturing)
- TelecomConnect Networks (Telecom)
- Regional Healthcare System (Healthcare)
- Precision Manufacturing Ltd (Manufacturing)
- Metro Wireless Solutions (Telecom)

### Users (43 total)
- 10 BFSI users (CRO, Compliance Manager, Risk Managers, etc.)
- 13 Healthcare users (CMO, Patient Safety Director, Clinical Research Director, etc.)
- 13 Manufacturing users (Quality Director, Environmental Manager, Safety Manager, etc.)
- 13 Telecom users (Regulatory Affairs Director, Network Security Manager, etc.)

### GRC Data
- **25 Policies** across all industries
- **35 Risks** with realistic probability/impact scores
- **32 Compliance Assessments** with scores and gaps
- **32 Workflows** with active tasks and assignments
- **20 AI Agents** with performance metrics and activities
- **Risk Mitigation Plans** and **Compliance Gaps**
- **Audit Logs** for sample audit trail

## Dashboard Impact

With this data populated, your dashboard will show:

### Key Metrics Cards
- **Total Policies**: 25 (instead of 0)
- **Total Risks**: 35 (instead of 0)  
- **Compliance Score**: 82.5% (instead of 0%)
- **Active Workflows**: 32 (instead of 0)

### Charts and Visualizations
- **Risk Trends**: Realistic monthly risk data
- **Compliance Status**: Pie chart with compliant/non-compliant/in-progress
- **Policy Status**: Distribution across active/review/draft/archived
- **AI Agent Status**: Active agents with performance scores

### Recent Activity
- Policy approvals and updates
- Risk identifications and assessments
- Compliance assessment completions
- Workflow task assignments

## Backend Services Enhancement

All backend services now include **mock data fallback**:

- If database is empty, services return realistic mock data
- Mock data includes proper structure and realistic values
- Services gracefully handle both real and mock data scenarios
- Dashboard will work immediately even without database population

## Verification

After populating data, verify with these queries:

```sql
-- Check record counts
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
SELECT 'AI Agent Records', COUNT(*) FROM ai_agent_records;

-- Check dashboard data
SELECT 
    (SELECT COUNT(*) FROM policies) as total_policies,
    (SELECT COUNT(*) FROM risks) as total_risks,
    (SELECT AVG(score) FROM compliance_assessments) as avg_compliance_score,
    (SELECT COUNT(*) FROM workflows WHERE status = 'Active') as active_workflows;
```

## Troubleshooting

### Common Issues

1. **Foreign Key Errors**: Ensure you run `schema.sql` first to create all tables
2. **User ID Conflicts**: All user IDs are unique across industries
3. **Organization ID Conflicts**: Each industry uses different organization IDs
4. **Permission Errors**: Ensure your database user has INSERT permissions

### Reset Database
```sql
-- Drop and recreate database (WARNING: This deletes all data)
DROP DATABASE IF EXISTS grc_platform;
CREATE DATABASE grc_platform;
```

## Industry-Specific Details

### BFSI (Banking, Financial Services, Insurance)
- **Focus**: Basel III, KYC/AML, Credit Risk, Operational Risk
- **Compliance**: Basel III, SOX, AML/CFT, FATCA/CRS
- **Risks**: Capital adequacy, credit concentration, liquidity, cybersecurity
- **AI Agents**: Compliance, Risk Assessment, Fraud Detection, AML Monitoring, Regulatory Reporting

### Healthcare
- **Focus**: HIPAA, Patient Safety, Clinical Trials, Medical Device Security
- **Compliance**: HIPAA, FDA 21 CFR, Joint Commission, ISO 13485
- **Risks**: Patient data breaches, device security, clinical trial compliance
- **AI Agents**: HIPAA Compliance, Patient Safety, Clinical Risk, Device Security, Quality Assurance

### Manufacturing
- **Focus**: ISO 9001, Environmental Management, Workplace Safety, Supply Chain
- **Compliance**: ISO 9001, ISO 14001, OSHA, FDA 21 CFR, EPA
- **Risks**: Supply chain disruption, quality failure, safety incidents, environmental compliance
- **AI Agents**: Quality Control, Supply Chain, Safety, Environmental, Compliance

### Telecom
- **Focus**: FCC Compliance, Network Security, Customer Privacy, Service Quality
- **Compliance**: FCC, GDPR/CCPA, NIST CSF, ITIL, FCC 911
- **Risks**: Network outages, cybersecurity, FCC violations, data breaches
- **AI Agents**: Network Monitoring, Fraud Detection, Compliance, Customer Experience, Security

## Next Steps

1. **Start Services**: Start all backend services and frontend
2. **Access Dashboard**: Navigate to http://localhost:3000
3. **Verify Data**: Check that all metrics show realistic values
4. **Test Features**: Test policy management, risk assessment, compliance workflows
5. **Customize**: Modify data to match your specific requirements

The dashboard should now display meaningful, realistic data across all GRC domains and industries!
