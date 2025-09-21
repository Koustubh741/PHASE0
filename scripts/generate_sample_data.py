#!/usr/bin/env python3
"""
Dynamic Sample Data Generator for GRC Platform
Generates realistic sample data for all industries without hardcoded values
"""

import os
import sys
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SampleDataGenerator:
    """Generate dynamic sample data for GRC Platform"""
    
    def __init__(self):
        self.industries = {
            'bfsi': {
                'name': 'Banking, Financial Services, and Insurance',
                'organizations': ['Global Bank International', 'Regional Credit Union', 'Insurance Corp'],
                'roles': ['Chief Risk Officer', 'Compliance Manager', 'Credit Risk Manager', 'Operational Risk Manager', 'Regulatory Reporting Manager', 'Cybersecurity Manager', 'Market Risk Manager', 'Risk Analyst', 'Compliance Analyst', 'GRC Administrator']
            },
            'healthcare': {
                'name': 'Healthcare',
                'organizations': ['MedTech Solutions Inc.', 'Regional Healthcare System', 'Community Health Center'],
                'roles': ['Chief Medical Officer', 'Patient Safety Director', 'Clinical Research Director', 'IT Security Manager', 'Quality Assurance Manager', 'Data Analytics Manager', 'Regulatory Affairs Manager', 'Emergency Preparedness Manager', 'Clinical Quality Manager', 'Healthcare Compliance Analyst']
            },
            'manufacturing': {
                'name': 'Manufacturing',
                'organizations': ['Advanced Manufacturing Corp', 'Precision Manufacturing Ltd', 'Industrial Solutions Inc'],
                'roles': ['Quality Director', 'Environmental Manager', 'Safety Manager', 'Supply Chain Manager', 'Production Manager', 'Quality Control Manager', 'Environmental Compliance Manager', 'Safety Coordinator', 'Quality Analyst', 'Manufacturing Compliance Specialist']
            },
            'telecom': {
                'name': 'Telecommunications',
                'organizations': ['TelecomConnect Networks', 'Metro Wireless Solutions', 'Digital Communications Inc'],
                'roles': ['Regulatory Affairs Director', 'Network Security Manager', 'Compliance Manager', 'Quality Assurance Manager', 'Customer Experience Manager', 'Network Operations Manager', 'Regulatory Compliance Specialist', 'Security Analyst', 'Quality Manager', 'Telecom Compliance Analyst']
            }
        }
        
        self.locations = [
            'New York, NY', 'Boston, MA', 'Detroit, MI', 'Dallas, TX', 'Chicago, IL', 
            'Cleveland, OH', 'Atlanta, GA', 'San Francisco, CA', 'Seattle, WA', 'Miami, FL'
        ]
        
        self.company_sizes = ['Small', 'Medium', 'Large', 'Enterprise']
        
    def generate_organizations(self, count_per_industry: int = 2) -> List[Dict[str, Any]]:
        """Generate organization data"""
        organizations = []
        
        for industry_key, industry_data in self.industries.items():
            for i in range(count_per_industry):
                org_id = f"org-{industry_key}-{i+1:03d}"
                size = random.choice(self.company_sizes)
                location = random.choice(self.locations)
                
                organizations.append({
                    'id': org_id,
                    'name': random.choice(industry_data['organizations']),
                    'industry': industry_data['name'],
                    'size': size,
                    'location': location,
                    'created_at': self._random_date(),
                    'updated_at': self._random_date()
                })
        
        return organizations
    
    def generate_users(self, organizations: List[Dict[str, Any]], users_per_org: int = 10) -> List[Dict[str, Any]]:
        """Generate user data"""
        users = []
        
        for org in organizations:
            industry_key = org['id'].split('-')[1]
            industry_data = self.industries[industry_key]
            
            for i in range(users_per_org):
                user_id = f"user-{industry_key}-{i+1:03d}"
                first_name = self._random_name('first')
                last_name = self._random_name('last')
                username = f"{first_name.lower()}.{last_name.lower()}"
                email = f"{username}@{org['name'].lower().replace(' ', '').replace(',', '')}.com"
                role = random.choice(industry_data['roles'])
                
                users.append({
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'organization_id': org['id'],
                    'is_active': True,
                    'created_at': self._random_date(),
                    'updated_at': self._random_date()
                })
        
        return users
    
    def generate_policies(self, organizations: List[Dict[str, Any]], policies_per_org: int = 7) -> List[Dict[str, Any]]:
        """Generate policy data"""
        policies = []
        
        policy_templates = {
            'bfsi': [
                'Basel III Capital Requirements Policy',
                'Anti-Money Laundering Policy',
                'Data Privacy and Protection Policy',
                'Operational Risk Management Policy',
                'Market Risk Management Policy',
                'Credit Risk Management Policy',
                'Regulatory Reporting Policy'
            ],
            'healthcare': [
                'HIPAA Compliance Policy',
                'Patient Safety Policy',
                'Clinical Quality Policy',
                'Data Security Policy',
                'Emergency Preparedness Policy',
                'Regulatory Affairs Policy',
                'Clinical Research Policy'
            ],
            'manufacturing': [
                'ISO 9001 Quality Management Policy',
                'Environmental Management Policy',
                'Workplace Safety Policy',
                'Supply Chain Management Policy',
                'Product Safety Policy',
                'Cybersecurity Policy',
                'Regulatory Compliance Policy'
            ],
            'telecom': [
                'FCC Compliance Policy',
                'Network Security Policy',
                'Data Privacy Policy',
                'Service Quality Policy',
                'Infrastructure Management Policy',
                'Fraud Prevention Policy',
                'Emergency Services Policy'
            ]
        }
        
        for org in organizations:
            industry_key = org['id'].split('-')[1]
            org_policies = policy_templates.get(industry_key, [])
            
            for i, policy_name in enumerate(org_policies[:policies_per_org]):
                policy_id = f"policy-{org['id']}-{i+1:03d}"
                
                policies.append({
                    'id': policy_id,
                    'title': policy_name,
                    'description': f"Comprehensive {policy_name.lower()} for {org['name']}",
                    'category': self._get_policy_category(policy_name),
                    'status': random.choice(['active', 'draft', 'review', 'archived']),
                    'version': f"{random.randint(1, 5)}.{random.randint(0, 9)}",
                    'effective_date': self._random_date(),
                    'review_date': self._random_future_date(),
                    'organization_id': org['id'],
                    'created_at': self._random_date(),
                    'updated_at': self._random_date()
                })
        
        return policies
    
    def generate_risks(self, organizations: List[Dict[str, Any]], risks_per_org: int = 9) -> List[Dict[str, Any]]:
        """Generate risk data"""
        risks = []
        
        risk_templates = {
            'bfsi': [
                'Credit Risk Exposure',
                'Market Risk Volatility',
                'Operational Risk Events',
                'Regulatory Compliance Risk',
                'Cybersecurity Risk',
                'Liquidity Risk',
                'Reputation Risk',
                'Model Risk',
                'Concentration Risk'
            ],
            'healthcare': [
                'Patient Safety Risk',
                'Data Breach Risk',
                'Regulatory Compliance Risk',
                'Clinical Risk',
                'Operational Risk',
                'Financial Risk',
                'Reputation Risk',
                'Technology Risk',
                'Emergency Preparedness Risk'
            ],
            'manufacturing': [
                'Supply Chain Disruption',
                'Quality Failure Risk',
                'Safety Incident Risk',
                'Environmental Compliance Risk',
                'Technology Risk',
                'Financial Risk',
                'Regulatory Risk',
                'Operational Risk',
                'Reputation Risk'
            ],
            'telecom': [
                'Network Outage Risk',
                'Cybersecurity Risk',
                'FCC Violation Risk',
                'Data Breach Risk',
                'Service Quality Risk',
                'Regulatory Risk',
                'Technology Risk',
                'Operational Risk',
                'Financial Risk'
            ]
        }
        
        for org in organizations:
            industry_key = org['id'].split('-')[1]
            org_risks = risk_templates.get(industry_key, [])
            
            for i, risk_name in enumerate(org_risks[:risks_per_org]):
                risk_id = f"risk-{org['id']}-{i+1:03d}"
                
                risks.append({
                    'id': risk_id,
                    'title': risk_name,
                    'description': f"Risk assessment for {risk_name.lower()} at {org['name']}",
                    'category': self._get_risk_category(risk_name),
                    'impact': random.choice(['low', 'medium', 'high']),
                    'probability': random.choice(['low', 'medium', 'high']),
                    'status': random.choice(['open', 'monitoring', 'mitigated', 'closed']),
                    'owner': f"user-{industry_key}-{random.randint(1, 10):03d}",
                    'organization_id': org['id'],
                    'created_at': self._random_date(),
                    'updated_at': self._random_date()
                })
        
        return risks
    
    def _random_name(self, name_type: str) -> str:
        """Generate random names"""
        first_names = ['John', 'Sarah', 'Michael', 'Lisa', 'Robert', 'Jennifer', 'David', 'Amanda', 'Kevin', 'Rachel', 'Maria', 'James', 'Emily', 'Alex', 'Sophia', 'Marcus', 'Olivia', 'Tyler', 'Nathan', 'Isabella']
        last_names = ['Smith', 'Johnson', 'Chen', 'Davis', 'Wilson', 'Brown', 'Miller', 'Taylor', 'Anderson', 'Thomas', 'Rodriguez', 'Patel', 'Wang', 'Kim', 'Garcia', 'Johnson', 'Martinez', 'White', 'Lee', 'Clark']
        
        if name_type == 'first':
            return random.choice(first_names)
        else:
            return random.choice(last_names)
    
    def _random_date(self) -> str:
        """Generate random date within last year"""
        start_date = datetime.now() - timedelta(days=365)
        random_date = start_date + timedelta(days=random.randint(0, 365))
        return random_date.strftime('%Y-%m-%d %H:%M:%S')
    
    def _random_future_date(self) -> str:
        """Generate random future date"""
        future_date = datetime.now() + timedelta(days=random.randint(30, 365))
        return future_date.strftime('%Y-%m-%d')
    
    def _get_policy_category(self, policy_name: str) -> str:
        """Get policy category based on name"""
        if 'risk' in policy_name.lower():
            return 'Risk Management'
        elif 'security' in policy_name.lower() or 'cyber' in policy_name.lower():
            return 'Security'
        elif 'quality' in policy_name.lower():
            return 'Quality'
        elif 'compliance' in policy_name.lower():
            return 'Compliance'
        elif 'data' in policy_name.lower() or 'privacy' in policy_name.lower():
            return 'Data Protection'
        else:
            return 'General'
    
    def _get_risk_category(self, risk_name: str) -> str:
        """Get risk category based on name"""
        if 'credit' in risk_name.lower() or 'market' in risk_name.lower():
            return 'Financial'
        elif 'operational' in risk_name.lower():
            return 'Operational'
        elif 'cyber' in risk_name.lower() or 'security' in risk_name.lower():
            return 'Security'
        elif 'regulatory' in risk_name.lower() or 'compliance' in risk_name.lower():
            return 'Compliance'
        elif 'supply' in risk_name.lower():
            return 'Supply Chain'
        else:
            return 'General'
    
    def generate_sql_script(self, output_file: str = 'config/database/generated_sample_data.sql'):
        """Generate SQL script with sample data"""
        organizations = self.generate_organizations()
        users = self.generate_users(organizations)
        policies = self.generate_policies(organizations)
        risks = self.generate_risks(organizations)
        
        sql_content = []
        sql_content.append("-- Generated Sample Data for GRC Platform")
        sql_content.append("-- Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql_content.append("-- This file is auto-generated - do not edit manually")
        sql_content.append("")
        
        # Organizations
        sql_content.append("-- Organizations")
        sql_content.append("INSERT INTO organizations (id, name, industry, size, location, created_at, updated_at) VALUES")
        for i, org in enumerate(organizations):
            comma = "," if i < len(organizations) - 1 else ";"
            sql_content.append(f"('{org['id']}', '{org['name']}', '{org['industry']}', '{org['size']}', '{org['location']}', '{org['created_at']}', '{org['updated_at']}'){comma}")
        sql_content.append("")
        
        # Users
        sql_content.append("-- Users")
        sql_content.append("INSERT INTO users (id, username, email, first_name, last_name, role, organization_id, is_active, created_at, updated_at) VALUES")
        for i, user in enumerate(users):
            comma = "," if i < len(users) - 1 else ";"
            sql_content.append(f"('{user['id']}', '{user['username']}', '{user['email']}', '{user['first_name']}', '{user['last_name']}', '{user['role']}', '{user['organization_id']}', {user['is_active']}, '{user['created_at']}', '{user['updated_at']}'){comma}")
        sql_content.append("")
        
        # Policies
        sql_content.append("-- Policies")
        sql_content.append("INSERT INTO policies (id, title, description, category, status, version, effective_date, review_date, organization_id, created_at, updated_at) VALUES")
        for i, policy in enumerate(policies):
            comma = "," if i < len(policies) - 1 else ";"
            sql_content.append(f"('{policy['id']}', '{policy['title']}', '{policy['description']}', '{policy['category']}', '{policy['status']}', '{policy['version']}', '{policy['effective_date']}', '{policy['review_date']}', '{policy['organization_id']}', '{policy['created_at']}', '{policy['updated_at']}'){comma}")
        sql_content.append("")
        
        # Risks
        sql_content.append("-- Risks")
        sql_content.append("INSERT INTO risks (id, title, description, category, impact, probability, status, owner, organization_id, created_at, updated_at) VALUES")
        for i, risk in enumerate(risks):
            comma = "," if i < len(risks) - 1 else ";"
            sql_content.append(f"('{risk['id']}', '{risk['title']}', '{risk['description']}', '{risk['category']}', '{risk['impact']}', '{risk['probability']}', '{risk['status']}', '{risk['owner']}', '{risk['organization_id']}', '{risk['created_at']}', '{risk['updated_at']}'){comma}")
        
        # Write to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write('\n'.join(sql_content))
        
        print(f"Generated sample data SQL script: {output_file}")
        print(f"Organizations: {len(organizations)}")
        print(f"Users: {len(users)}")
        print(f"Policies: {len(policies)}")
        print(f"Risks: {len(risks)}")

def main():
    """Main function to generate sample data"""
    generator = SampleDataGenerator()
    generator.generate_sql_script()

if __name__ == "__main__":
    main()
