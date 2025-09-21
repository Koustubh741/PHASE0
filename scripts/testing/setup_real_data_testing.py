#!/usr/bin/env python3
"""
Real Data Testing Setup Script for GRC Platform
Sets up the complete testing environment with real BFSI data
"""

import os
import sys
import subprocess
import time
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GRCRealDataTester:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'grc_platform'),
            'user': os.getenv('DB_USER', 'grc_user'),
            'password': os.getenv('DB_PASSWORD', 'grc_password')
        }
        self.test_results = {}
        
    def check_docker_services(self):
        """Check if all Docker services are running"""
        logger.info("🐳 Checking Docker services...")
        
        services = ['grc-postgres', 'grc-redis', 'grc-backend', 'grc-frontend', 'grc-ai-agents']
        running_services = []
        
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'], 
                                  capture_output=True, text=True)
            
            for service in services:
                if service in result.stdout:
                    running_services.append(service)
                    logger.info(f"  ✅ {service} is running")
                else:
                    logger.warning(f"  ❌ {service} is not running")
            
            return len(running_services) == len(services)
            
        except Exception as e:
            logger.error(f"Error checking Docker services: {e}")
            return False
    
    def start_docker_services(self):
        """Start all Docker services"""
        logger.info("🚀 Starting Docker services...")
        
        try:
            # Change to project directory
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            os.chdir(project_dir)
            
            # Start services
            result = subprocess.run(['docker-compose', 'up', '-d'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Docker services started successfully")
                time.sleep(30)  # Wait for services to initialize
                return True
            else:
                logger.error(f"❌ Failed to start Docker services: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Docker services: {e}")
            return False
    
    def wait_for_database(self, max_retries=30):
        """Wait for database to be ready"""
        logger.info("⏳ Waiting for database to be ready...")
        
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(**self.db_config)
                conn.close()
                logger.info("✅ Database is ready")
                return True
            except Exception as e:
                logger.info(f"  Attempt {attempt + 1}/{max_retries}: Database not ready yet...")
                time.sleep(2)
        
        logger.error("❌ Database failed to become ready")
        return False
    
    def load_real_bfsi_data(self):
        """Load real BFSI sample data"""
        logger.info("📊 Loading real BFSI data...")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get the path to the BFSI sample data
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sql_file_path = os.path.join(script_dir, '..', 'database', 'bfsi_sample_data.sql')
            
            # Execute the SQL file
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            cursor.execute(sql_content)
            conn.commit()
            
            # Verify data was loaded
            cursor.execute("SELECT COUNT(*) FROM policies WHERE organization_id = 'org-123'")
            policies_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM risks WHERE organization_id = 'org-123'")
            risks_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_assessments WHERE organization_id = 'org-123'")
            compliance_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM workflows WHERE organization_id = 'org-123'")
            workflows_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ BFSI data loaded successfully:")
            logger.info(f"   - Policies: {policies_count}")
            logger.info(f"   - Risks: {risks_count}")
            logger.info(f"   - Compliance Assessments: {compliance_count}")
            logger.info(f"   - Workflows: {workflows_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load BFSI data: {e}")
            return False
    
    def _generate_test_users(self):
        """Generate test users dynamically"""
        import uuid
        from datetime import datetime
        
        roles = [
            'Chief Risk Officer', 'Compliance Manager', 'Risk Analyst', 
            'Operations Manager', 'Credit Risk Manager', 'Market Risk Manager'
        ]
        
        first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Lisa']
        last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Taylor']
        
        test_users = []
        for i, role in enumerate(roles):
            user_id = f"user-{str(uuid.uuid4())[:8]}"
            first_name = first_names[i % len(first_names)]
            last_name = last_names[i % len(last_names)]
            email = f"{first_name.lower()}.{last_name.lower()}@testbank.com"
            
            test_users.append({
                'id': user_id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role,
                'organization_id': 'org-123'
            })
        
        return test_users

    def create_test_users(self):
        """Create test users for different roles"""
        logger.info("👥 Creating test users...")
        
        # Generate test users dynamically
        test_users = self._generate_test_users()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            for user in test_users:
                cursor.execute("""
                    INSERT INTO users (id, email, first_name, last_name, role, organization_id, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (id) DO UPDATE SET
                        email = EXCLUDED.email,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        role = EXCLUDED.role,
                        updated_at = NOW()
                """, (user['id'], user['email'], user['first_name'], 
                     user['last_name'], user['role'], user['organization_id']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Created {len(test_users)} test users")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create test users: {e}")
            return False
    
    def create_real_risk_scenarios(self):
        """Create realistic BFSI risk scenarios"""
        logger.info("⚠️ Creating realistic BFSI risk scenarios...")
        
        real_risks = [
            {
                'id': 'RISK-REAL-001',
                'title': 'Basel III Capital Adequacy Breach Risk',
                'description': 'Risk of falling below minimum capital requirements due to increased credit losses in commercial real estate portfolio',
                'category': 'Credit Risk',
                'risk_level': 'High',
                'probability': 0.4,
                'impact': 0.9,
                'status': 'Active',
                'owner_id': 'user-001',
                'organization_id': 'org-123',
                'mitigation_plan': 'Increase capital buffers, reduce exposure to commercial real estate, implement stress testing',
                'due_date': (datetime.now() + timedelta(days=30)).isoformat()
            },
            {
                'id': 'RISK-REAL-002',
                'title': 'AML Transaction Monitoring System Failure',
                'description': 'Risk of AML monitoring system downtime leading to undetected suspicious transactions',
                'category': 'Operational Risk',
                'risk_level': 'Critical',
                'probability': 0.2,
                'impact': 0.95,
                'status': 'Active',
                'owner_id': 'user-002',
                'organization_id': 'org-123',
                'mitigation_plan': 'Implement redundant systems, establish manual monitoring procedures, regular system testing',
                'due_date': (datetime.now() + timedelta(days=7)).isoformat()
            },
            {
                'id': 'RISK-REAL-003',
                'title': 'Interest Rate Risk Exposure',
                'description': 'Significant exposure to rising interest rates affecting net interest margin and bond portfolio value',
                'category': 'Market Risk',
                'risk_level': 'Medium',
                'probability': 0.7,
                'impact': 0.6,
                'status': 'Active',
                'owner_id': 'user-003',
                'organization_id': 'org-123',
                'mitigation_plan': 'Implement interest rate hedging strategies, diversify portfolio, stress testing',
                'due_date': (datetime.now() + timedelta(days=45)).isoformat()
            }
        ]
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            for risk in real_risks:
                cursor.execute("""
                    INSERT INTO risks (id, title, description, category, risk_level, probability, impact, 
                                     status, owner_id, organization_id, mitigation_plan, due_date, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        description = EXCLUDED.description,
                        category = EXCLUDED.category,
                        risk_level = EXCLUDED.risk_level,
                        probability = EXCLUDED.probability,
                        impact = EXCLUDED.impact,
                        status = EXCLUDED.status,
                        mitigation_plan = EXCLUDED.mitigation_plan,
                        due_date = EXCLUDED.due_date,
                        updated_at = NOW()
                """, (risk['id'], risk['title'], risk['description'], risk['category'],
                     risk['risk_level'], risk['probability'], risk['impact'], risk['status'],
                     risk['owner_id'], risk['organization_id'], risk['mitigation_plan'],
                     risk['due_date']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Created {len(real_risks)} realistic risk scenarios")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create realistic risk scenarios: {e}")
            return False
    
    def create_real_compliance_scenarios(self):
        """Create realistic BFSI compliance scenarios"""
        logger.info("✅ Creating realistic BFSI compliance scenarios...")
        
        real_compliance = [
            {
                'id': 'COMP-REAL-001',
                'title': 'Basel III Capital Adequacy Assessment Q4 2024',
                'description': 'Quarterly assessment of capital adequacy ratios and Basel III compliance requirements',
                'framework': 'Basel III',
                'status': 'In Progress',
                'score': 7.2,
                'target_score': 9.0,
                'assessor_id': 'user-001',
                'organization_id': 'org-123',
                'due_date': (datetime.now() + timedelta(days=15)).isoformat(),
                'requirements': [
                    'Tier 1 Capital Ratio ≥ 6%',
                    'Total Capital Ratio ≥ 8%',
                    'Leverage Ratio ≥ 3%',
                    'LCR ≥ 100%',
                    'NSFR ≥ 100%'
                ]
            },
            {
                'id': 'COMP-REAL-002',
                'title': 'SOX Internal Controls Testing',
                'description': 'Annual testing of internal controls over financial reporting',
                'framework': 'SOX',
                'status': 'In Progress',
                'score': 8.1,
                'target_score': 8.5,
                'assessor_id': 'user-002',
                'organization_id': 'org-123',
                'due_date': (datetime.now() + timedelta(days=30)).isoformat(),
                'requirements': [
                    'Control Environment Assessment',
                    'Risk Assessment Process',
                    'Control Activities Testing',
                    'Information and Communication',
                    'Monitoring Activities'
                ]
            },
            {
                'id': 'COMP-REAL-003',
                'title': 'PCI DSS Security Assessment',
                'description': 'Annual PCI DSS compliance assessment for payment card data security',
                'framework': 'PCI DSS',
                'status': 'Pending',
                'score': 0,
                'target_score': 8.0,
                'assessor_id': 'user-004',
                'organization_id': 'org-123',
                'due_date': (datetime.now() + timedelta(days=60)).isoformat(),
                'requirements': [
                    'Build and Maintain Secure Networks',
                    'Protect Cardholder Data',
                    'Maintain Vulnerability Management',
                    'Implement Strong Access Control',
                    'Regularly Monitor Networks',
                    'Maintain Information Security Policy'
                ]
            }
        ]
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            for comp in real_compliance:
                cursor.execute("""
                    INSERT INTO compliance_assessments (id, title, description, framework, status, 
                                                      score, target_score, assessor_id, organization_id, 
                                                      due_date, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        description = EXCLUDED.description,
                        framework = EXCLUDED.framework,
                        status = EXCLUDED.status,
                        score = EXCLUDED.score,
                        target_score = EXCLUDED.target_score,
                        due_date = EXCLUDED.due_date,
                        updated_at = NOW()
                """, (comp['id'], comp['title'], comp['description'], comp['framework'],
                     comp['status'], comp['score'], comp['target_score'], comp['assessor_id'],
                     comp['organization_id'], comp['due_date']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Created {len(real_compliance)} realistic compliance scenarios")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create realistic compliance scenarios: {e}")
            return False
    
    def verify_test_environment(self):
        """Verify the test environment is properly set up"""
        logger.info("🔍 Verifying test environment...")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check database tables
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """)
            tables = [row['table_name'] for row in cursor.fetchall()]
            
            expected_tables = ['policies', 'risks', 'compliance_assessments', 'workflows', 
                             'ai_agent_records', 'users', 'organizations']
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.error(f"❌ Missing tables: {missing_tables}")
                return False
            
            # Check data counts
            cursor.execute("SELECT COUNT(*) as count FROM policies WHERE organization_id = 'org-123'")
            policies_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM risks WHERE organization_id = 'org-123'")
            risks_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM compliance_assessments WHERE organization_id = 'org-123'")
            compliance_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE organization_id = 'org-123'")
            users_count = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            logger.info("✅ Test environment verification:")
            logger.info(f"   - Database tables: {len(tables)} tables found")
            logger.info(f"   - Policies: {policies_count}")
            logger.info(f"   - Risks: {risks_count}")
            logger.info(f"   - Compliance Assessments: {compliance_count}")
            logger.info(f"   - Users: {users_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to verify test environment: {e}")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        logger.info("🚀 Starting GRC Platform Real Data Testing Setup")
        logger.info("=" * 60)
        
        setup_steps = [
            ("Check Docker Services", self.check_docker_services),
            ("Start Docker Services", self.start_docker_services),
            ("Wait for Database", self.wait_for_database),
            ("Load BFSI Data", self.load_real_bfsi_data),
            ("Create Test Users", self.create_test_users),
            ("Create Risk Scenarios", self.create_real_risk_scenarios),
            ("Create Compliance Scenarios", self.create_real_compliance_scenarios),
            ("Verify Environment", self.verify_test_environment)
        ]
        
        for step_name, step_function in setup_steps:
            logger.info(f"\n📋 {step_name}...")
            try:
                result = step_function()
                self.test_results[step_name] = result
                if result:
                    logger.info(f"✅ {step_name} completed successfully")
                else:
                    logger.error(f"❌ {step_name} failed")
                    return False
            except Exception as e:
                logger.error(f"❌ {step_name} failed with error: {e}")
                self.test_results[step_name] = False
                return False
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Real Data Testing Setup Completed Successfully!")
        logger.info("=" * 60)
        
        # Print summary
        logger.info("\n📊 Setup Summary:")
        for step_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"   {step_name}: {status}")
        
        logger.info("\n🌐 Access URLs:")
        logger.info("   Frontend: http://localhost:3000")
        logger.info("   Backend API: http://localhost:3001")
        logger.info("   AI Agents: http://localhost:8000")
        logger.info("   Database: localhost:5432")
        logger.info("   Redis: localhost:6379")
        
        logger.info("\n👥 Test Users:")
        logger.info("   CFO: cfo@testbank.com")
        logger.info("   Compliance Manager: compliance@testbank.com")
        logger.info("   Risk Analyst: risk@testbank.com")
        logger.info("   Operations Manager: ops@testbank.com")
        
        return True

def main():
    """Main function"""
    tester = GRCRealDataTester()
    success = tester.run_setup()
    
    if success:
        logger.info("\n🎯 Next Steps:")
        logger.info("   1. Run API tests: python scripts/test_real_data_apis.py")
        logger.info("   2. Run AI agent tests: python scripts/test_real_data_ai_agents.py")
        logger.info("   3. Run end-to-end tests: python scripts/test_real_data_e2e.py")
        logger.info("   4. Access the frontend and test user workflows")
        sys.exit(0)
    else:
        logger.error("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
