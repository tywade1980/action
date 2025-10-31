"""
Engineering Team Integration
Wraps the CrewAI engineering team for use in the master application
"""

import sys
from pathlib import Path

# Add engineering team to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "2_engineering_team" / "engineering_team" / "src"))

from engineering_team.crew import EngineeringTeam


class EngineeringIntegration:
    """
    Integration wrapper for the Engineering Team system
    """
    
    def __init__(self):
        self._crew = None
    
    def crew(self):
        """Get or create the engineering team crew"""
        if self._crew is None:
            self._crew = EngineeringTeam()
        return self._crew
    
    def build(self, requirements: str, module_name: str = "module.py", class_name: str = "Module"):
        """
        Build a module based on requirements
        
        Args:
            requirements: Description of what to build
            module_name: Name of the module file
            class_name: Name of the main class
            
        Returns:
            Result from the crew execution
        """
        inputs = {
            'requirements': requirements,
            'module_name': module_name,
            'class_name': class_name
        }
        
        result = self.crew().crew().kickoff(inputs=inputs)
        return result
    
    def get_system_info(self) -> dict:
        """Get information about the engineering system"""
        return {
            "name": "Engineering Team",
            "description": "Multi-agent software development team using CrewAI",
            "capabilities": [
                "Software design and architecture",
                "Python module implementation",
                "Gradio UI generation",
                "Unit test creation",
                "Code execution in safe environment"
            ],
            "agents": [
                "Engineering Lead (GPT-4o) - Creates designs",
                "Backend Engineer (Claude 3.7) - Implements code",
                "Frontend Engineer (Claude 3.7) - Creates UIs",
                "Test Engineer (Claude 3.7) - Writes tests"
            ],
            "process": "Sequential (Design → Code → Frontend → Test)"
        }
