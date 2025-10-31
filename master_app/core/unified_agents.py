"""
Unified Agent System - Integrates agents from all subsystems
Provides shared knowledge graph and cross-system collaboration
"""

from typing import Dict, Any, List, Optional
from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel
import asyncio
from datetime import datetime
import json


class KnowledgeEntry(BaseModel):
    """Represents an entry in the knowledge graph"""
    key: str
    value: Any
    source: str
    timestamp: str
    tags: List[str] = []
    related_keys: List[str] = []


class UnifiedKnowledgeGraph:
    """
    Shared knowledge graph accessible by all agents
    Stores and retrieves information across systems
    """
    
    def __init__(self):
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.tags_index: Dict[str, List[str]] = {}
        
    def store(self, key: str, value: Any, source: str, tags: List[str] = None, related_keys: List[str] = None):
        """Store information in the knowledge graph"""
        if tags is None:
            tags = []
        if related_keys is None:
            related_keys = []
            
        entry = KnowledgeEntry(
            key=key,
            value=value,
            source=source,
            timestamp=datetime.now().isoformat(),
            tags=tags,
            related_keys=related_keys
        )
        
        self.entries[key] = entry
        
        # Update tags index
        for tag in tags:
            if tag not in self.tags_index:
                self.tags_index[tag] = []
            if key not in self.tags_index[tag]:
                self.tags_index[tag].append(key)
    
    def retrieve(self, key: str) -> Optional[KnowledgeEntry]:
        """Retrieve information from the knowledge graph"""
        return self.entries.get(key)
    
    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        """Search for entries by tag"""
        keys = self.tags_index.get(tag, [])
        return [self.entries[key] for key in keys if key in self.entries]
    
    def get_related(self, key: str) -> List[KnowledgeEntry]:
        """Get related entries"""
        entry = self.entries.get(key)
        if not entry:
            return []
        
        return [self.entries[k] for k in entry.related_keys if k in self.entries]
    
    def export(self) -> str:
        """Export knowledge graph as JSON"""
        return json.dumps({
            "entries": {k: v.model_dump() for k, v in self.entries.items()},
            "tags_index": self.tags_index
        }, indent=2, default=str)
    
    def import_data(self, data: str):
        """Import knowledge graph from JSON"""
        parsed = json.loads(data)
        
        for key, entry_data in parsed.get("entries", {}).items():
            self.entries[key] = KnowledgeEntry(**entry_data)
        
        self.tags_index = parsed.get("tags_index", {})


