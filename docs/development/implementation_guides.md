# GRC Platform Implementation Guides

## Quick Start Guide

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ (for AI/ML components)
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- Git

### Development Environment Setup

#### 1. Clone and Setup Project
```bash
# Create project structure
mkdir grc-platform
cd grc-platform

# Initialize git repository
git init

# Create directory structure
mkdir -p {frontend,backend,ai-agents,infrastructure,docs}
mkdir -p backend/{api,services,models,middleware}
mkdir -p frontend/{src,public,components,pages}
mkdir -p ai-agents/{compliance,risk,documents,communication}
```

#### 2. Backend Setup (Node.js/Express)
```bash
cd backend
npm init -y
npm install express cors helmet morgan dotenv
npm install -D nodemon typescript @types/node @types/express
npm install pg redis jsonwebtoken bcryptjs
npm install -D @types/pg @types/jsonwebtoken @types/bcryptjs

# Initialize TypeScript
npx tsc --init
```

#### 3. Frontend Setup (React/TypeScript)
```bash
cd frontend
npx create-react-app . --template typescript
npm install @mui/material @emotion/react @emotion/styled
npm install @reduxjs/toolkit react-redux
npm install axios socket.io-client
npm install recharts @types/recharts
```

#### 4. AI Agents Setup (Python)
```bash
cd ai-agents
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn
pip install openai langchain pinecone-client
pip install pandas numpy scikit-learn
pip install pymongo psycopg2-binary redis
```

## Phase 1: Foundation Implementation

### Week 1-2: Project Setup

#### Backend API Structure
```typescript
// backend/src/app.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/policies', policyRoutes);
app.use('/api/risks', riskRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

#### Database Schema (PostgreSQL)
```sql
-- backend/database/schema.sql

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'risk_manager', 'compliance_officer', 'auditor')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policies table
CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    version VARCHAR(20) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('draft', 'review', 'approved', 'archived')),
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    effective_date DATE,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk register table
CREATE TABLE risks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    impact_score INTEGER CHECK (impact_score BETWEEN 1 AND 5),
    probability_score INTEGER CHECK (probability_score BETWEEN 1 AND 5),
    risk_score INTEGER GENERATED ALWAYS AS (impact_score * probability_score) STORED,
    status VARCHAR(50) NOT NULL CHECK (status IN ('identified', 'assessed', 'mitigated', 'accepted')),
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Authentication Service
```typescript
// backend/src/services/auth.service.ts
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { User } from '../models/user.model';

export class AuthService {
  private static readonly JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
  private static readonly JWT_EXPIRES_IN = '24h';

  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 12);
  }

  static async comparePassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  static generateToken(user: User): string {
    return jwt.sign(
      { 
        userId: user.id, 
        email: user.email, 
        role: user.role 
      },
      this.JWT_SECRET,
      { expiresIn: this.JWT_EXPIRES_IN }
    );
  }

  static verifyToken(token: string): any {
    return jwt.verify(token, this.JWT_SECRET);
  }
}
```

### Week 3-4: Core Services

#### User Management Service
```typescript
// backend/src/services/user.service.ts
import { User } from '../models/user.model';
import { DatabaseService } from './database.service';

export class UserService {
  static async createUser(userData: Partial<User>): Promise<User> {
    const query = `
      INSERT INTO users (email, password_hash, first_name, last_name, role)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `;
    
    const values = [
      userData.email,
      userData.password_hash,
      userData.first_name,
      userData.last_name,
      userData.role
    ];

    const result = await DatabaseService.query(query, values);
    return result.rows[0];
  }

  static async getUserById(id: string): Promise<User | null> {
    const query = 'SELECT * FROM users WHERE id = $1 AND is_active = true';
    const result = await DatabaseService.query(query, [id]);
    return result.rows[0] || null;
  }

  static async getUserByEmail(email: string): Promise<User | null> {
    const query = 'SELECT * FROM users WHERE email = $1 AND is_active = true';
    const result = await DatabaseService.query(query, [email]);
    return result.rows[0] || null;
  }
}
```

## Phase 2: GRC Features Implementation

### Policy Management System

