# backend/app/db/models.py
import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True) # e.g., 'tenant_saasify_99'
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    configs = relationship("BusinessConfig", back_populates="tenant", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="tenant", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="tenant", cascade="all, delete-orphan")

class BusinessConfig(Base):
    __tablename__ = "business_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Core JSON payload containing FAQs, rules, qualification keys as per contracts
    config_data = Column(JSON, nullable=False) 
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="configs")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True) # Unique reference key
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=True)
    contact_info = Column(String, nullable=True) # Phone or Email context
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="customers")
    conversations = relationship("Conversation", back_populates="customer", cascade="all, delete-orphan")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(String, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Fields generated from Analytics Agent Output Contract
    score = Column(Integer, default=0)
    intent = Column(String, nullable=True)
    category = Column(String, default="cold_lead") # hot_lead, warm_lead, cold_lead
    status = Column(String, default="new") # open, processing, qualified, archived
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="leads")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True) # unique pipeline tracking session id
    customer_id = Column(String, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, default="active") # active, closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    turns = relationship("ConversationTurn", back_populates="conversation", cascade="all, delete-orphan")

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False) # 'user', 'assistant' or 'system'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="turns")
    agent_logs = relationship("AgentOutput", back_populates="turn", cascade="all, delete-orphan")

class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    turn_id = Column(Integer, ForeignKey("conversation_turns.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name = Column(String, nullable=False) # 'analytics_ai' or 'sales_ai'
    
    # Store complete structured json map from the agent output block safely
    structured_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    turn = relationship("ConversationTurn", back_populates="agent_logs")

class ScenarioUpdate(Base):
    __tablename__ = "scenario_updates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    pattern_detected = Column(Text, nullable=False)
    suggested_improvements = Column(JSON, nullable=False) # recommendations array block
    status = Column(String, default="pending") # pending, applied, dismissed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ManagerReport(Base):
    __tablename__ = "manager_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    summary_text = Column(Text, nullable=False)
    metrics = Column(JSON, nullable=False) # breakout dict containing aggregate performance metadata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)