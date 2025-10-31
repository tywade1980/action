"""
Example Workflows - Demonstrates how to use the Master AI System
"""

import asyncio
from master_app.core.orchestrator import MasterOrchestrator, SystemType, WorkflowType, Task, Workflow
from master_app.core.unified_agents import UnifiedAgentSystem, UnifiedKnowledgeGraph
from master_app.integrations import ResearchIntegration, EngineeringIntegration, TradingIntegration


async def example_simple_research():
    """
    Example 1: Simple research task
    """
    print("\n" + "="*60)
    print("Example 1: Simple Research Task")
    print("="*60)
    
    orchestrator = MasterOrchestrator()
    research_system = ResearchIntegration()
    orchestrator.register_system(SystemType.DEEP_RESEARCH, research_system)
    
    task = Task(
        id="research_ai_trends",
        system=SystemType.DEEP_RESEARCH,
        action="research",
        params={"query": "Latest AI agent frameworks in 2025"}
    )
    
    result = await orchestrator.execute_task(task)
    
    if result.status == "completed":
        print("\n✅ Research completed successfully!")
        print(f"Report preview: {str(result.result.get('report', ''))[:200]}...")
    else:
        print(f"\n❌ Research failed: {result.error}")


async def example_research_to_trade_workflow():
    """
    Example 2: Research to Trade workflow
    """
    print("\n" + "="*60)
    print("Example 2: Research to Trade Workflow")
    print("="*60)
    
    orchestrator = MasterOrchestrator()
    
    # Register systems
    research_system = ResearchIntegration()
    trading_system = TradingIntegration()
    orchestrator.register_system(SystemType.DEEP_RESEARCH, research_system)
    orchestrator.register_system(SystemType.TRADING_FLOOR, trading_system)
    
    # Create workflow
    workflow = orchestrator.create_workflow(
        WorkflowType.RESEARCH_TO_TRADE,
        {
            "query": "Emerging AI chip companies",
            "trader_name": "Cathie"
        }
    )
    
    orchestrator.workflows[workflow.id] = workflow
    
    print(f"\n📋 Created workflow: {workflow.name}")
    print(f"   Tasks: {len(workflow.tasks)}")
    
    # Execute workflow
    result = await orchestrator.execute_workflow(workflow)
    
    if result.status == "completed":
        print("\n✅ Workflow completed successfully!")
        print(f"   Results: {len(result.results)} tasks completed")
    else:
        print(f"\n❌ Workflow failed")


async def example_build_tool_workflow():
    """
    Example 3: Build Tool workflow
    """
    print("\n" + "="*60)
    print("Example 3: Build Tool Workflow")
    print("="*60)
    
    orchestrator = MasterOrchestrator()
    engineering_system = EngineeringIntegration()
    orchestrator.register_system(SystemType.ENGINEERING_TEAM, engineering_system)
    
    workflow = orchestrator.create_workflow(
        WorkflowType.BUILD_TOOL,
        {
            "requirements": """
            A simple stock price tracker that can:
            - Store stock symbols and prices
            - Calculate price changes
            - Alert on significant moves
            """,
            "module_name": "stock_tracker.py"
        }
    )
    
    orchestrator.workflows[workflow.id] = workflow
    
    print(f"\n📋 Created workflow: {workflow.name}")
    print(f"   Module: stock_tracker.py")
    
    # Note: This would execute the full engineering team
    # Commented out to avoid long execution time in example
    # result = await orchestrator.execute_workflow(workflow)
    
    print("\n💡 Workflow created (execution skipped in example)")


async def example_unified_agents():
    """
    Example 4: Using unified agents with knowledge graph
    """
    print("\n" + "="*60)
    print("Example 4: Unified Agents with Knowledge Graph")
    print("="*60)
    
    knowledge_graph = UnifiedKnowledgeGraph()
    agent_system = UnifiedAgentSystem(knowledge_graph)
    
    # Create agents
    meta_agent = agent_system.create_meta_agent()
    research_coordinator = agent_system.create_research_coordinator()
    
    print(f"\n🤖 Created agents:")
    print(f"   - {meta_agent.name}")
    print(f"   - {research_coordinator.name}")
    
    # Store some knowledge
    knowledge_graph.store(
        key="ai_trends_2025",
        value="Multi-agent systems and autonomous AI are dominant trends",
        source="research",
        tags=["ai", "trends", "2025"],
        related_keys=["agent_frameworks", "automation"]
    )
    
    knowledge_graph.store(
        key="agent_frameworks",
        value="OpenAI Agents SDK, CrewAI, LangGraph, AutoGen are popular",
        source="research",
        tags=["ai", "frameworks", "agents"],
        related_keys=["ai_trends_2025"]
    )
    
    print(f"\n🧠 Knowledge graph:")
    print(f"   - Total entries: {len(knowledge_graph.entries)}")
    print(f"   - Tags: {list(knowledge_graph.tags_index.keys())}")
    
    # Search by tag
    ai_entries = knowledge_graph.search_by_tag("ai")
    print(f"\n🔍 Entries tagged 'ai': {len(ai_entries)}")
    for entry in ai_entries:
        print(f"   - {entry.key}: {entry.value[:50]}...")
    
    # Get related knowledge
    related = knowledge_graph.get_related("ai_trends_2025")
    print(f"\n🔗 Related to 'ai_trends_2025': {len(related)}")
    for entry in related:
        print(f"   - {entry.key}")


