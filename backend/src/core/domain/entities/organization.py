"""
Organization Domain Entity
Core business logic for Organization management in GRC Platform
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4


class OrganizationType(Enum):
    """Organization type enumeration"""
    CORPORATION = "corporation"
    PARTNERSHIP = "partnership"
    LLC = "llc"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    SUBSIDIARY = "subsidiary"
    DIVISION = "division"


class IndustryType(Enum):
    """Industry type enumeration"""
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    EDUCATION = "education"
    GOVERNMENT = "government"
    NON_PROFIT = "non_profit"
    OTHER = "other"


class OrganizationSize(Enum):
    """Organization size enumeration"""
    SMALL = "small"  # 1-50 employees
    MEDIUM = "medium"  # 51-999 employees
    LARGE = "large"  # 1000+ employees


@dataclass
class Organization:
    """Organization domain entity"""
    id: UUID
    name: str
    description: Optional[str] = None
    organization_type: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values after object creation"""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.id is None:
            self.id = uuid4()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert organization to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "organization_type": self.organization_type,
            "industry": self.industry,
            "size": self.size,
            "address": self.address,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "website": self.website,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        """Create organization from dictionary"""
        return cls(
            id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"],
            name=data["name"],
            description=data.get("description"),
            organization_type=data.get("organization_type"),
            industry=data.get("industry"),
            size=data.get("size"),
            address=data.get("address"),
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            website=data.get("website"),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        )
    
    def update(self, updates: Dict[str, Any]) -> "Organization":
        """Update organization with new values"""
        for key, value in updates.items():
            if hasattr(self, key) and key not in ["id", "created_at"]:
                setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
        return self
    
    def deactivate(self) -> "Organization":
        """Deactivate the organization"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        return self
    
    def activate(self) -> "Organization":
        """Activate the organization"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        return self
    
    def validate(self) -> List[str]:
        """Validate organization data"""
        errors = []
        
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Organization name is required")
        
        if self.contact_email and "@" not in self.contact_email:
            errors.append("Invalid contact email format")
        
        if self.organization_type and self.organization_type not in [e.value for e in OrganizationType]:
            errors.append("Invalid organization type")
        
        if self.industry and self.industry not in [e.value for e in IndustryType]:
            errors.append("Invalid industry type")
        
        if self.size and self.size not in [e.value for e in OrganizationSize]:
            errors.append("Invalid organization size")
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if organization data is valid"""
        return len(self.validate()) == 0