#### Policy Model
```typescript
// backend/src/models/policy.model.ts
export interface Policy {
  id: string;
  title: string;
  content: string;
  version: string;
  status: 'draft' | 'review' | 'approved' | 'archived';
  created_by: string;
  approved_by?: string;
  effective_date?: Date;
  expiry_date?: Date;
  created_at: Date;
  updated_at: Date;
}

export interface PolicyVersion {
  id: string;
  policy_id: string;
  version: string;
  content: string;
  change_summary: string;
  created_at: Date;
}
```

#### Policy Service
```typescript
// backend/src/services/policy.service.ts
export class PolicyService {
  static async createPolicy(policyData: Partial<Policy>): Promise<Policy> {
    const query = `
      INSERT INTO policies (title, content, version, status, created_by, effective_date, expiry_date)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *
    `;
    
    const values = [
      policyData.title,
      policyData.content,
      policyData.version || '1.0',
      policyData.status || 'draft',
      policyData.created_by,
      policyData.effective_date,
      policyData.expiry_date
    ];

    const result = await DatabaseService.query(query, values);
    return result.rows[0];
  }

  static async updatePolicy(id: string, updates: Partial<Policy>): Promise<Policy> {
    const setClause = Object.keys(updates)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');
    
    const query = `
      UPDATE policies 
      SET ${setClause}, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;
    
    const values = [id, ...Object.values(updates)];
    const result = await DatabaseService.query(query, values);
    return result.rows[0];
  }

  static async getPoliciesByStatus(status: string): Promise<Policy[]> {
    const query = 'SELECT * FROM policies WHERE status = $1 ORDER BY created_at DESC';
    const result = await DatabaseService.query(query, [status]);
    return result.rows;
  }
}
```

### Risk Management System

#### Risk Assessment Algorithm
```typescript
// backend/src/services/risk.service.ts
export class RiskService {
  static calculateRiskScore(impact: number, probability: number): number {
    return impact * probability;
  }

  static getRiskLevel(score: number): string {
    if (score <= 4) return 'Low';
    if (score <= 9) return 'Medium';
    if (score <= 16) return 'High';
    return 'Critical';
  }

  static async assessRisk(riskData: {
    title: string;
    description: string;
    category: string;
    impact_score: number;
    probability_score: number;
    owner_id: string;
  }): Promise<any> {
    const risk_score = this.calculateRiskScore(
      riskData.impact_score, 
      riskData.probability_score
    );
    
    const risk_level = this.getRiskLevel(risk_score);

    const query = `
      INSERT INTO risks (title, description, category, impact_score, probability_score, owner_id, status)
      VALUES ($1, $2, $3, $4, $5, $6, 'identified')
      RETURNING *
    `;

    const values = [
      riskData.title,
      riskData.description,
      riskData.category,
      riskData.impact_score,
      riskData.probability_score,
      riskData.owner_id
    ];

    const result = await DatabaseService.query(query, values);
    return { ...result.rows[0], risk_level };
  }
}
```

## Phase 3: AI Integration

### AI Agent Base Class
```python
# ai-agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import asyncio
import json
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.status = "inactive"
        self.last_activity = None
        
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific tasks"""
        pass
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send message to another agent via MCP"""
        mcp_message = {
            "header": {
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source": self.agent_id,
                "destination": target_agent,
                "message_type": message.get("type", "general")
            },
            "payload": message
        }
        # Send via MCP broker
        await self.mcp_broker.send(mcp_message)
    
    def update_status(self, status: str):
        self.status = status
        self.last_activity = datetime.utcnow()