async def example_parallel_research():
    """
    Example 5: Parallel research tasks
    """
    print("\n" + "="*60)
    print("Example 5: Parallel Research Tasks")
    print("="*60)
    
    orchestrator = MasterOrchestrator()
    research_system = ResearchIntegration()
    orchestrator.register_system(SystemType.DEEP_RESEARCH, research_system)
    
    # Create multiple research tasks
    topics = [
        "Quantum computing developments",
        "Renewable energy trends",
        "AI in healthcare"
    ]
    
    tasks = []
    for i, topic in enumerate(topics):
        task = Task(
            id=f"research_{i}",
            system=SystemType.DEEP_RESEARCH,
            action="research",
            params={"query": topic}
        )
        tasks.append(task)
    
    print(f"\n📋 Created {len(tasks)} research tasks")
    
    # Execute in parallel
    print("\n⚡ Executing tasks in parallel...")
    results = await asyncio.gather(*[orchestrator.execute_task(task) for task in tasks])
    
    completed = sum(1 for r in results if r.status == "completed")
    print(f"\n✅ Completed: {completed}/{len(tasks)} tasks")


async def example_knowledge_graph_export():
    """
    Example 6: Export and import knowledge graph
    """
    print("\n" + "="*60)
    print("Example 6: Knowledge Graph Export/Import")
    print("="*60)
    
    # Create and populate knowledge graph
    kg1 = UnifiedKnowledgeGraph()
    
    kg1.store("fact1", "Python is great for AI", "system", ["python", "ai"])
    kg1.store("fact2", "Gradio makes UIs easy", "system", ["gradio", "ui"])
    kg1.store("fact3", "Agents can collaborate", "system", ["agents", "collaboration"])
    
    print(f"\n📊 Original knowledge graph: {len(kg1.entries)} entries")
    
    # Export
    exported = kg1.export()
    print(f"\n💾 Exported {len(exported)} characters")
    
    # Create new knowledge graph and import
    kg2 = UnifiedKnowledgeGraph()
    kg2.import_data(exported)
    
    print(f"\n📥 Imported knowledge graph: {len(kg2.entries)} entries")
    
    # Verify
    for key in kg1.entries.keys():
        assert key in kg2.entries, f"Missing key: {key}"
    
    print("\n✅ Export/import successful!")


async def example_system_status():
    """
    Example 7: Monitor system status
    """
    print("\n" + "="*60)
    print("Example 7: System Status Monitoring")
    print("="*60)
    
    orchestrator = MasterOrchestrator()
    
    # Register all systems
    orchestrator.register_system(SystemType.DEEP_RESEARCH, ResearchIntegration())
    orchestrator.register_system(SystemType.ENGINEERING_TEAM, EngineeringIntegration())
    orchestrator.register_system(SystemType.TRADING_FLOOR, TradingIntegration())
    
    # Get status
    status = orchestrator.get_system_status()
    
    print("\n📊 System Status:")
    print(f"\n   Subsystems:")
    for system, state in status["systems"].items():
        emoji = "✅" if state == "active" else "❌"
        print(f"   {emoji} {system}: {state}")
    
    print(f"\n   Workflows:")
    print(f"   - Total: {status['workflows']['total']}")
    print(f"   - Active: {status['workflows']['active']}")
    print(f"   - Completed: {status['workflows']['completed']}")
    print(f"   - Failed: {status['workflows']['failed']}")
    
    print(f"\n   Knowledge Base: {status['knowledge_base_size']} entries")


async def run_all_examples():
    """
    Run all examples
    """
    print("\n" + "="*60)
    print("MASTER AI SYSTEM - EXAMPLE WORKFLOWS")
    print("="*60)
    
    examples = [
        ("Simple Research", example_simple_research),
        ("Unified Agents", example_unified_agents),
        ("Parallel Research", example_parallel_research),
        ("Knowledge Export", example_knowledge_graph_export),
        ("System Status", example_system_status),
    ]
    
    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"\n❌ Example '{name}' failed: {e}")
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    # Run examples
    asyncio.run(run_all_examples())