class UnifiedAgentSystem:
    """
    Unified agent system that provides cross-system collaboration
    Agents can access shared knowledge and coordinate across systems
    """
    
    def __init__(self, knowledge_graph: UnifiedKnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.agents: Dict[str, Agent] = {}
        
    def create_knowledge_tools(self, source: str):
        """Create knowledge graph tools for agents"""
        
        @function_tool
        def store_knowledge(key: str, value: str, tags: str = "", related_keys: str = ""):
            """
            Store information in the shared knowledge graph for future reference.
            
            Args:
                key: Unique identifier for this knowledge
                value: The information to store
                tags: Comma-separated tags for categorization
                related_keys: Comma-separated keys of related knowledge
            """
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            related_list = [k.strip() for k in related_keys.split(",") if k.strip()]
            
            self.knowledge_graph.store(
                key=key,
                value=value,
                source=source,
                tags=tag_list,
                related_keys=related_list
            )
            return {"status": "success", "key": key}
        
        @function_tool
        def retrieve_knowledge(key: str):
            """
            Retrieve information from the shared knowledge graph.
            
            Args:
                key: The unique identifier of the knowledge to retrieve
            """
            entry = self.knowledge_graph.retrieve(key)
            if entry:
                return {
                    "found": True,
                    "value": entry.value,
                    "source": entry.source,
                    "timestamp": entry.timestamp,
                    "tags": entry.tags,
                    "related_keys": entry.related_keys
                }
            return {"found": False}
        
        @function_tool
        def search_knowledge_by_tag(tag: str):
            """
            Search for knowledge entries by tag.
            
            Args:
                tag: The tag to search for
            """
            entries = self.knowledge_graph.search_by_tag(tag)
            return {
                "count": len(entries),
                "entries": [
                    {
                        "key": e.key,
                        "value": e.value,
                        "source": e.source,
                        "timestamp": e.timestamp
                    }
                    for e in entries
                ]
            }
        
        @function_tool
        def get_related_knowledge(key: str):
            """
            Get knowledge entries related to a specific key.
            
            Args:
                key: The key to find related knowledge for
            """
            entries = self.knowledge_graph.get_related(key)
            return {
                "count": len(entries),
                "entries": [
                    {
                        "key": e.key,
                        "value": e.value,
                        "source": e.source,
                        "timestamp": e.timestamp
                    }
                    for e in entries
                ]
            }
        
        return [store_knowledge, retrieve_knowledge, search_knowledge_by_tag, get_related_knowledge]
    
    def create_meta_agent(self, model: str = "gpt-4o-mini") -> Agent:
        """
        Create a meta-agent that can coordinate across all systems
        """
        instructions = """You are a meta-agent that coordinates across multiple AI systems:
        
        1. Deep Research System - For researching topics, gathering information, and generating reports
        2. Engineering Team - For building software, creating tools, and generating code
        3. Trading Floor - For financial analysis, portfolio management, and trading decisions
        
        You have access to a shared knowledge graph where you can store and retrieve information
        that persists across all systems and agents. Use this to build institutional knowledge.
        
        When given a task, you should:
        1. Break it down into subtasks
        2. Determine which systems are needed
        3. Coordinate the execution across systems
        4. Store important findings in the knowledge graph
        5. Synthesize results into a coherent response
        
        Always think about how to leverage the strengths of each system and how they can work together.
        """
        
        tools = self.create_knowledge_tools("meta_agent")
        
        agent = Agent(
            name="MetaAgent",
            instructions=instructions,
            model=model,
            tools=tools
        )
        
        self.agents["meta_agent"] = agent
        return agent
    
    def create_research_coordinator(self, model: str = "gpt-4o-mini") -> Agent:
        """
        Create an agent that coordinates research across systems
        """
        instructions = """You are a research coordinator that manages research activities across systems.
        
        Your responsibilities:
        - Coordinate deep research on topics
        - Analyze trading portfolios and market conditions
        - Store research findings in the knowledge graph
        - Provide insights based on accumulated knowledge
        
        Use the knowledge graph to build a comprehensive understanding over time.
        Tag your findings appropriately (e.g., 'market_research', 'company_analysis', 'trend').
        """
        
        tools = self.create_knowledge_tools("research_coordinator")
        
        agent = Agent(
            name="ResearchCoordinator",
            instructions=instructions,
            model=model,
            tools=tools
        )
        
        self.agents["research_coordinator"] = agent
        return agent
    
    def create_development_coordinator(self, model: str = "gpt-4o-mini") -> Agent:
        """
        Create an agent that coordinates development activities
        """
        instructions = """You are a development coordinator that manages software development.
        
        Your responsibilities:
        - Coordinate the engineering team to build tools and systems
        - Store information about built tools and their capabilities
        - Help integrate new tools into existing systems
        - Maintain documentation in the knowledge graph
        
        Use the knowledge graph to track what has been built and how systems work.
        Tag your entries appropriately (e.g., 'tool', 'module', 'api', 'documentation').
        """
        
        tools = self.create_knowledge_tools("development_coordinator")
        
        agent = Agent(
            name="DevelopmentCoordinator",
            instructions=instructions,
            model=model,
            tools=tools
        )
        
        self.agents["development_coordinator"] = agent
        return agent
    
    def create_trading_coordinator(self, model: str = "gpt-4o-mini") -> Agent:
        """
        Create an agent that coordinates trading activities
        """
        instructions = """You are a trading coordinator that manages trading and portfolio activities.
        
        Your responsibilities:
        - Coordinate trading decisions across multiple traders
        - Analyze portfolio performance
        - Store market insights and trading strategies
        - Learn from past trades and outcomes
        
        Use the knowledge graph to build trading intelligence over time.
        Tag your entries appropriately (e.g., 'market_data', 'strategy', 'trade', 'analysis').
        """
        
        tools = self.create_knowledge_tools("trading_coordinator")
        
        agent = Agent(
            name="TradingCoordinator",
            instructions=instructions,
            model=model,
            tools=tools
        )
        
        self.agents["trading_coordinator"] = agent
        return agent
    
    async def run_agent(self, agent_name: str, message: str, max_turns: int = 10) -> str:
        """Run an agent with a message"""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
        
        with trace(f"{agent_name}_execution"):
            result = await Runner.run(agent, message, max_turns=max_turns)
            return str(result.final_output)
    
    async def collaborative_task(self, task_description: str, agents: List[str]) -> Dict[str, str]:
        """
        Execute a task collaboratively across multiple agents
        Each agent contributes their perspective
        """
        results = {}
        
        # Run agents in parallel
        tasks = []
        for agent_name in agents:
            if agent_name in self.agents:
                tasks.append(self.run_agent(agent_name, task_description))
        
        agent_results = await asyncio.gather(*tasks)
        
        for agent_name, result in zip(agents, agent_results):
            results[agent_name] = result
        
        return results
    
    def get_agent_list(self) -> List[str]:
        """Get list of available agents"""
        return list(self.agents.keys())
    
    def export_knowledge_graph(self) -> str:
        """Export the knowledge graph"""
        return self.knowledge_graph.export()
    
    def import_knowledge_graph(self, data: str):
        """Import a knowledge graph"""
        self.knowledge_graph.import_data(data)
