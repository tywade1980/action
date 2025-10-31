# Master AI System

## 🚀 Overview

The **Master AI System** is a unified platform that integrates three powerful agentic AI systems into one cohesive application:

1. **Deep Research** - Multi-agent research system with web search and report generation
2. **Engineering Team** - Automated software development using CrewAI
3. **Trading Floor** - AI-powered portfolio management and autonomous trading

All systems share a **unified knowledge graph** for cross-system learning and collaboration.

---

## 🎯 Key Features

### Unified Dashboard
- Single interface to access all three systems
- Real-time system monitoring and event logging
- Integrated workflow automation
- Shared knowledge base explorer

### Cross-System Integration
- **Research → Trading**: Research market trends and execute trades
- **Engineering → All**: Build custom tools for any system
- **Trading → Research**: Analyze portfolio performance
- **Knowledge Sharing**: All systems learn from each other

### Workflow Automation
Predefined workflows that combine multiple systems:
- **Research to Trade**: Research a topic and make trading decisions
- **Build Tool**: Create custom modules and tools
- **Analyze Portfolio**: Deep analysis of trading performance
- **Market Research**: Comprehensive multi-topic research

### Unified Agent System
Specialized coordinator agents:
- **Meta Agent**: Coordinates across all systems
- **Research Coordinator**: Manages research activities
- **Development Coordinator**: Oversees engineering tasks
- **Trading Coordinator**: Handles trading operations

---

## 📁 Architecture

```
master_app/
├── core/
│   ├── orchestrator.py          # Central task and workflow orchestration
│   └── unified_agents.py        # Unified agent system with knowledge graph
├── integrations/
│   ├── research_integration.py  # Deep Research wrapper
│   ├── engineering_integration.py # Engineering Team wrapper
│   └── trading_integration.py   # Trading Floor wrapper
├── ui/
│   └── dashboard.py             # Unified Gradio dashboard
├── main.py                      # Main entry point
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python >= 3.12
- UV package manager
- All dependencies from parent repository

### Installation

```bash
# From the repository root
cd /vercel/sandbox

# Ensure all dependencies are installed
uv sync
```

### Configuration

Ensure your `.env` file contains all necessary API keys:

```bash
# OpenAI (required for all systems)
OPENAI_API_KEY=your_key_here

# Optional: Additional model providers
DEEPSEEK_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
GROK_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here

# Optional: Market data
POLYGON_API_KEY=your_key_here
POLYGON_PLAN=free  # or 'paid' or 'realtime'

# Optional: Push notifications
PUSHOVER_USER=your_user_key
PUSHOVER_TOKEN=your_token
```

### Running the Application

```bash
# From the repository root
python master_app/main.py
```

The dashboard will automatically open in your browser at `http://localhost:7860`

---

## 📊 Dashboard Tabs

### 1. Dashboard
- System status overview
- Real-time event log
- Active workflows monitoring
- Knowledge base statistics

### 2. Deep Research
- Enter research queries
- Get comprehensive reports
- Web search integration
- Automated synthesis

### 3. Engineering Team
- Describe what to build
- Automated design and implementation
- Gradio UI generation
- Unit test creation

### 4. Trading Floor
- View trader portfolios
- Monitor performance
- Execute trading cycles
- Portfolio analytics

### 5. Workflows
- Execute predefined workflows
- Combine multiple systems
- Automated task chains
- Custom workflow parameters

### 6. Knowledge Base
- Search shared knowledge
- View system learning
- Cross-system insights
- Knowledge graph exploration

---

## 🔄 Workflow Examples

### Research to Trade
```json
{
  "query": "Latest AI chip developments",
  "trader_name": "Cathie"
}
```
1. Researches AI chip news
2. Analyzes market implications
3. Executes trades based on findings

### Build Tool
```json
{
  "requirements": "A sentiment analysis tool for financial news",
  "module_name": "sentiment_analyzer.py"
}
```
1. Designs the module
2. Implements the code
3. Creates UI and tests
4. Outputs to `2_engineering_team/engineering_team/output/`

### Analyze Portfolio
```json
{
  "trader_name": "Warren"
}
```
1. Retrieves portfolio holdings
2. Researches each position
3. Generates performance analysis
4. Provides recommendations

### Market Research
```json
{
  "topics": [
    "Quantum computing stocks",
    "Renewable energy trends",
    "AI infrastructure"
  ]
}
```
1. Researches each topic in parallel
2. Synthesizes findings
3. Identifies opportunities
4. Stores insights in knowledge graph

---

