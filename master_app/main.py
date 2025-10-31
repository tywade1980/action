"""
Master Application - Main Entry Point
Unified platform integrating Deep Research, Engineering Team, and Trading Floor
"""

import asyncio
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load environment variables
load_dotenv(override=True)

# Add master_app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from master_app.core.orchestrator import MasterOrchestrator, SystemType
from master_app.core.unified_agents import UnifiedAgentSystem, UnifiedKnowledgeGraph
from master_app.integrations import ResearchIntegration, EngineeringIntegration, TradingIntegration
from master_app.ui.dashboard import create_dashboard


def initialize_master_system():
    """
    Initialize the master system with all subsystems
    """
    print("🚀 Initializing Master AI System...")
    
    # Create core components
    orchestrator = MasterOrchestrator()
    knowledge_graph = UnifiedKnowledgeGraph()
    agent_system = UnifiedAgentSystem(knowledge_graph)
    
    # Initialize subsystems
    print("📚 Loading Deep Research system...")
    research_system = ResearchIntegration()
    orchestrator.register_system(SystemType.DEEP_RESEARCH, research_system)
    
    print("⚙️ Loading Engineering Team system...")
    engineering_system = EngineeringIntegration()
    orchestrator.register_system(SystemType.ENGINEERING_TEAM, engineering_system)
    
    print("💹 Loading Trading Floor system...")
    trading_system = TradingIntegration()
    orchestrator.register_system(SystemType.TRADING_FLOOR, trading_system)
    
    # Create unified agents
    print("🤖 Creating unified agents...")
    agent_system.create_meta_agent()
    agent_system.create_research_coordinator()
    agent_system.create_development_coordinator()
    agent_system.create_trading_coordinator()
    
    # Store system information in knowledge graph
    print("🧠 Initializing knowledge graph...")
    knowledge_graph.store(
        key="system_info",
        value={
            "name": "Master AI System",
            "version": "1.0.0",
            "subsystems": ["Deep Research", "Engineering Team", "Trading Floor"],
            "initialized": True
        },
        source="system",
        tags=["system", "metadata"]
    )
    
    # Store subsystem information
    for system_type in [SystemType.DEEP_RESEARCH, SystemType.ENGINEERING_TEAM, SystemType.TRADING_FLOOR]:
        system = orchestrator.systems.get(system_type)
        if system and hasattr(system, 'get_system_info'):
            info = system.get_system_info()
            knowledge_graph.store(
                key=f"system_{system_type.value}",
                value=info,
                source="system",
                tags=["system", "subsystem", system_type.value]
            )
    
    print("✅ Master AI System initialized successfully!")
    print(f"   - {len(orchestrator.systems)} subsystems loaded")
    print(f"   - {len(agent_system.agents)} unified agents created")
    print(f"   - {len(knowledge_graph.entries)} knowledge entries")
    
    return orchestrator, agent_system, knowledge_graph


def main():
    """
    Main entry point for the master application
    """
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🚀 MASTER AI SYSTEM 🚀                       ║
    ║                                                           ║
    ║  Unified Platform for Agentic AI Systems                 ║
    ║                                                           ║
    ║  • Deep Research - Multi-agent research system           ║
    ║  • Engineering Team - Automated development              ║
    ║  • Trading Floor - AI portfolio management               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize the system
    orchestrator, agent_system, knowledge_graph = initialize_master_system()
    
    # Create and launch the dashboard
    print("\n🌐 Launching unified dashboard...")
    ui = create_dashboard(orchestrator)
    
    print("\n" + "="*60)
    print("Dashboard is ready!")
    print("="*60)
    print("\n📊 Access the dashboard in your browser")
    print("   The interface provides:")
    print("   • System status and monitoring")
    print("   • Deep research interface")
    print("   • Engineering team builder")
    print("   • Trading floor management")
    print("   • Workflow automation")
    print("   • Knowledge base explorer")
    print("\n" + "="*60 + "\n")
    
    # Launch the UI
    ui.launch(
        inbrowser=True,
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )


if __name__ == "__main__":
    main()
