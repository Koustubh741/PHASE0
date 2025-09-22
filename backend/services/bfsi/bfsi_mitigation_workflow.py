#!/usr/bin/env python3
"""
BFSI Mitigation Workflow System
GRC workflow integration for gap mitigation and compliance management
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

class WorkflowPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

@dataclass
class WorkflowTask:
    task_id: str
    workflow_id: str
    task_name: str
    description: str
    assigned_to: str
    due_date: datetime
    status: TaskStatus
    priority: WorkflowPriority
    dependencies: List[str]
    deliverables: List[str]
    created_date: datetime
    completed_date: Optional[datetime] = None

@dataclass
class MitigationWorkflow:
    workflow_id: str
    gap_id: str
    organization_name: str
    workflow_name: str
    description: str
    assigned_owner: str
    target_completion_date: datetime
    status: WorkflowStatus
    priority: WorkflowPriority
    progress_percentage: int
    tasks: List[WorkflowTask]
    created_date: datetime
    last_updated: datetime
    completed_date: Optional[datetime] = None

class BFSIMitigationWorkflowSystem:
    """
    BFSI Mitigation Workflow System
    Manages GRC workflows for gap mitigation and compliance management
    """
    
    def __init__(self, db_path: str = "bfsi_policies.db"):
        self.db_path = db_path
        self.ensure_database()
        
        # Standard workflow templates for different gap types
        self.workflow_templates = {
            "sox_compliance": {
                "name": "SOX Compliance Implementation",
                "description": "Comprehensive SOX compliance implementation workflow",
                "tasks": [
                    {
                        "name": "Policy Development",
                        "description": "Develop comprehensive SOX compliance policies",
                        "duration_days": 14,
                        "priority": "critical"
                    },
                    {
                        "name": "Control Implementation",
                        "description": "Implement internal controls over financial reporting",
                        "duration_days": 21,
                        "priority": "critical"
                    },
                    {
                        "name": "Documentation",
                        "description": "Create comprehensive documentation",
                        "duration_days": 7,
                        "priority": "high"
                    },
                    {
                        "name": "Training",
                        "description": "Conduct staff training on SOX requirements",
                        "duration_days": 5,
                        "priority": "high"
                    },
                    {
                        "name": "Testing",
                        "description": "Test and validate controls",
                        "duration_days": 10,
                        "priority": "high"
                    }
                ]
            },
            "basel_iii_compliance": {
                "name": "Basel III Capital Requirements",
                "description": "Basel III capital adequacy implementation workflow",
                "tasks": [
                    {
                        "name": "Capital Assessment",
                        "description": "Assess current capital adequacy ratios",
                        "duration_days": 10,
                        "priority": "critical"
                    },
                    {
                        "name": "Risk Framework",
                        "description": "Implement risk management framework",
                        "duration_days": 21,
                        "priority": "critical"
                    },
                    {
                        "name": "Stress Testing",
                        "description": "Implement stress testing procedures",
                        "duration_days": 14,
                        "priority": "high"
                    },
                    {
                        "name": "Reporting Systems",
                        "description": "Set up regulatory reporting systems",
                        "duration_days": 14,
                        "priority": "high"
                    }
                ]
            },
            "pci_dss_compliance": {
                "name": "PCI DSS Implementation",
                "description": "Payment Card Industry Data Security Standard implementation",
                "tasks": [
                    {
                        "name": "Security Assessment",
                        "description": "Conduct comprehensive security assessment",
                        "duration_days": 7,
                        "priority": "critical"
                    },
                    {
                        "name": "Network Security",
                        "description": "Implement network security controls",
                        "duration_days": 14,
                        "priority": "critical"
                    },
                    {
                        "name": "Data Protection",
                        "description": "Implement cardholder data protection",
                        "duration_days": 10,
                        "priority": "high"
                    },
                    {
                        "name": "Monitoring",
                        "description": "Set up continuous monitoring",
                        "duration_days": 7,
                        "priority": "high"
                    }
                ]
            },
            "gdpr_compliance": {
                "name": "GDPR Compliance Implementation",
                "description": "General Data Protection Regulation compliance workflow",
                "tasks": [
                    {
                        "name": "Data Mapping",
                        "description": "Map all personal data processing activities",
                        "duration_days": 14,
                        "priority": "critical"
                    },
                    {
                        "name": "Privacy Policies",
                        "description": "Develop comprehensive privacy policies",
                        "duration_days": 10,
                        "priority": "high"
                    },
                    {
                        "name": "Consent Management",
                        "description": "Implement consent management systems",
                        "duration_days": 14,
                        "priority": "high"
                    },
                    {
                        "name": "Data Subject Rights",
                        "description": "Implement data subject rights procedures",
                        "duration_days": 10,
                        "priority": "high"
                    }
                ]
            }
        }
        
        logger.info("BFSI Mitigation Workflow System initialized")

    def ensure_database(self):
        """Ensure database tables exist for workflow management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create workflow tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mitigation_workflows (
                workflow_id TEXT PRIMARY KEY,
                gap_id TEXT NOT NULL,
                organization_name TEXT NOT NULL,
                workflow_name TEXT NOT NULL,
                description TEXT,
                assigned_owner TEXT NOT NULL,
                target_completion_date TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                progress_percentage INTEGER DEFAULT 0,
                created_date TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                completed_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_tasks (
                task_id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                description TEXT,
                assigned_to TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                dependencies TEXT,
                deliverables TEXT,
                created_date TEXT NOT NULL,
                completed_date TEXT,
                FOREIGN KEY (workflow_id) REFERENCES mitigation_workflows (workflow_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_mitigation_workflow(self, 
                                 gap_id: str,
                                 organization_name: str,
                                 assigned_owner: str,
                                 target_completion_date: str,
                                 gap_type: str = "general") -> MitigationWorkflow:
        """Create a new mitigation workflow for a gap"""
        
        logger.info(f"Creating mitigation workflow for gap {gap_id}")
        
        # Get workflow template based on gap type
        template = self.workflow_templates.get(gap_type, self.workflow_templates["sox_compliance"])
        
        # Create workflow
        workflow_id = str(uuid.uuid4())
        workflow = MitigationWorkflow(
            workflow_id=workflow_id,
            gap_id=gap_id,
            organization_name=organization_name,
            workflow_name=template["name"],
            description=template["description"],
            assigned_owner=assigned_owner,
            target_completion_date=datetime.fromisoformat(target_completion_date),
            status=WorkflowStatus.CREATED,
            priority=WorkflowPriority.HIGH,
            progress_percentage=0,
            tasks=[],
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Create tasks from template
        current_date = datetime.now()
        for i, task_template in enumerate(template["tasks"]):
            task_id = str(uuid.uuid4())
            due_date = current_date + timedelta(days=task_template["duration_days"])
            
            task = WorkflowTask(
                task_id=task_id,
                workflow_id=workflow_id,
                task_name=task_template["name"],
                description=task_template["description"],
                assigned_to=assigned_owner,
                due_date=due_date,
                status=TaskStatus.PENDING,
                priority=WorkflowPriority(task_template["priority"]),
                dependencies=[],
                deliverables=[],
                created_date=current_date
            )
            
            workflow.tasks.append(task)
            current_date = due_date
        
        # Save workflow to database
        self._save_workflow(workflow)
        
        logger.info(f"Created mitigation workflow {workflow_id} with {len(workflow.tasks)} tasks")
        return workflow

    def update_workflow_status(self, workflow_id: str, status: WorkflowStatus) -> bool:
        """Update workflow status"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mitigation_workflows 
            SET status = ?, last_updated = ?
            WHERE workflow_id = ?
        ''', (status.value, datetime.now().isoformat(), workflow_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Updated workflow {workflow_id} status to {status.value}")
        
        return success

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status and recalculate workflow progress"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update task status
        completed_date = datetime.now().isoformat() if status == TaskStatus.COMPLETED else None
        
        cursor.execute('''
            UPDATE workflow_tasks 
            SET status = ?, completed_date = ?
            WHERE task_id = ?
        ''', (status.value, completed_date, task_id))
        
        if cursor.rowcount > 0:
            # Get workflow ID for this task
            cursor.execute('SELECT workflow_id FROM workflow_tasks WHERE task_id = ?', (task_id,))
            workflow_id = cursor.fetchone()[0]
            
            # Recalculate workflow progress
            self._recalculate_workflow_progress(workflow_id)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated task {task_id} status to {status.value}")
            return True
        
        conn.close()
        return False

    def _recalculate_workflow_progress(self, workflow_id: str):
        """Recalculate workflow progress based on completed tasks"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get task counts
        cursor.execute('''
            SELECT 
                COUNT(*) as total_tasks,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks
            FROM workflow_tasks 
            WHERE workflow_id = ?
        ''', (workflow_id,))
        
        result = cursor.fetchone()
        total_tasks = result[0]
        completed_tasks = result[1]
        
        if total_tasks > 0:
            progress_percentage = int((completed_tasks / total_tasks) * 100)
            
            # Update workflow progress
            cursor.execute('''
                UPDATE mitigation_workflows 
                SET progress_percentage = ?, last_updated = ?
                WHERE workflow_id = ?
            ''', (progress_percentage, datetime.now().isoformat(), workflow_id))
            
            # Update workflow status based on progress
            if progress_percentage == 100:
                cursor.execute('''
                    UPDATE mitigation_workflows 
                    SET status = 'completed', completed_date = ?
                    WHERE workflow_id = ?
                ''', (datetime.now().isoformat(), workflow_id))
        
        conn.commit()
        conn.close()

    def get_workflow(self, workflow_id: str) -> Optional[MitigationWorkflow]:
        """Get workflow by ID"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get workflow
        cursor.execute('''
            SELECT * FROM mitigation_workflows WHERE workflow_id = ?
        ''', (workflow_id,))
        
        workflow_row = cursor.fetchone()
        if not workflow_row:
            conn.close()
            return None
        
        # Get tasks
        cursor.execute('''
            SELECT * FROM workflow_tasks WHERE workflow_id = ? ORDER BY due_date
        ''', (workflow_id,))
        
        tasks = []
        for task_row in cursor.fetchall():
            task = WorkflowTask(
                task_id=task_row[0],
                workflow_id=task_row[1],
                task_name=task_row[2],
                description=task_row[3],
                assigned_to=task_row[4],
                due_date=datetime.fromisoformat(task_row[5]),
                status=TaskStatus(task_row[6]),
                priority=WorkflowPriority(task_row[7]),
                dependencies=json.loads(task_row[8]) if task_row[8] else [],
                deliverables=json.loads(task_row[9]) if task_row[9] else [],
                created_date=datetime.fromisoformat(task_row[10]),
                completed_date=datetime.fromisoformat(task_row[11]) if task_row[11] else None
            )
            tasks.append(task)
        
        conn.close()
        
        # Reconstruct workflow
        workflow = MitigationWorkflow(
            workflow_id=workflow_row[0],
            gap_id=workflow_row[1],
            organization_name=workflow_row[2],
            workflow_name=workflow_row[3],
            description=workflow_row[4],
            assigned_owner=workflow_row[5],
            target_completion_date=datetime.fromisoformat(workflow_row[6]),
            status=WorkflowStatus(workflow_row[7]),
            priority=WorkflowPriority(workflow_row[8]),
            progress_percentage=workflow_row[9],
            tasks=tasks,
            created_date=datetime.fromisoformat(workflow_row[10]),
            last_updated=datetime.fromisoformat(workflow_row[11]),
            completed_date=datetime.fromisoformat(workflow_row[12]) if workflow_row[12] else None
        )
        
        return workflow

    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT workflow_id, gap_id, organization_name, workflow_name, 
                   assigned_owner, target_completion_date, status, priority, 
                   progress_percentage, created_date
            FROM mitigation_workflows
            ORDER BY created_date DESC
        ''')
        
        workflows = []
        for row in cursor.fetchall():
            workflows.append({
                "workflow_id": row[0],
                "gap_id": row[1],
                "organization_name": row[2],
                "workflow_name": row[3],
                "assigned_owner": row[4],
                "target_completion_date": row[5],
                "status": row[6],
                "priority": row[7],
                "progress_percentage": row[8],
                "created_date": row[9]
            })
        
        conn.close()
        return workflows

    def get_workflows_by_owner(self, assigned_owner: str) -> List[Dict[str, Any]]:
        """Get workflows assigned to a specific owner"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT workflow_id, gap_id, organization_name, workflow_name, 
                   target_completion_date, status, priority, progress_percentage
            FROM mitigation_workflows
            WHERE assigned_owner = ?
            ORDER BY target_completion_date ASC
        ''', (assigned_owner,))
        
        workflows = []
        for row in cursor.fetchall():
            workflows.append({
                "workflow_id": row[0],
                "gap_id": row[1],
                "organization_name": row[2],
                "workflow_name": row[3],
                "target_completion_date": row[4],
                "status": row[5],
                "priority": row[6],
                "progress_percentage": row[7]
            })
        
        conn.close()
        return workflows

    def get_overdue_workflows(self) -> List[Dict[str, Any]]:
        """Get overdue workflows"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_date = datetime.now().isoformat()
        cursor.execute('''
            SELECT workflow_id, gap_id, organization_name, workflow_name, 
                   assigned_owner, target_completion_date, status, priority, 
                   progress_percentage
            FROM mitigation_workflows
            WHERE target_completion_date < ? AND status NOT IN ('completed', 'cancelled')
            ORDER BY target_completion_date ASC
        ''', (current_date,))
        
        workflows = []
        for row in cursor.fetchall():
            workflows.append({
                "workflow_id": row[0],
                "gap_id": row[1],
                "organization_name": row[2],
                "workflow_name": row[3],
                "assigned_owner": row[4],
                "target_completion_date": row[5],
                "status": row[6],
                "priority": row[7],
                "progress_percentage": row[8]
            })
        
        conn.close()
        return workflows

    def _save_workflow(self, workflow: MitigationWorkflow):
        """Save workflow to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save workflow
        cursor.execute('''
            INSERT INTO mitigation_workflows 
            (workflow_id, gap_id, organization_name, workflow_name, description,
             assigned_owner, target_completion_date, status, priority, progress_percentage,
             created_date, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            workflow.workflow_id,
            workflow.gap_id,
            workflow.organization_name,
            workflow.workflow_name,
            workflow.description,
            workflow.assigned_owner,
            workflow.target_completion_date.isoformat(),
            workflow.status.value,
            workflow.priority.value,
            workflow.progress_percentage,
            workflow.created_date.isoformat(),
            workflow.last_updated.isoformat()
        ))
        
        # Save tasks
        for task in workflow.tasks:
            cursor.execute('''
                INSERT INTO workflow_tasks 
                (task_id, workflow_id, task_name, description, assigned_to, due_date,
                 status, priority, dependencies, deliverables, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.task_id,
                task.workflow_id,
                task.task_name,
                task.description,
                task.assigned_to,
                task.due_date.isoformat(),
                task.status.value,
                task.priority.value,
                json.dumps(task.dependencies),
                json.dumps(task.deliverables),
                task.created_date.isoformat()
            ))
        
        conn.commit()
        conn.close()

    def generate_workflow_report(self, workflow_id: str) -> Dict[str, Any]:
        """Generate detailed workflow report"""
        
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return {"error": "Workflow not found"}
        
        # Calculate statistics
        total_tasks = len(workflow.tasks)
        completed_tasks = len([task for task in workflow.tasks if task.status == TaskStatus.COMPLETED])
        pending_tasks = len([task for task in workflow.tasks if task.status == TaskStatus.PENDING])
        in_progress_tasks = len([task for task in workflow.tasks if task.status == TaskStatus.IN_PROGRESS])
        
        # Calculate overdue tasks
        current_date = datetime.now()
        overdue_tasks = len([task for task in workflow.tasks 
                           if task.due_date < current_date and task.status != TaskStatus.COMPLETED])
        
        # Calculate completion timeline
        if completed_tasks > 0:
            avg_completion_time = sum([
                (task.completed_date - task.created_date).days 
                for task in workflow.tasks 
                if task.completed_date
            ]) / completed_tasks
        else:
            avg_completion_time = 0
        
        return {
            "workflow_id": workflow.workflow_id,
            "workflow_name": workflow.workflow_name,
            "organization_name": workflow.organization_name,
            "assigned_owner": workflow.assigned_owner,
            "status": workflow.status.value,
            "priority": workflow.priority.value,
            "progress_percentage": workflow.progress_percentage,
            "target_completion_date": workflow.target_completion_date.isoformat(),
            "created_date": workflow.created_date.isoformat(),
            "last_updated": workflow.last_updated.isoformat(),
            "statistics": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "in_progress_tasks": in_progress_tasks,
                "overdue_tasks": overdue_tasks,
                "avg_completion_time_days": round(avg_completion_time, 1)
            },
            "tasks": [
                {
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "description": task.description,
                    "assigned_to": task.assigned_to,
                    "due_date": task.due_date.isoformat(),
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "is_overdue": task.due_date < current_date and task.status != TaskStatus.COMPLETED
                }
                for task in workflow.tasks
            ]
        }

# Example usage and testing
def main():
    """Example usage of the BFSI Mitigation Workflow System"""
    
    # Initialize workflow system
    workflow_system = BFSIMitigationWorkflowSystem()
    
    # Create a mitigation workflow
    print("🔄 Creating BFSI Mitigation Workflow...")
    
    workflow = workflow_system.create_mitigation_workflow(
        gap_id="gap_001",
        organization_name="Sample Financial Institution",
        assigned_owner="John Doe",
        target_completion_date="2024-03-15T00:00:00",
        gap_type="sox_compliance"
    )
    
    print(f"\n📋 Workflow Created:")
    print(f"Workflow ID: {workflow.workflow_id}")
    print(f"Workflow Name: {workflow.workflow_name}")
    print(f"Assigned Owner: {workflow.assigned_owner}")
    print(f"Target Completion: {workflow.target_completion_date}")
    print(f"Total Tasks: {len(workflow.tasks)}")
    
    print(f"\n📝 Tasks:")
    for i, task in enumerate(workflow.tasks, 1):
        print(f"{i}. {task.task_name} ({task.priority.value}) - Due: {task.due_date.strftime('%Y-%m-%d')}")
    
    # Generate workflow report
    print(f"\n📊 Workflow Report:")
    report = workflow_system.generate_workflow_report(workflow.workflow_id)
    print(f"Progress: {report['progress_percentage']}%")
    print(f"Status: {report['status']}")
    print(f"Total Tasks: {report['statistics']['total_tasks']}")
    print(f"Completed: {report['statistics']['completed_tasks']}")
    
    print(f"\n✅ Mitigation Workflow System Test Complete!")

if __name__ == "__main__":
    main()