## 🧠 Knowledge Graph

The unified knowledge graph enables:

- **Persistent Memory**: Information persists across sessions
- **Cross-System Learning**: All agents share knowledge
- **Tagging System**: Organize information by category
- **Relationship Mapping**: Link related concepts
- **Source Tracking**: Know where information came from

### Using the Knowledge Graph

Agents can:
```python
# Store knowledge
store_knowledge(
    key="nvidia_analysis",
    value="Strong AI chip leader with data center growth",
    tags="stock,analysis,ai",
    related_keys="ai_trends,chip_shortage"
)

# Retrieve knowledge
retrieve_knowledge(key="nvidia_analysis")

# Search by tag
search_knowledge_by_tag(tag="stock")

# Get related knowledge
get_related_knowledge(key="nvidia_analysis")
```

---

## 🎯 Use Cases

### Business Intelligence
- Market research and competitive analysis
- Trend identification and forecasting
- Automated report generation

### Software Development
- Rapid prototyping
- Internal tool creation
- Automated testing
- Documentation generation

### Financial Management
- Portfolio optimization
- Algorithmic trading
- Risk analysis
- Performance tracking

### Research & Analysis
- Academic research
- Technical analysis
- News aggregation
- Data synthesis

---

## 🔧 Customization

### Adding New Workflows

Edit `master_app/core/orchestrator.py`:

```python
def _create_custom_workflow(self, workflow_id: str, params: Dict[str, Any]) -> Workflow:
    """Create your custom workflow"""
    tasks = [
        Task(
            id=f"{workflow_id}_step1",
            system=SystemType.DEEP_RESEARCH,
            action="research",
            params={"query": params.get("query")}
        ),
        # Add more tasks...
    ]
    
    return Workflow(
        id=workflow_id,
        name="Custom Workflow",
        workflow_type=WorkflowType.CUSTOM,
        tasks=tasks
    )
```

### Creating Custom Agents

Edit `master_app/core/unified_agents.py`:

```python
def create_custom_agent(self, model: str = "gpt-4o-mini") -> Agent:
    """Create a custom specialized agent"""
    instructions = """Your custom agent instructions..."""
    
    tools = self.create_knowledge_tools("custom_agent")
    
    agent = Agent(
        name="CustomAgent",
        instructions=instructions,
        model=model,
        tools=tools
    )
    
    self.agents["custom_agent"] = agent
    return agent
```

---

## 📈 System Status

The orchestrator tracks:
- **Active Systems**: Which subsystems are loaded
- **Workflow Statistics**: Total, active, completed, failed
- **Knowledge Base Size**: Number of stored entries
- **Event Log**: Real-time system events

---

## 🔐 Security Notes

- API keys are loaded from `.env` file
- Never commit `.env` to version control
- Use environment-specific configurations
- Monitor API usage and costs
- Review generated code before execution

---

## 🐛 Troubleshooting

### Dashboard won't start
- Check all API keys are set in `.env`
- Ensure port 7860 is available
- Verify all dependencies are installed

### Subsystem not loading
- Check system-specific requirements
- Verify file paths in integration modules
- Review error logs in console

### Workflow fails
- Check event log in dashboard
- Verify task parameters
- Ensure required systems are active

---

## 📚 Related Documentation

- [Deep Research System](../1_deep_research/)
- [Engineering Team](../2_engineering_team/)
- [Trading Floor](../3_trading_floor/)
- [Repository Analysis](../REPOSITORY_ANALYSIS.md)

---

## 🤝 Contributing

To extend the master system:

1. Create integration in `integrations/`
2. Register system in `main.py`
3. Add UI tab in `ui/dashboard.py`
4. Define workflows in `core/orchestrator.py`
5. Create specialized agents in `core/unified_agents.py`

---

## 📝 License

Same as parent repository (see LICENSE file in root)

---

## 🎓 Learning Resources

This master application demonstrates:
- Multi-agent orchestration
- Cross-system integration
- Workflow automation
- Knowledge graph implementation
- Gradio dashboard development
- Async Python patterns
- Event-driven architecture

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Real-time collaboration between agents
- [ ] Advanced workflow builder UI
- [ ] Knowledge graph visualization
- [ ] Performance analytics dashboard
- [ ] Custom tool marketplace
- [ ] Multi-user support
- [ ] Cloud deployment options
- [ ] API endpoints for external integration

---

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review system logs
- Consult parent repository documentation
- Contact: ed@edwarddonner.com

---

**Built with ❤️ using OpenAI Agents SDK, CrewAI, and Gradio**
