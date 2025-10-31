"""
Deep Research System Integration
Wraps the deep research system for use in the master application
"""

import sys
from pathlib import Path

# Add deep research to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "1_deep_research" / "deep_research"))

from research_manager import ResearchManager


class ResearchIntegration:
    """
    Integration wrapper for the Deep Research system
    """
    
    def __init__(self):
        self.manager = ResearchManager()
    
    async def run(self, query: str):
        """
        Execute a research query
        Yields status updates and final report
        """
        async for chunk in self.manager.run(query):
            yield chunk
    
    async def research(self, query: str) -> str:
        """
        Execute research and return final report
        """
        result = None
        async for chunk in self.run(query):
            result = chunk
        return result if result else "No results"
    
    def get_system_info(self) -> dict:
        """Get information about the research system"""
        return {
            "name": "Deep Research",
            "description": "Multi-agent research system with web search",
            "capabilities": [
                "Web search and information gathering",
                "Multi-source research synthesis",
                "Comprehensive report generation",
                "Push notifications"
            ],
            "agents": [
                "Planner Agent - Creates search strategies",
                "Search Agent - Executes web searches",
                "Writer Agent - Synthesizes reports",
                "Push Agent - Sends notifications"
            ]
        }
