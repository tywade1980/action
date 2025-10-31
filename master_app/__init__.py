"""
Master AI System
Unified platform integrating Deep Research, Engineering Team, and Trading Floor
"""

__version__ = "1.0.0"
__author__ = "Master AI System"

from .core.orchestrator import MasterOrchestrator, SystemType, WorkflowType, Task, Workflow
from .core.unified_agents import UnifiedAgentSystem, UnifiedKnowledgeGraph
from .integrations import ResearchIntegration, EngineeringIntegration, TradingIntegration

__all__ = [
    'MasterOrchestrator',
    'SystemType',
    'WorkflowType',
    'Task',
    'Workflow',
    'UnifiedAgentSystem',
    'UnifiedKnowledgeGraph',
    'ResearchIntegration',
    'EngineeringIntegration',
    'TradingIntegration'
]
