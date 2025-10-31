"""
Master Orchestrator - Coordinates all agentic AI systems
Integrates Deep Research, Engineering Team, and Trading Floor
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime
import json


class SystemType(Enum):
    """Available subsystems"""
    DEEP_RESEARCH = "deep_research"
    ENGINEERING_TEAM = "engineering_team"
    TRADING_FLOOR = "trading_floor"
    ALL = "all"


class WorkflowType(Enum):
    """Predefined workflow types"""
    RESEARCH_TO_TRADE = "research_to_trade"
    BUILD_TOOL = "build_tool"
    ANALYZE_PORTFOLIO = "analyze_portfolio"
    MARKET_RESEARCH = "market_research"
    CUSTOM = "custom"


@dataclass
class Task:
    """Represents a task to be executed"""
    id: str
    system: SystemType
    action: str
    params: Dict[str, Any]
    dependencies: List[str] = None
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Workflow:
    """Represents a workflow of multiple tasks"""
    id: str
    name: str
    workflow_type: WorkflowType
    tasks: List[Task]
    status: str = "pending"
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.results is None:
            self.results = {}


class MasterOrchestrator:
    """
    Central orchestrator that coordinates all agentic AI systems
    Manages workflows, task execution, and cross-system communication
    """
    
    def __init__(self):
        self.systems: Dict[SystemType, Any] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.tasks: Dict[str, Task] = {}
        self.knowledge_base: Dict[str, Any] = {}
        self.event_handlers: List[Callable] = []
        
    def register_system(self, system_type: SystemType, system_instance: Any):
        """Register a subsystem with the orchestrator"""
        self.systems[system_type] = system_instance
        self._emit_event("system_registered", {"system": system_type.value})
        
    def register_event_handler(self, handler: Callable):
        """Register an event handler for system events"""
        self.event_handlers.append(handler)
        
    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to all registered handlers"""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        for handler in self.event_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")
    
    async def execute_task(self, task: Task) -> Task:
        """Execute a single task"""
        task.status = "running"
        self._emit_event("task_started", {"task_id": task.id, "system": task.system.value})
        
        try:
            system = self.systems.get(task.system)
            if not system:
                raise ValueError(f"System {task.system.value} not registered")
            
            # Execute the task based on system type
            if task.system == SystemType.DEEP_RESEARCH:
                result = await self._execute_research_task(system, task)
            elif task.system == SystemType.ENGINEERING_TEAM:
                result = await self._execute_engineering_task(system, task)
            elif task.system == SystemType.TRADING_FLOOR:
                result = await self._execute_trading_task(system, task)
            else:
                raise ValueError(f"Unknown system type: {task.system}")
            
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
            self._emit_event("task_completed", {
                "task_id": task.id,
                "system": task.system.value,
                "duration": (task.completed_at - task.created_at).total_seconds()
            })
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            self._emit_event("task_failed", {
                "task_id": task.id,
                "system": task.system.value,
                "error": str(e)
            })
        
        return task
    
    async def _execute_research_task(self, system: Any, task: Task) -> Any:
        """Execute a deep research task"""
        action = task.action
        params = task.params
        
        if action == "research":
            query = params.get("query")
            results = []
            async for chunk in system.run(query):
                results.append(chunk)
            return {"report": results[-1] if results else None, "chunks": results}
        else:
            raise ValueError(f"Unknown research action: {action}")
    
    async def _execute_engineering_task(self, system: Any, task: Task) -> Any:
        """Execute an engineering team task"""
        action = task.action
        params = task.params
        
        if action == "build":
            requirements = params.get("requirements")
            module_name = params.get("module_name", "module")
            class_name = params.get("class_name", "Module")
            
            inputs = {
                "requirements": requirements,
                "module_name": module_name,
                "class_name": class_name
            }
            
            result = system.crew().kickoff(inputs=inputs)
            return {"result": str(result), "module_name": module_name}
        else:
            raise ValueError(f"Unknown engineering action: {action}")
    
    async def _execute_trading_task(self, system: Any, task: Task) -> Any:
        """Execute a trading floor task"""
        action = task.action
        params = task.params
        
        if action == "trade":
            trader_name = params.get("trader_name")
            trader = system.get_trader(trader_name)
            if trader:
                await trader.run()
                return {"trader": trader_name, "status": "completed"}
            else:
                raise ValueError(f"Trader {trader_name} not found")
        elif action == "get_portfolio":
            trader_name = params.get("trader_name")
            account = system.get_account(trader_name)
            return {"account": account.model_dump() if account else None}
        else:
            raise ValueError(f"Unknown trading action: {action}")
    
    async def execute_workflow(self, workflow: Workflow) -> Workflow:
        """Execute a complete workflow"""
        workflow.status = "running"
        self._emit_event("workflow_started", {"workflow_id": workflow.id, "type": workflow.workflow_type.value})
        
        try:
            # Build dependency graph
            task_map = {task.id: task for task in workflow.tasks}
            completed_tasks = set()
            
            while len(completed_tasks) < len(workflow.tasks):
                # Find tasks ready to execute
                ready_tasks = []
                for task in workflow.tasks:
                    if task.id not in completed_tasks:
                        deps_met = all(dep in completed_tasks for dep in task.dependencies)
                        if deps_met:
                            ready_tasks.append(task)
                
                if not ready_tasks:
                    raise RuntimeError("Circular dependency or no tasks ready")
                
                # Execute ready tasks in parallel
                results = await asyncio.gather(*[self.execute_task(task) for task in ready_tasks])
                
                # Mark as completed and store results
                for task in results:
                    completed_tasks.add(task.id)
                    workflow.results[task.id] = task.result
            
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            self._emit_event("workflow_completed", {
                "workflow_id": workflow.id,
                "type": workflow.workflow_type.value,
                "duration": (workflow.completed_at - workflow.created_at).total_seconds()
            })
            
        except Exception as e:
            workflow.status = "failed"
            workflow.completed_at = datetime.now()
            self._emit_event("workflow_failed", {
                "workflow_id": workflow.id,
                "type": workflow.workflow_type.value,
                "error": str(e)
            })
        
        return workflow
    
    def create_workflow(self, workflow_type: WorkflowType, params: Dict[str, Any]) -> Workflow:
        """Create a predefined workflow"""
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if workflow_type == WorkflowType.RESEARCH_TO_TRADE:
            return self._create_research_to_trade_workflow(workflow_id, params)
        elif workflow_type == WorkflowType.BUILD_TOOL:
            return self._create_build_tool_workflow(workflow_id, params)
        elif workflow_type == WorkflowType.ANALYZE_PORTFOLIO:
            return self._create_analyze_portfolio_workflow(workflow_id, params)
        elif workflow_type == WorkflowType.MARKET_RESEARCH:
            return self._create_market_research_workflow(workflow_id, params)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
    
    def _create_research_to_trade_workflow(self, workflow_id: str, params: Dict[str, Any]) -> Workflow:
        """Create a workflow that researches a topic and makes trading decisions"""
        query = params.get("query", "Latest market trends")
        trader_name = params.get("trader_name", "Warren")
        
        tasks = [
            Task(
                id=f"{workflow_id}_research",
                system=SystemType.DEEP_RESEARCH,
                action="research",
                params={"query": query}
            ),
            Task(
                id=f"{workflow_id}_trade",
                system=SystemType.TRADING_FLOOR,
                action="trade",
                params={"trader_name": trader_name},
                dependencies=[f"{workflow_id}_research"]
            )
        ]
        
        return Workflow(
            id=workflow_id,
            name="Research to Trade",
            workflow_type=WorkflowType.RESEARCH_TO_TRADE,
            tasks=tasks
        )
    
    def _create_build_tool_workflow(self, workflow_id: str, params: Dict[str, Any]) -> Workflow:
        """Create a workflow that builds a custom tool"""
        requirements = params.get("requirements", "A simple calculator")
        module_name = params.get("module_name", "calculator.py")
        
        tasks = [
            Task(
                id=f"{workflow_id}_build",
                system=SystemType.ENGINEERING_TEAM,
                action="build",
                params={
                    "requirements": requirements,
                    "module_name": module_name,
                    "class_name": "Calculator"
                }
            )
        ]
        
        return Workflow(
            id=workflow_id,
            name="Build Tool",
            workflow_type=WorkflowType.BUILD_TOOL,
            tasks=tasks
        )
    
    def _create_analyze_portfolio_workflow(self, workflow_id: str, params: Dict[str, Any]) -> Workflow:
        """Create a workflow that analyzes portfolio performance"""
        trader_name = params.get("trader_name", "Warren")
        
        tasks = [
            Task(
                id=f"{workflow_id}_get_portfolio",
                system=SystemType.TRADING_FLOOR,
                action="get_portfolio",
                params={"trader_name": trader_name}
            ),
            Task(
                id=f"{workflow_id}_research",
                system=SystemType.DEEP_RESEARCH,
                action="research",
                params={"query": f"Analysis of portfolio holdings for {trader_name}"},
                dependencies=[f"{workflow_id}_get_portfolio"]
            )
        ]
        
        return Workflow(
            id=workflow_id,
            name="Analyze Portfolio",
            workflow_type=WorkflowType.ANALYZE_PORTFOLIO,
            tasks=tasks
        )
    
    def _create_market_research_workflow(self, workflow_id: str, params: Dict[str, Any]) -> Workflow:
        """Create a workflow for comprehensive market research"""
        topics = params.get("topics", ["AI stocks", "Tech trends", "Market outlook"])
        
        tasks = []
        for i, topic in enumerate(topics):
            tasks.append(Task(
                id=f"{workflow_id}_research_{i}",
                system=SystemType.DEEP_RESEARCH,
                action="research",
                params={"query": topic}
            ))
        
        return Workflow(
            id=workflow_id,
            name="Market Research",
            workflow_type=WorkflowType.MARKET_RESEARCH,
            tasks=tasks
        )
    
    def store_knowledge(self, key: str, value: Any):
        """Store information in the shared knowledge base"""
        self.knowledge_base[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._emit_event("knowledge_stored", {"key": key})
    
    def retrieve_knowledge(self, key: str) -> Optional[Any]:
        """Retrieve information from the shared knowledge base"""
        entry = self.knowledge_base.get(key)
        if entry:
            self._emit_event("knowledge_retrieved", {"key": key})
            return entry["value"]
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all systems"""
        return {
            "systems": {
                system_type.value: "active" if system else "inactive"
                for system_type, system in self.systems.items()
            },
            "workflows": {
                "total": len(self.workflows),
                "active": sum(1 for w in self.workflows.values() if w.status == "running"),
                "completed": sum(1 for w in self.workflows.values() if w.status == "completed"),
                "failed": sum(1 for w in self.workflows.values() if w.status == "failed")
            },
            "knowledge_base_size": len(self.knowledge_base)
        }
    
    def export_workflow_results(self, workflow_id: str) -> Optional[str]:
        """Export workflow results as JSON"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        export_data = {
            "workflow_id": workflow.id,
            "name": workflow.name,
            "type": workflow.workflow_type.value,
            "status": workflow.status,
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "results": workflow.results
        }
        
        return json.dumps(export_data, indent=2, default=str)
