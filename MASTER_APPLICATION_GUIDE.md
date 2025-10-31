# Master Application Guide

## Complete Integration of All Repository Systems

This guide provides comprehensive documentation for the Master AI System that unifies all three agentic AI systems in this repository.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Features List](#features-list)
4. [Installation & Setup](#installation--setup)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Workflow Catalog](#workflow-catalog)
8. [Best Practices](#best-practices)

---

## Overview

### What is the Master AI System?

The Master AI System is a unified platform that integrates three powerful agentic AI systems:

| System | Purpose | Framework | Key Features |
|--------|---------|-----------|--------------|
| **Deep Research** | Information gathering & synthesis | OpenAI Agents SDK | Web search, report generation, multi-agent coordination |
| **Engineering Team** | Software development automation | CrewAI | Design, coding, UI creation, testing |
| **Trading Floor** | Portfolio management & trading | OpenAI Agents SDK + MCP | Multi-trader simulation, market data, autonomous trading |

### Why Use the Master System?

- **Unified Interface**: Single dashboard for all systems
- **Cross-System Workflows**: Combine capabilities across systems
- **Shared Knowledge**: All agents learn from each other
- **Workflow Automation**: Predefined and custom workflows
- **Scalable Architecture**: Easy to extend and customize

---

## System Architecture

### Component Hierarchy

```
Master AI System
│
├── Core Layer
│   ├── Orchestrator (Task & Workflow Management)
│   └── Unified Agents (Knowledge Graph & Coordination)
│
├── Integration Layer
│   ├── Research Integration
│   ├── Engineering Integration
│   └── Trading Integration
│
├── UI Layer
│   └── Unified Dashboard (Gradio)
│
└── Examples Layer
    └── Workflow Demonstrations
```

### Data Flow

```
User Input → Dashboard → Orchestrator → Integration → Subsystem → Result
                ↓                                          ↓
         Knowledge Graph ←──────────────────────────────────┘
```

---

## Features List

### Core Features

✅ **Unified Orchestration**
- Task management and execution
- Workflow automation
- Dependency resolution
- Parallel execution
- Error handling and recovery

✅ **Knowledge Graph**
- Persistent memory across sessions
- Tag-based organization
- Relationship mapping
- Cross-system knowledge sharing
- Export/import capabilities

✅ **Unified Agents**
- Meta Agent (cross-system coordination)
- Research Coordinator
- Development Coordinator
- Trading Coordinator
- Custom agent creation

✅ **Dashboard Interface**
- System status monitoring
- Real-time event logging
- Research interface
- Engineering builder
- Trading management
- Workflow executor
- Knowledge explorer

### Integration Features

✅ **Deep Research Integration**
- Multi-agent research pipeline
- Web search capabilities
- Report generation
- Push notifications
- Streaming results

✅ **Engineering Team Integration**
- CrewAI workflow execution
- Multi-agent development
- Code generation
- UI creation
- Test automation

✅ **Trading Floor Integration**
- Multi-trader management
- Portfolio tracking
- Market data access
- Trade execution
- Performance analytics

### Workflow Features

✅ **Predefined Workflows**
- Research to Trade
- Build Tool
- Analyze Portfolio
- Market Research

✅ **Custom Workflows**
- Define task sequences
- Set dependencies
- Configure parameters
- Monitor execution

---

## Installation & Setup

### Prerequisites

```bash
# Required
Python >= 3.12
UV package manager

# Optional but recommended
Docker (for CrewAI code execution)
```

### Step 1: Install Dependencies

```bash
# From repository root
cd /vercel/sandbox

# Install all dependencies
uv sync
```

### Step 2: Configure Environment

Create or update `.env` file:

```bash
# Required: OpenAI API
OPENAI_API_KEY=sk-...

# Optional: Additional Models
DEEPSEEK_API_KEY=...
GOOGLE_API_KEY=...
GROK_API_KEY=...
OPENROUTER_API_KEY=...

# Optional: Market Data
POLYGON_API_KEY=...
POLYGON_PLAN=free  # or 'paid' or 'realtime'

# Optional: Notifications
PUSHOVER_USER=...
PUSHOVER_TOKEN=...

# Optional: Trading Configuration
RUN_EVERY_N_MINUTES=60
RUN_EVEN_WHEN_MARKET_IS_CLOSED=false
USE_MANY_MODELS=false
```

### Step 3: Launch the Application

```bash
# From repository root
python master_app/main.py
```

The dashboard will open at `http://localhost:7860`

---

## Usage Examples

### Example 1: Simple Research

```python
from master_app import MasterOrchestrator, SystemType, Task
from master_app.integrations import ResearchIntegration

# Initialize
orchestrator = MasterOrchestrator()
research = ResearchIntegration()
orchestrator.register_system(SystemType.DEEP_RESEARCH, research)

# Create task
task = Task(
    id="research_1",
    system=SystemType.DEEP_RESEARCH,
    action="research",
    params={"query": "Latest AI developments"}
)

# Execute
result = await orchestrator.execute_task(task)
print(result.result)
```

### Example 2: Build a Tool

```python
from master_app import MasterOrchestrator, SystemType, Task
from master_app.integrations import EngineeringIntegration

# Initialize
orchestrator = MasterOrchestrator()
engineering = EngineeringIntegration()
orchestrator.register_system(SystemType.ENGINEERING_TEAM, engineering)

# Create task
task = Task(
    id="build_1",
    system=SystemType.ENGINEERING_TEAM,
    action="build",
    params={
        "requirements": "A calculator with basic operations",
        "module_name": "calculator.py",
        "class_name": "Calculator"
    }
)

# Execute
result = await orchestrator.execute_task(task)
```

### Example 3: Execute Workflow

```python
from master_app import MasterOrchestrator, WorkflowType

# Initialize with all systems
orchestrator = initialize_all_systems()

# Create workflow
workflow = orchestrator.create_workflow(
    WorkflowType.RESEARCH_TO_TRADE,
    {
        "query": "Emerging tech stocks",
        "trader_name": "Cathie"
    }
)

# Execute
result = await orchestrator.execute_workflow(workflow)
print(result.results)
```

### Example 4: Use Knowledge Graph

```python
from master_app import UnifiedKnowledgeGraph, UnifiedAgentSystem

# Create knowledge graph
kg = UnifiedKnowledgeGraph()

# Store knowledge
kg.store(
    key="market_insight",
    value="AI chips showing strong growth",
    source="research",
    tags=["market", "ai", "chips"],
    related_keys=["nvidia", "amd"]
)

# Retrieve knowledge
entry = kg.retrieve("market_insight")
print(entry.value)

# Search by tag
results = kg.search_by_tag("market")
for entry in results:
    print(f"{entry.key}: {entry.value}")
```

### Example 5: Create Custom Agent

```python
from master_app import UnifiedAgentSystem, UnifiedKnowledgeGraph

# Initialize
kg = UnifiedKnowledgeGraph()
agent_system = UnifiedAgentSystem(kg)

# Create custom agent
from agents import Agent

instructions = "You are a specialized analyst..."
tools = agent_system.create_knowledge_tools("analyst")

agent = Agent(
    name="CustomAnalyst",
    instructions=instructions,
    model="gpt-4o-mini",
    tools=tools
)

agent_system.agents["analyst"] = agent

# Use agent
result = await agent_system.run_agent("analyst", "Analyze market trends")
```

---

## API Reference

### MasterOrchestrator

```python
class MasterOrchestrator:
    def register_system(system_type: SystemType, system_instance: Any)
    def register_event_handler(handler: Callable)
    async def execute_task(task: Task) -> Task
    async def execute_workflow(workflow: Workflow) -> Workflow
    def create_workflow(workflow_type: WorkflowType, params: Dict) -> Workflow
    def store_knowledge(key: str, value: Any)
    def retrieve_knowledge(key: str) -> Optional[Any]
    def get_system_status() -> Dict[str, Any]
    def export_workflow_results(workflow_id: str) -> Optional[str]
```

### UnifiedKnowledgeGraph

```python
class UnifiedKnowledgeGraph:
    def store(key: str, value: Any, source: str, tags: List[str], related_keys: List[str])
    def retrieve(key: str) -> Optional[KnowledgeEntry]
    def search_by_tag(tag: str) -> List[KnowledgeEntry]
    def get_related(key: str) -> List[KnowledgeEntry]
    def export() -> str
    def import_data(data: str)
```

### UnifiedAgentSystem

```python
class UnifiedAgentSystem:
    def create_knowledge_tools(source: str) -> List[Tool]
    def create_meta_agent(model: str) -> Agent
    def create_research_coordinator(model: str) -> Agent
    def create_development_coordinator(model: str) -> Agent
    def create_trading_coordinator(model: str) -> Agent
    async def run_agent(agent_name: str, message: str, max_turns: int) -> str
    async def collaborative_task(task_description: str, agents: List[str]) -> Dict[str, str]
    def get_agent_list() -> List[str]
    def export_knowledge_graph() -> str
    def import_knowledge_graph(data: str)
```

---

## Workflow Catalog

### 1. Research to Trade

**Purpose**: Research a topic and execute trades based on findings

**Parameters**:
```json
{
  "query": "Topic to research",
  "trader_name": "Warren|George|Ray|Cathie"
}
```

**Steps**:
1. Deep research on query
2. Analyze trading implications
3. Execute trades via specified trader

**Use Cases**:
- News-driven trading
- Sector analysis
- Company research

### 2. Build Tool

**Purpose**: Create a custom software module

**Parameters**:
```json
{
  "requirements": "Description of what to build",
  "module_name": "filename.py"
}
```

**Steps**:
1. Design architecture
2. Implement code
3. Create UI
4. Generate tests

**Use Cases**:
- Internal tools
- Prototypes
- Utilities

### 3. Analyze Portfolio

**Purpose**: Deep analysis of trading performance

**Parameters**:
```json
{
  "trader_name": "Warren|George|Ray|Cathie"
}
```

**Steps**:
1. Retrieve portfolio holdings
2. Research each position
3. Generate analysis report

**Use Cases**:
- Performance review
- Risk assessment
- Strategy evaluation

### 4. Market Research

**Purpose**: Comprehensive multi-topic research

**Parameters**:
```json
{
  "topics": ["Topic 1", "Topic 2", "Topic 3"]
}
```

**Steps**:
1. Research each topic in parallel
2. Synthesize findings
3. Identify opportunities

**Use Cases**:
- Market overview
- Trend analysis
- Opportunity identification

---

## Best Practices

### 1. Knowledge Graph Usage

✅ **DO**:
- Use descriptive keys
- Tag entries consistently
- Link related concepts
- Store actionable insights

❌ **DON'T**:
- Store temporary data
- Use generic keys
- Forget to tag entries
- Duplicate information

### 2. Workflow Design

✅ **DO**:
- Break complex tasks into steps
- Set clear dependencies
- Handle errors gracefully
- Monitor execution

❌ **DON'T**:
- Create circular dependencies
- Skip error handling
- Ignore task results
- Over-complicate workflows

### 3. Agent Coordination

✅ **DO**:
- Use specialized agents
- Share knowledge via graph
- Coordinate through orchestrator
- Monitor agent interactions

❌ **DON'T**:
- Create redundant agents
- Bypass orchestrator
- Ignore agent outputs
- Mix responsibilities

### 4. System Integration

✅ **DO**:
- Register all systems
- Handle integration errors
- Monitor system health
- Log important events

❌ **DON'T**:
- Assume systems are available
- Ignore error messages
- Skip initialization
- Bypass integration layer

---

## Troubleshooting

### Common Issues

**Issue**: Dashboard won't start
- Check API keys in `.env`
- Verify port 7860 is available
- Ensure dependencies installed

**Issue**: Workflow fails
- Check event log in dashboard
- Verify task parameters
- Ensure systems registered

**Issue**: Knowledge graph not persisting
- Check file permissions
- Verify export/import calls
- Review error logs

**Issue**: Agent not responding
- Check API key validity
- Monitor API rate limits
- Review agent instructions

---

## Performance Tips

1. **Parallel Execution**: Use workflows for parallel tasks
2. **Caching**: Store frequently accessed data in knowledge graph
3. **Batch Operations**: Group similar tasks together
4. **Resource Management**: Monitor API usage and costs
5. **Error Recovery**: Implement retry logic for failed tasks

---

## Security Considerations

1. **API Keys**: Never commit `.env` to version control
2. **Code Execution**: Review generated code before running
3. **Data Privacy**: Be mindful of sensitive information
4. **Access Control**: Implement authentication for production
5. **Audit Logging**: Monitor system events and actions

---

## Future Enhancements

Planned features:
- Real-time agent collaboration
- Visual workflow builder
- Knowledge graph visualization
- Advanced analytics dashboard
- Multi-user support
- Cloud deployment
- REST API endpoints
- Plugin system

---

## Support & Resources

- **Documentation**: See `master_app/README.md`
- **Examples**: Run `python master_app/examples/example_workflows.py`
- **Repository Analysis**: See `REPOSITORY_ANALYSIS.md`
- **Contact**: ed@edwarddonner.com

---

**Built with ❤️ using OpenAI Agents SDK, CrewAI, and Gradio**