```

### Compliance Monitoring Agent
```python
# ai-agents/compliance/compliance_agent.py
from base_agent import BaseAgent
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__("compliance_001", "Compliance Monitoring Agent")
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embeddings = OpenAIEmbeddings()
        self.setup_vector_store()
    
    def setup_vector_store(self):
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        self.vector_store = Pinecone.from_existing_index(
            index_name="compliance-policies",
            embedding=self.embeddings
        )
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        if message.get("type") == "compliance_check":
            return await self.check_compliance(message.get("data", {}))
        elif message.get("type") == "policy_analysis":
            return await self.analyze_policy(message.get("data", {}))
        else:
            return {"error": "Unknown message type"}
    
    async def check_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance against policies"""
        document_content = data.get("content", "")
        policy_id = data.get("policy_id")
        
        # Get relevant policy sections
        relevant_sections = await self.find_relevant_policy_sections(
            document_content, policy_id
        )
        
        # Use GPT-4 to analyze compliance
        compliance_result = await self.analyze_compliance_with_gpt(
            document_content, relevant_sections
        )
        
        return {
            "compliance_status": compliance_result.get("status"),
            "violations": compliance_result.get("violations", []),
            "recommendations": compliance_result.get("recommendations", []),
            "confidence_score": compliance_result.get("confidence", 0.0)
        }
    
    async def analyze_compliance_with_gpt(self, content: str, policies: List[str]) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following content for compliance against the provided policies:
        
        Content: {content}
        
        Policies: {policies}
        
        Please provide:
        1. Compliance status (compliant, non-compliant, partially compliant)
        2. List of any violations found
        3. Recommendations for improvement
        4. Confidence score (0-1)
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        # Parse response and return structured data
        return self.parse_gpt_response(response.choices[0].message.content)
```

### MCP Communication Protocol
```python
# ai-agents/communication/mcp_broker.py
import asyncio
import json
import redis
from typing import Dict, Any, Callable
import uuid
from datetime import datetime

class MCPBroker:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        self.agents = {}
        self.message_handlers = {}
    
    async def register_agent(self, agent_id: str, agent: BaseAgent):
        """Register an agent with the MCP broker"""
        self.agents[agent_id] = agent
        await self.redis_client.sadd("registered_agents", agent_id)
        print(f"Agent {agent_id} registered successfully")
    
    async def send_message(self, message: Dict[str, Any]):
        """Send message via MCP protocol"""
        message_id = message["header"]["message_id"]
        destination = message["header"]["destination"]
        
        # Store message in Redis
        await self.redis_client.setex(
            f"message:{message_id}",
            3600,  # 1 hour TTL
            json.dumps(message)
        )
        
        # Publish to destination channel
        await self.redis_client.publish(
            f"agent:{destination}",
            json.dumps(message)
        )
    
    async def listen_for_messages(self, agent_id: str):
        """Listen for incoming messages"""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"agent:{agent_id}")
        
        async for message in pubsub.listen():
            if message["type"] == "message":
                mcp_message = json.loads(message["data"])
                await self.handle_incoming_message(agent_id, mcp_message)
    
    async def handle_incoming_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle incoming message for specific agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            response = await agent.process_message(message["payload"])
            
            # Send response back if needed
            if response and message["header"].get("expects_response"):
                response_message = {
                    "header": {
                        "message_id": str(uuid.uuid4()),
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": agent_id,
                        "destination": message["header"]["source"],
                        "message_type": "response"
                    },
                    "payload": response
                }
                await self.send_message(response_message)
```

## Phase 4: Frontend Implementation

### React Component Structure
```typescript
// frontend/src/components/Dashboard/Dashboard.tsx
import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { RiskChart } from '../Charts/RiskChart';
import { ComplianceStatus } from '../Compliance/ComplianceStatus';
import { PolicyList } from '../Policies/PolicyList';

export const Dashboard: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        GRC Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Risk Overview
            </Typography>
            <RiskChart />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Compliance Status
            </Typography>
            <ComplianceStatus />
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Policies
            </Typography>
            <PolicyList limit={5} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
```

### Redux Store Setup
```typescript
// frontend/src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { authSlice } from './slices/authSlice';
import { policySlice } from './slices/policySlice';
import { riskSlice } from './slices/riskSlice';
import { complianceSlice } from './slices/complianceSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
    policies: policySlice.reducer,
    risks: riskSlice.reducer,
    compliance: complianceSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

## Phase 5: Testing & Deployment

### Docker Configuration
```dockerfile
# Dockerfile.backend
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3001

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: grc_platform
      POSTGRES_USER: grc_user
      POSTGRES_PASSWORD: grc_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://grc_user:grc_password@postgres:5432/grc_platform
      REDIS_URL: redis://redis:6379
    ports:
      - "3001:3001"
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend

  ai-agents:
    build:
      context: ./ai-agents
      dockerfile: Dockerfile
    environment:
      REDIS_URL: redis://redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - redis

volumes:
  postgres_data:
```

### Kubernetes Deployment
```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grc-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: grc-backend
  template:
    metadata:
      labels:
        app: grc-backend
    spec:
      containers:
      - name: backend
        image: grc-platform/backend:latest
        ports:
        - containerPort: 3001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: grc-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

This implementation guide provides the foundation for building your GRC platform. Each phase builds upon the previous one, ensuring a systematic and manageable development process.

